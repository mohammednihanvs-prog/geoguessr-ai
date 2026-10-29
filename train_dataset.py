import os
import sys
import glob
import argparse
import torch
from torch.optim import AdamW
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from locations import LOCATIONS

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODEL_WEIGHTS_FILE = "fine_tuned_streetclip.pt"
CACHE_FILE = "embeddings_cache.pt"
IMAGE_DIR = "Imgs"

def resolve_location_for_filename(filename, locations):
    """
    Matches an image filename to the most relevant location entry in LOCATIONS.
    Filename example: 'Munnar_Idukki_Kerala_India.jpg'
    """
    base = os.path.splitext(filename)[0]
    tokens = [t.lower() for t in base.replace("-", "_").split("_") if t]

    best_loc = None
    best_score = 0

    for loc in locations:
        loc_name_lower = loc["name"].lower()
        score = sum(1 for tok in tokens if tok in loc_name_lower)
        if score > best_score:
            best_score = score
            best_loc = loc

    # If good match found
    if best_loc and best_score >= 1:
        prompt = best_loc.get("prompt", f"a street view photo in {best_loc['name']}")
        return best_loc["name"], prompt

    # Fallback to reconstructing title from filename
    clean_name = base.replace("_", " ")
    prompt = f"a street view photo in {clean_name}"
    return clean_name, prompt

def train_on_images(epochs=1, lr=5e-6, dry_run=False):
    # Find all images in Imgs/
    extensions = ("*.jpg", "*.jpeg", "*.png")
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))

    # Exclude generic test files
    image_paths = [p for p in image_paths if not os.path.basename(p).startswith("test")]

    print(f"=== Found {len(image_paths)} Training Images in '{IMAGE_DIR}/' ===")
    if not image_paths:
        print("No images found to train on.")
        return

    # Print matching summary
    samples = []
    for path in image_paths:
        fname = os.path.basename(path)
        loc_name, prompt = resolve_location_for_filename(fname, LOCATIONS)
        samples.append((path, loc_name, prompt))

    print("\n--- Training Plan Preview ---")
    for idx, (path, loc_name, prompt) in enumerate(samples[:8], 1):
        print(f"{idx}. {os.path.basename(path)}")
        print(f"   Target: {loc_name}")
        print(f"   Prompt: {prompt[:80]}...\n")
    if len(samples) > 8:
        print(f"... and {len(samples) - 8} more images.\n")

    if dry_run:
        print("[Dry Run] Finished inspection. No weights were modified.")
        return

    # Load StreetCLIP model
    print("Loading StreetCLIP model for training...")
    model_name = "geolocal/StreetCLIP"
    try:
        processor = CLIPProcessor.from_pretrained(model_name, local_files_only=True)
        model = CLIPModel.from_pretrained(model_name, local_files_only=True)
    except Exception:
        processor = CLIPProcessor.from_pretrained(model_name)
        model = CLIPModel.from_pretrained(model_name)

    if os.path.exists(MODEL_WEIGHTS_FILE):
        print(f"Resuming from existing checkpoint '{MODEL_WEIGHTS_FILE}'...")
        state_dict = torch.load(MODEL_WEIGHTS_FILE, map_location="cpu", weights_only=True)
        model.load_state_dict(state_dict)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.train()

    optimizer = AdamW(model.parameters(), lr=lr)

    print(f"\n--- Starting Fine-Tuning ({epochs} epoch(s), lr={lr}, device={device}) ---")
    for epoch in range(1, epochs + 1):
        running_loss = 0.0
        success_count = 0

        for i, (path, loc_name, prompt) in enumerate(samples, 1):
            try:
                img = Image.open(path).convert("RGB")
                inputs = processor(
                    text=[prompt],
                    images=img,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=77
                ).to(device)

                optimizer.zero_grad()
                outputs = model(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    return_loss=True
                )
                loss = outputs.loss
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                success_count += 1
                print(f"[{epoch}/{epochs}][{i}/{len(samples)}] {os.path.basename(path)[:35]:35s} | Loss: {loss.item():.4f}")
            except Exception as e:
                print(f"[{epoch}/{epochs}][{i}/{len(samples)}] Failed on {os.path.basename(path)}: {e}")

        avg_loss = running_loss / max(success_count, 1)
        print(f"\nEpoch {epoch}/{epochs} Complete. Average Loss: {avg_loss:.4f}\n")

    # Save fine-tuned checkpoint
    print(f"Saving updated model weights to '{MODEL_WEIGHTS_FILE}'...")
    torch.save(model.state_dict(), MODEL_WEIGHTS_FILE)
    print("Checkpoint saved successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch fine-tune StreetCLIP on dataset images in Imgs/")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=5e-6, help="Learning rate")
    parser.add_argument("--dry-run", action="store_true", help="Inspect matching without running training")
    args = parser.parse_args()

    train_on_images(epochs=args.epochs, lr=args.lr, dry_run=args.dry_run)
