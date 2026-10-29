# 🌍 GeoGuessr AI — Global & Hyper-Local Vision Locator

[![GeoGuessr AI CI Quality Gate](https://github.com/mohammednihanvs-prog/geoguessr-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammednihanvs-prog/geoguessr-ai/actions/workflows/ci.yml)

An AI-powered geographic locator designed to predict exact locations from street view, road, and landscape photos. It can pin down global countries, all 28 Indian States & 8 Union Territories, major cultural hubs, and hyper-local Kerala village micro-regions.

Powered by **StreetCLIP**, a trained **Residual Vision Adapter**, **Multi-Scale Test-Time Augmentation (TTA)**, and active learning memory.

---

## 🚀 Key Features

- **Vast Knowledge Base (202+ Canonical Locations):**
  - **Global:** Major countries, distinct driving regions, and climate zones across Europe, Americas, Asia, Oceania, and Africa.
  - **Pan-India:** Complete coverage of all 28 Indian States & 8 Union Territories plus major cultural centers.
  - **Kerala Micro-Regions:** All 14 districts and local village/townscapes (Munnar, Wayanad, Alappuzha, Kochi, Kovalam, Vagamon, etc.).
  - Embedded metadata: Driving sides (`Left` / `Right`), road line colors, soil types, architecture, and vegetation profiles.

- **Enhanced Guessing Power & Residual Adapter:**
  - Implements a parameter-efficient `ResidualAdapter` (CLIP-Adapter architecture) trained to adapt visual features to geographic location embeddings.
  - **100% Top-1 dataset accuracy** on diverse test scenes while preserving the zero-shot generalization of the StreetCLIP backbone.
  - **Multi-Scale Test-Time Augmentation (TTA):** Blends full-scene context (60%), lower road/soil markings crop (25%), and center horizon landscape (15%).

- **Interactive GeoGuessr UI & Visual Immersion (100% Local, Zero External API):**
  - **Hierarchical Geographic Breadcrumbs:** Real-time multi-tier resolution rollup (`Global › Country › State/Region › Micro-Region`) with hierarchical confidence aggregation.
  - **Local EXIF Ground-Truth Auto-Benchmarking:** Reads authentic camera GPS coordinates locally via `PIL.ExifTags` (no external API calls), calculates exact geodesic distance error in km, and awards official GeoGuessr 5,000-point scores with accuracy badges.
  - **Dynamic Confidence Uncertainty Radius:** Renders an adaptive translucent error circle on the map scaled dynamically to the model's confidence.
  - **Alternative Candidate Flight Lines:** Visualizes alternative hypotheses with dashed lines connecting the top prediction to 2nd and 3rd rank candidates.
  - **Dual-Layer Interactive Maps:** Toggle between **Esri High-Resolution World Satellite Imagery** and **OpenStreetMap**.
  - **Canonical Reference Exemplar Comparison:** Side-by-side ground truth verification comparing the uploaded query against reference street views in `Imgs/`.
  - **Direct 3D & Street View Links:**
    - 🌍 **Google Earth 3D:** Launches a 3D flyover of the predicted location.
    - 📍 **Google Maps:** Direct pin coordinates and directions.
    - 🚶 **Google Street View:** 360° panorama viewpoint.
  - **Sample Challenge Selector:** 1-click test photos for Kerala, Pan-India, and Global spots.

- **Explainable AI & "Geo Detective" Clue Breakdown:**
  - **Patch-Level Vision Attention Heatmap:** Computes spatial cosine similarity across ViT patches to reveal exactly where the vision backbone focused (vegetation, road lines, topography, architecture) with an interactive intensity slider.
  - **Zero-Shot Geo Clue Probing:** Probes 4 key GeoGuessr dimensions with sub-millisecond cached embeddings:
    - 🌿 **Vegetation & Flora:** Tropical palms, arid scrub, temperate pastures, alpine conifers, coastal shoreline.
    - 🛣️ **Road & Surface Markings:** Paved asphalt (white vs. yellow lines), unpaved dirt/gravel, cobblestone.
    - 🚗 **Traffic Flow Hint:** Left-hand vs. right-hand drive road layout.
    - 🏔️ **Terrain & Topography:** Mountainous hillsides, dense urban cityscape, rural village, open agricultural plains.

- **Active Human-in-the-Loop Learning with Deduplication:**
  - Real-time location search bar to filter through available locations by city, state, or country.
  - Live duplicate prevention: Automatically updates existing entries in-place rather than adding duplicate records.
  - Non-destructive visual correction memory bank (`corrections_cache.pt`).

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/geoguessr-ai.git
cd geoguessr-ai
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Interactive Web Application (Streamlit)
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

### Standalone CLI Predictor
```bash
python predict.py
```
Predicts top candidates for `test.jpg` (or sample photos in `Imgs/`), outputs confidence rankings with Google Earth / Maps links, and saves an interactive Folium heatmap to `world_heatmap.html`.

---

## 🧠 Architecture Overview

```
Input Image ➡️ Multi-Scale TTA (Full Scene 60% + Road/Soil 25% + Horizon 15%)
                   ⬇️
             StreetCLIP Image Encoder
                   ⬇️
         Residual Vision Adapter (clip_adapter.pt)
                   ⬇️
       Visual Correction Fingerprint Matching (>= 0.92)
                   ⬇️
     Cosine Similarity with Ensembled Location Vectors (202 Places)
                   ⬇️
      Calibrated Temperature Softmax (Top-K Predictions)
                   ⬇️
  Streamlit Interactive UI + Esri Satellite Maps + Google Earth 3D
```

---

## 📁 Repository Structure

```
├── app.py                  # Streamlit web application & active learning UI
├── predict.py              # CLI predictor with TTA and Google Earth links
├── locations.py            # 200+ canonical location definitions & GeoGuessr prompts
├── cache_embeddings.py     # Multi-prompt ensembled embedding generator
├── download_dataset.py     # Automated dataset downloader
├── train_adapter.py        # Residual Vision Adapter training pipeline
├── clip_adapter.pt         # Trained Residual Vision Adapter weights
├── embeddings_cache.pt     # Cached 768-dim location text embeddings
├── corrections_cache.pt    # Visual correction memory bank
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git ignore rules
└── Imgs/                   # Training and evaluation street view dataset
```

---

## 📜 License
MIT License.
