import os
import sys
from predict import predict_location

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

test_imgs = [
    "Munnar_Idukki_Kerala_India.jpg",
    "Fort_Kochi_Ernakulam_Kerala_India.jpg",
    "Tokyo_Shinjuku_Japan.jpg",
    "Paris_Haussmann_Boulevard_France.jpg",
    "London_Westminster_United_Kingdom.jpg",
    "New_York_City_Manhattan_United_States.jpg",
    "Amsterdam_Canal_Netherlands.jpg",
    "Varanasi_Ghats_Uttar_Pradesh_India.jpg"
]

print("=== Evaluating Predictions on Real Dataset Images ===")
for name in test_imgs:
    path = os.path.join("Imgs", name)
    if os.path.exists(path):
        res = predict_location(path, top_k=3)
        print(f"\nTarget File: {name}")
        for i, r in enumerate(res, 1):
            print(f"  {i}. {r['name']} - {r['confidence']*100:.2f}%")
