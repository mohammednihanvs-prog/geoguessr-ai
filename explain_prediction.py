import os
import sys
import torch
import numpy as np
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from torch import nn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CACHE_FILE = "embeddings_cache.pt"
ADAPTER_FILE = "clip_adapter.pt"

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

GEO_CLUE_DEFINITIONS = [
    (
        "🌿 Vegetation & Flora",
        [
            ("Tropical palms & lush foliage", "tropical coconut palms banana trees lush green monsoon foliage"),
            ("Arid scrub & desert sand", "arid desert landscape dry red sand sparse scrub dry rocky terrain"),
            ("Temperate meadows & deciduous woods", "temperate green agricultural fields deciduous forest pastures"),
            ("Alpine conifers & snow peaks", "alpine evergreen pine conifers rugged mountain peaks cool climate"),
            ("Coastal shoreline & ocean water", "coastal beach shoreline ocean waves maritime coastline")
        ]
    ),
    (
        "🛣️ Road & Surface",
        [
            ("Asphalt with white markings", "paved asphalt road with white pavement line markings"),
            ("Asphalt with yellow markings", "paved asphalt road with yellow pavement line markings"),
            ("Unpaved dirt / gravel track", "unpaved dirt gravel rural country road or mud trail"),
            ("Historic stone / cobblestone", "historic cobblestone stone paved ancient alley street")
        ]
    ),
    (
        "🚗 Traffic Flow Hint",
        [
            ("Left-hand drive layout", "left-hand drive traffic driving on the left side of the road"),
            ("Right-hand drive layout", "right-hand drive traffic driving on the right side of the road")
        ]
    ),
    (
        "🏔️ Terrain & Topography",
        [
            ("Mountainous winding hillside", "mountainous terrain winding hillside roads tea estates hills"),
            ("Dense urban commercial cityscape", "dense multi-story modern urban cityscape commercial downtown"),
            ("Rural village settlement", "quiet rural village countryside settlement with small houses"),
            ("Flat open agricultural plains", "flat agricultural crop plains open landscape wide horizon")
        ]
    )
]

def analyze_image(image_path="test.jpg"):
    cache = torch.load(CACHE_FILE, weights_only=False)
    text_embeddings = cache["embeddings"]
    locations = cache["locations"]

    model_name = "geolocal/StreetCLIP"
    processor = CLIPProcessor.from_pretrained(model_name)
    model = CLIPModel.from_pretrained(model_name)
    model.eval()

    adapter = ResidualAdapter()
    if os.path.exists(ADAPTER_FILE):
        adapter.load_state_dict(torch.load(ADAPTER_FILE, weights_only=False))
    adapter.eval()

    image = Image.open(image_path).convert("RGB")
    w, h = image.size

    # Crops: Full context (45%), Road/Ground (25%), Roadside/Infrastructure (15%), Horizon (15%)
    crop_ground = image.crop((0, int(h * 0.45), w, h))
    crop_side = image.crop((0, int(h * 0.20), int(w * 0.45), h))
    crop_horizon = image.crop((0, 0, w, int(h * 0.55)))

    crops = [image, crop_ground, crop_side, crop_horizon]
    weights = [0.45, 0.25, 0.15, 0.15]

    crop_embeddings = []
    with torch.no_grad():
        for c in crops:
            inputs = processor(images=c, return_tensors="pt")
            out = model.get_image_features(pixel_values=inputs["pixel_values"])
            feat = out.pooler_output if hasattr(out, "pooler_output") else out
            norm_feat = feat / feat.norm(dim=-1, keepdim=True)
            crop_embeddings.append(norm_feat)

    # Multi-crop fusion
    fused = sum(w * e for w, e in zip(weights, crop_embeddings))
    fused = fused / fused.norm(dim=-1, keepdim=True)

    # Residual Adapter transformation
    adapted = adapter(fused)
    adapted = adapted / adapted.norm(dim=-1, keepdim=True)

    # Geo Clue Probing
    clue_findings = []
    for cat_name, items in GEO_CLUE_DEFINITIONS:
        prompts = [it[1] for it in items]
        t_in = processor(text=prompts, return_tensors="pt", padding=True, truncation=True, max_length=77)
        with torch.no_grad():
            t_out = model.get_text_features(input_ids=t_in["input_ids"])
            t_raw = t_out.pooler_output if hasattr(t_out, "pooler_output") else t_out
            t_norm = t_raw / t_raw.norm(dim=-1, keepdim=True)
        scores = torch.matmul(t_norm, fused.squeeze(0))
        probs = torch.softmax(scores * 18.0, dim=-1).tolist()
        best_idx = int(scores.argmax().item())
        clue_findings.append({
            "category": cat_name,
            "label": items[best_idx][0],
            "confidence": probs[best_idx] * 100,
            "all_scores": list(zip([it[0] for it in items], [p * 100 for p in probs]))
        })

    # Cosine similarities
    sims = torch.matmul(text_embeddings, adapted.squeeze(0))

    # Evidence booster calculation
    base_scores = sims.clone()
    boosted_scores = sims.clone()

    top_traffic = clue_findings[2]["label"]
    top_veg = clue_findings[0]["label"]
    top_road = clue_findings[1]["label"]

    for i, loc in enumerate(locations):
        loc_prompt = loc.get("prompt", "").lower()
        loc_driving = loc.get("driving_side", "Unknown")

        if top_traffic == "Left-hand drive layout" and loc_driving == "Left":
            boosted_scores[i] += 0.20
        elif top_traffic == "Right-hand drive layout" and loc_driving == "Right":
            boosted_scores[i] += 0.20

        if "tropical" in top_veg.lower() and ("tropical" in loc_prompt or "palm" in loc_prompt or "backwater" in loc_prompt):
            boosted_scores[i] += 0.15
        elif "arid" in top_veg.lower() and ("desert" in loc_prompt or "arid" in loc_prompt or "sand" in loc_prompt):
            boosted_scores[i] += 0.15

        if "unpaved" in top_road.lower() and ("unpaved" in loc_prompt or "dirt" in loc_prompt or "gravel" in loc_prompt):
            boosted_scores[i] += 0.10

    # Softmax probabilities
    probs_boosted = torch.softmax(boosted_scores * 22.0, dim=0)
    top_k = torch.topk(probs_boosted, 5)

    print("=== EXPLANATION BREAKDOWN FOR test.jpg ===")
    print("\n1. Detected Visual Cues & Probes:")
    for c in clue_findings:
        print(f"  - {c['category']}: {c['label']} ({c['confidence']:.2f}%)")
        for sub_lbl, sub_p in c["all_scores"]:
            print(f"      • {sub_lbl}: {sub_p:.2f}%")

    print("\n2. Top 5 Predicted Locations:")
    for rank, (idx, prob) in enumerate(zip(top_k.indices.tolist(), top_k.values.tolist())):
        loc = locations[idx]
        raw_sim = base_scores[idx].item()
        boost = boosted_scores[idx].item() - raw_sim
        print(f"  Rank {rank+1}: {loc['name']}")
        print(f"      Country: {loc.get('country')} | Category: {loc.get('category')} | Driving: {loc.get('driving_side')}")
        print(f"      Raw StreetCLIP Cosine Sim: {raw_sim:.4f}")
        print(f"      Micro-Clue Evidence Boost: +{boost:.4f}")
        print(f"      Final Softmax Confidence:  {prob * 100:.2f}%")
        print(f"      Prompt Profile: {loc.get('prompt')}")

if __name__ == "__main__":
    analyze_image("test.jpg")
