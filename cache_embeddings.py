import torch
from transformers import CLIPModel, CLIPProcessor
from locations import LOCATIONS

print("Loading geolocal/StreetCLIP model...")
model_name = "geolocal/StreetCLIP"

processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)
model.eval()

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"Running on device: {device}")
print(f"Total candidate locations to index: {len(LOCATIONS)}")

# Helper to encode a list of text prompts in batches
def encode_prompts(prompt_list, batch_size=32):
    all_embeddings = []
    total = len(prompt_list)
    for i in range(0, total, batch_size):
        batch = prompt_list[i : i + batch_size]
        inputs = processor(
            text=batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(device)
        with torch.no_grad():
            outputs = model.get_text_features(input_ids=inputs["input_ids"])
            features = outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
            # Normalize each vector
            normalized = features / features.norm(dim=-1, keepdim=True)
            all_embeddings.append(normalized.cpu())
        print(f"  Processed {min(i + batch_size, total)}/{total} prompts...", end="\r")
    print()
    return torch.cat(all_embeddings, dim=0)

# Build ensembled prompts for each location:
# 1. Rich visual descriptor prompt (clues, soil, architecture, driving side)
# 2. Canonical street view prompt
# 3. Canonical landscape / road photo prompt
print("Encoding Visual Descriptor Prompts (Set 1)...")
prompts_visual = [loc.get("prompt", f"a street photo in {loc['name']}") for loc in LOCATIONS]
embeds_visual = encode_prompts(prompts_visual)

print("Encoding Canonical Place Prompts (Set 2)...")
prompts_canonical = [f"a street view photo in {loc['name']}" for loc in LOCATIONS]
embeds_canonical = encode_prompts(prompts_canonical)

print("Encoding Geographic Context Prompts (Set 3)...")
prompts_geo = [f"a photo taken in {loc['name']}, {loc.get('country', '')}" for loc in LOCATIONS]
embeds_geo = encode_prompts(prompts_geo)

# Ensemble: Average normalized vectors and re-normalize
print("Ensembling embeddings...")
# Weighting: 50% visual features, 30% canonical name, 20% country context
combined = 0.50 * embeds_visual + 0.30 * embeds_canonical + 0.20 * embeds_geo
final_embeddings = combined / combined.norm(dim=-1, keepdim=True)

# Save to cache file
output_cache = "embeddings_cache.pt"
torch.save(
    {
        "embeddings": final_embeddings,
        "locations": LOCATIONS
    },
    output_cache
)

print(f"\nSuccessfully built and saved cache to '{output_cache}'!")
print(f"Cached tensor shape: {final_embeddings.shape}")
print(f"Indexed locations: {len(LOCATIONS)}")