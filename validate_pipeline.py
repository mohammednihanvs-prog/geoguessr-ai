"""
Team Validation Script for GeoGuessr AI
Run this before submitting a Pull Request to ensure your changes are healthy:
    python validate_pipeline.py
"""

import os
import sys
from collections import Counter
from PIL import Image
import torch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_locations():
    print("\n--- 1. Checking Locations Database ---")
    if not os.path.exists("locations.py"):
        print("❌ locations.py not found!")
        return False
    try:
        import locations
        locs = locations.LOCATIONS
        print(f"Total locations indexed: {len(locs)}")
        
        # Check duplicates
        names = [l["name"].strip().lower() for l in locs]
        counts = Counter(names)
        dups = [n for n, c in counts.items() if c > 1]
        if dups:
            print(f"❌ Found duplicate locations in locations.py: {dups}")
            return False
        else:
            print("✅ Zero duplicate locations in locations.py.")
        
        # Check required fields
        for l in locs:
            for req in ["name", "lat", "lon", "country", "category"]:
                if req not in l:
                    print(f"❌ Location missing required key '{req}': {l.get('name')}")
                    return False
        print("✅ All locations have required metadata (name, lat, lon, country, category).")
        return True
    except Exception as e:
        print(f"❌ Failed to import or parse locations.py: {e}")
        return False

def check_images():
    print("\n--- 2. Checking Image Dataset ---")
    if not os.path.exists("Imgs"):
        print("❌ Imgs directory not found!")
        return False
    img_files = [f for f in os.listdir("Imgs") if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    print(f"Total image files in Imgs/: {len(img_files)}")
    corrupted = []
    for f in img_files:
        p = os.path.join("Imgs", f)
        try:
            with Image.open(p) as img:
                img.verify()
        except Exception:
            corrupted.append(f)
    if corrupted:
        print(f"❌ Corrupted images found: {corrupted}")
        return False
    print("✅ All images in Imgs/ are valid and non-corrupted.")
    return True

def check_model_and_caches():
    print("\n--- 3. Checking Model Artifacts & Caches ---")
    ok = True
    for cache_f in ["embeddings_cache.pt", "clip_adapter.pt"]:
        if not os.path.exists(cache_f):
            print(f"⚠️ Warning: '{cache_f}' is missing. Run cache_embeddings.py or train_adapter.py.")
            ok = False
        else:
            size_mb = os.path.getsize(cache_f) / (1024 * 1024)
            print(f"✅ Found '{cache_f}' ({size_mb:.2f} MB).")
    return ok

def check_apps():
    print("\n--- 4. Checking Code Syntax ---")
    import py_compile
    for py_file in ["app.py", "predict.py", "train_adapter.py", "cache_embeddings.py"]:
        if os.path.exists(py_file):
            try:
                py_compile.compile(py_file, doraise=True)
                print(f"✅ {py_file} compiles cleanly.")
            except Exception as e:
                print(f"❌ Syntax error in {py_file}: {e}")
                return False
    return True

if __name__ == "__main__":
    print("==============================================")
    print("   GeoGuessr AI Team Pre-Flight Verification   ")
    print("==============================================")
    res_loc = check_locations()
    res_img = check_images()
    res_mod = check_model_and_caches()
    res_app = check_apps()

    print("\n==============================================")
    if res_loc and res_img and res_mod and res_app:
        print("🎉 ALL CHECKS PASSED! Ready to commit and push.")
        sys.exit(0)
    else:
        print("⚠️ Some checks failed. Please address them before pushing.")
        sys.exit(1)
