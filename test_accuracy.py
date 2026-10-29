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
top1_correct = 0
top3_correct = 0
total = 0

for name in test_imgs:
    path = os.path.join("Imgs", name)
    if os.path.exists(path):
        res = predict_location(path, top_k=3)
        total += 1
        print(f"\nTarget File: {name}")
        for i, r in enumerate(res, 1):
            print(f"  {i}. {r['name']} - {r['confidence']*100:.2f}%")

        # Verify whether top prediction corresponds to the target scene
        base = os.path.splitext(name)[0].lower()
        key_tokens = [t for t in base.replace("-", "_").split("_") if t]

        top_name = res[0]["name"].lower()
        if any(tok in top_name for tok in key_tokens[:2]):
            top1_correct += 1
            top3_correct += 1
        elif any(any(tok in r["name"].lower() for tok in key_tokens[:2]) for r in res):
            top3_correct += 1

if total > 0:
    print(f"\n==========================================")
    print(f"Accuracy Benchmark Summary ({total} test scenes):")
    print(f"Top-1 Accuracy: {top1_correct}/{total} ({top1_correct/total*100:.2f}%)")
    print(f"Top-3 Accuracy: {top3_correct}/{total} ({top3_correct/total*100:.2f}%)")
    print(f"==========================================")
