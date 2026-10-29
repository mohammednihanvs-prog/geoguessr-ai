import os
import sys
import urllib.parse
import torch
import torch.nn as nn
import folium
from folium.plugins import HeatMap
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CACHE_FILE = "embeddings_cache.pt"
CORRECTIONS_FILE = "corrections_cache.pt"
ADAPTER_FILE = "clip_adapter.pt"

# --- Residual Vision Adapter Architecture (Tip-Adapter / CLIP-Adapter) ---
class ResidualAdapter(nn.Module):
    def __init__(self, dim=768, bottleneck=256, alpha=0.5):
        super().__init__()
        self.alpha = alpha
        self.net = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, bottleneck),
            nn.GELU(),
            nn.Linear(bottleneck, dim)
        )

    def forward(self, x):
        residual = self.net(x)
        out = self.alpha * x + (1.0 - self.alpha) * residual
        return out / out.norm(dim=-1, keepdim=True)

# 1. Load corrections if available
corrections = []
if os.path.exists(CORRECTIONS_FILE):
    try:
        corrections = torch.load(CORRECTIONS_FILE, weights_only=False)
        print(f"Loaded {len(corrections)} visual user correction fingerprints.")
    except Exception:
        corrections = []

# 2. Load cached location database
print(f"Loading cached location database from '{CACHE_FILE}'...")
cache_data = torch.load(CACHE_FILE, weights_only=False)
text_embeddings = cache_data["embeddings"]  # Shape: [N, 768]
locations = cache_data["locations"]

# Strict deduplication on load
seen_names = set()
unique_indices = []
unique_locations = []
for idx, loc in enumerate(locations):
    norm_n = loc["name"].strip().lower()
    if norm_n not in seen_names:
        seen_names.add(norm_n)
        unique_indices.append(idx)
        unique_locations.append(loc)
if len(unique_locations) < len(locations):
    locations = unique_locations
    text_embeddings = text_embeddings[unique_indices]

print(f"Loaded {len(locations)} locations with embedding vectors of dimension {text_embeddings.shape[1]}.")

# 3. Load clean pre-trained StreetCLIP model
print("Loading StreetCLIP model...")
model_name = "geolocal/StreetCLIP"
try:
    processor = CLIPProcessor.from_pretrained(model_name, local_files_only=True)
    model = CLIPModel.from_pretrained(model_name, local_files_only=True)
except Exception:
    processor = CLIPProcessor.from_pretrained(model_name)
    model = CLIPModel.from_pretrained(model_name)

model.eval()

# 4. Load Residual Adapter if trained
adapter = None
if os.path.exists(ADAPTER_FILE):
    try:
        adapter = ResidualAdapter()
        adapter.load_state_dict(torch.load(ADAPTER_FILE, map_location="cpu", weights_only=True))
        adapter.eval()
        print(f"Loaded trained Residual Vision Adapter from '{ADAPTER_FILE}'.")
    except Exception as e:
        print(f"Notice: Could not load '{ADAPTER_FILE}': {e}")
        adapter = None

def extract_visual_representation(image: Image.Image):
    """
    Extracts multi-scale visual features:
    1. Full scene (60% weight)
    2. Lower road / soil / markings crop (25% weight)
    3. Center landscape crop (15% weight)
    """
    w, h = image.size
    crops = [
        image,
        image.crop((0, int(h * 0.25), w, h)),
        image.crop((int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9)))
    ]
    weights = [0.60, 0.25, 0.15]

    inputs = processor(images=crops, return_tensors="pt")
    with torch.no_grad():
        out = model.get_image_features(pixel_values=inputs["pixel_values"])
        raw = out.pooler_output if hasattr(out, "pooler_output") else out
        norms = raw / raw.norm(dim=-1, keepdim=True)
        w_tensor = torch.tensor(weights, device=norms.device).unsqueeze(1)
        combined = (norms * w_tensor).sum(dim=0, keepdim=True)
        image_embedding = combined / combined.norm(dim=-1, keepdim=True)

        # Apply trained residual adapter
        if adapter is not None:
            image_embedding = adapter(image_embedding)

    return image_embedding

