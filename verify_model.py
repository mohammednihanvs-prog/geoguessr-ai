import torch
from transformers import CLIPModel, CLIPProcessor
from PIL import Image

print("Loading geolocal/StreetCLIP model...")
model_name = "geolocal/StreetCLIP"

processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)

print("Model successfully loaded!")

# 1. Create a dummy image (224x224 RGB image)
dummy_image = Image.new("RGB", (224, 224), color=(100, 150, 200))

# 2. Define sample candidate locations
candidate_locations = ["a street in Tokyo, Japan", "a street in Paris, France"]

# 3. Preprocess inputs
inputs = processor(
    text=candidate_locations,
    images=dummy_image,
    return_tensors="pt",
    padding=True
)

print(f"Preprocessed Image Tensor Shape: {inputs['pixel_values'].shape}")
print(f"Preprocessed Text Tensor Shape:  {inputs['input_ids'].shape}")

# 4. Run inference through the model
with torch.no_grad():
    image_outputs = model.get_image_features(pixel_values=inputs['pixel_values'])
    text_outputs = model.get_text_features(input_ids=inputs['input_ids'])

# Extract raw tensor if wrapped in a BaseModelOutput object
image_features = image_outputs.pooler_output if hasattr(image_outputs, 'pooler_output') else image_outputs
text_features = text_outputs.pooler_output if hasattr(text_outputs, 'pooler_output') else text_outputs

print(f"Image Embedding Vector Shape:    {image_features.shape}")
print(f"Text Embedding Vectors Shape:    {text_features.shape}")