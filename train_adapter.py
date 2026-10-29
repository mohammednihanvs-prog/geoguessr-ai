import os
import sys
import glob
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from locations import LOCATIONS

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ADAPTER_WEIGHTS_FILE = "clip_adapter.pt"
CACHE_FILE = "embeddings_cache.pt"
IMAGE_DIR = "Imgs"

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
        # Identity initialization: zero-init final layer
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)

    def forward(self, x):
        residual = self.net(x)
        out = self.alpha * x + (1.0 - self.alpha) * residual
        return out / out.norm(dim=-1, keepdim=True)

def resolve_location_index(filename, locations):
    base = os.path.splitext(filename)[0]
    tokens = [t.lower() for t in base.replace("-", "_").split("_") if t]

    best_idx = 0
    best_score = 0
    for idx, loc in enumerate(locations):
        loc_name_lower = loc["name"].lower()
        score = sum(1 for tok in tokens if tok in loc_name_lower)
        if score > best_score:
            best_score = score
            best_idx = idx

    return best_idx

def train_adapter(epochs=35, lr=2e-3, bottleneck=256, alpha=0.5):
    print("=== Training StreetCLIP Residual Vision Adapter ===")
    
    # 1. Load cached location embeddings
    print(f"Loading cached text embeddings from '{CACHE_FILE}'...")
    cache_data = torch.load(CACHE_FILE, weights_only=False)
    text_embeddings = cache_data["embeddings"] # [201, 768]
    locations = cache_data["locations"]
    print(f"Indexed locations: {len(locations)} with embedding dim: {text_embeddings.shape[1]}")

    # 2. Find images
    extensions = ("*.jpg", "*.jpeg", "*.png")
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
    image_paths = [p for p in image_paths if not os.path.basename(p).startswith("test")]
    print(f"Found {len(image_paths)} training images in '{IMAGE_DIR}/'.")

    # 3. Load pre-trained model for feature extraction
    print("Loading pre-trained StreetCLIP model for frozen feature extraction...")
    model_name = "geolocal/StreetCLIP"
    try:
        processor = CLIPProcessor.from_pretrained(model_name, local_files_only=True)
        model = CLIPModel.from_pretrained(model_name, local_files_only=True)
    except Exception:
        processor = CLIPProcessor.from_pretrained(model_name)
        model = CLIPModel.from_pretrained(model_name)

    model.eval()

    # Pre-extract normalized image features
    print("Pre-extracting image representations (caching for fast training)...")
    feats_list = []
    targets_list = []

    for idx, path in enumerate(image_paths):
        fname = os.path.basename(path)
        loc_idx = resolve_location_index(fname, locations)
        
        try:
            im = Image.open(path).convert("RGB")
            inp = processor(images=im, return_tensors="pt")
            with torch.no_grad():
                out = model.get_image_features(pixel_values=inp["pixel_values"])
                raw = out.pooler_output if hasattr(out, "pooler_output") else out
                norm = raw / raw.norm(dim=-1, keepdim=True)
                feats_list.append(norm.squeeze(0))
                targets_list.append(loc_idx)
        except Exception as e:
            print(f"  Warning: failed on {fname}: {e}")

    X = torch.stack(feats_list) # [N, 768]
    Y = torch.tensor(targets_list, dtype=torch.long) # [N]
    print(f"Ready with training tensor X: {X.shape}, Y: {Y.shape}")

    # 4. Instantiate Adapter
    adapter = ResidualAdapter(dim=X.shape[1], bottleneck=bottleneck, alpha=alpha)
    optimizer = AdamW(adapter.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)
    loss_fn = nn.CrossEntropyLoss()

    # Initial zero-shot accuracy before training
    adapter.eval()
    with torch.no_grad():
        out_init = adapter(X)
        logits_init = (out_init @ text_embeddings.T) * 35.0
        preds_init = torch.argmax(logits_init, dim=-1)
        acc_init = (preds_init == Y).float().mean().item() * 100.0
        print(f"\nInitial Zero-Shot Top-1 Accuracy: {acc_init:.2f}%\n")

    # 5. Training loop
    adapter.train()
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        out_feats = adapter(X)
        logits = (out_feats @ text_embeddings.T) * 35.0
        loss = loss_fn(logits, Y)
        loss.backward()
        optimizer.step()
        scheduler.step()

        preds = torch.argmax(logits, dim=-1)
        acc = (preds == Y).float().mean().item() * 100.0

        if epoch % 5 == 0 or epoch == 1 or epoch == epochs:
            print(f"Epoch {epoch:2d}/{epochs:2d} | Loss: {loss.item():.4f} | Training Top-1 Accuracy: {acc:.2f}%")

    # 6. Save trained adapter
    torch.save(adapter.state_dict(), ADAPTER_WEIGHTS_FILE)
    print(f"\nSuccessfully saved trained Residual Adapter to '{ADAPTER_WEIGHTS_FILE}'!")
    print(f"Final Accuracy: {acc:.2f}% (Improved from {acc_init:.2f}%!)")

if __name__ == "__main__":
    train_adapter()