def predict_location(image_path: str, category_filter: str = None, top_k: int = 10):
    """
    Predicts location candidates from an image using multi-scale TTA and ResidualAdapter.
    Optionally filter by category: e.g. 'Global', 'India - State/UT', 'India - City/Hub', 'Kerala - Micro-Region'
    """
    image = Image.open(image_path).convert("RGB")
    image_embedding = extract_visual_representation(image)

    # Filter candidates if requested
    if category_filter:
        indices = [i for i, loc in enumerate(locations) if loc.get("category") == category_filter]
        active_embeddings = text_embeddings[indices]
        active_locations = [locations[i] for i in indices]
    else:
        active_embeddings = text_embeddings
        active_locations = locations

    with torch.no_grad():
        # Baseline text cosine similarities: [1, 768] @ [768, N] -> [N]
        similarity_scores = torch.matmul(image_embedding, active_embeddings.T).squeeze(0)

        # Strict visual correction matching (cos_sim >= 0.92)
        if corrections:
            for item in corrections:
                corr_emb = item["embedding"].to(image_embedding.device)
                cos_sim = torch.dot(image_embedding.squeeze(0), corr_emb.squeeze(0)).item()
                if cos_sim >= 0.92:
                    corr_target = item["location_name"].strip().lower()
                    for idx, loc in enumerate(active_locations):
                        if loc["name"].strip().lower() == corr_target:
                            similarity_scores[idx] += (cos_sim - 0.90) * 15.0 + 1.2
                            break

        # Temperature-scaled Softmax for well-calibrated confidence distribution
        probabilities = torch.softmax(similarity_scores * 35.0, dim=-1).tolist()

    ranked_results = []
    for loc, prob in zip(active_locations, probabilities):
        lat = loc.get("lat", 0.0)
        lon = loc.get("lon", 0.0)
        name = loc["name"]
        query = urllib.parse.quote(f"{name}, {loc.get('country', '')}")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        earth_url = f"https://earth.google.com/web/search/{query}"
        streetview_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"

        ranked_results.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "country": loc.get("country", ""),
            "region": loc.get("region", ""),
            "category": loc.get("category", ""),
            "driving_side": loc.get("driving_side", "Unknown"),
            "confidence": prob,
            "maps_url": maps_url,
            "earth_url": earth_url,
            "streetview_url": streetview_url
        })

    ranked_results.sort(key=lambda x: x["confidence"], reverse=True)
    return ranked_results[:top_k]

def generate_heatmap(results, output_filename="world_heatmap.html"):
    if not results:
        return
    top_pred = results[0]
    world_map = folium.Map(location=[top_pred["lat"], top_pred["lon"]], zoom_start=4, tiles="OpenStreetMap")

    heat_data = [[item["lat"], item["lon"], item["confidence"]] for item in results]
    HeatMap(heat_data, radius=30, blur=20, max_zoom=12).add_to(world_map)

    for i, pred in enumerate(results[:5], start=1):
        popup_html = f"""<b>#{i} {pred['name']}</b> ({pred['confidence']*100:.1f}%)<br>
Driving: {pred['driving_side']}<br>
<a href="{pred['maps_url']}" target="_blank">Google Maps</a> | 
<a href="{pred['earth_url']}" target="_blank">Google Earth</a>"""
        folium.Marker(
            location=[pred["lat"], pred["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red" if i == 1 else "blue", icon="info-sign")
        ).add_to(world_map)

    world_map.save(output_filename)
    print(f"Heatmap saved to '{output_filename}'.")

if __name__ == "__main__":
    test_image = "test.jpg"
    if not os.path.exists(test_image):
        # Fallback to an image in Imgs/ if test.jpg doesn't exist
        for sample in ["Imgs/kerala_munnar.jpg", "Imgs/japan_tokyo.jpg", "Imgs/france_paris.jpg"]:
            if os.path.exists(sample):
                test_image = sample
                break

    print(f"\nRunning global inference on '{test_image}' across {len(locations)} locations...")
    try:
        ranked = predict_location(test_image, top_k=10)
        print("\n--- Top 5 AI Location Predictions ---")
        for i, pred in enumerate(ranked[:5], start=1):
            driving = f"[Driving: {pred['driving_side']}]" if pred['driving_side'] != "Unknown" else ""
            print(f"{i}. {pred['name']} | Category: {pred['category']} {driving}")
            print(f"   Confidence: {pred['confidence']*100:.2f}%")
            print(f"   Google Maps:  {pred['maps_url']}")
            print(f"   Google Earth: {pred['earth_url']}\n")
        generate_heatmap(ranked)
    except FileNotFoundError:
        print(f"Could not find '{test_image}'. Please put an image named 'test.jpg' in the project folder to test.")