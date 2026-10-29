# 🌍 GeoGuessr AI — Global & Hyper-Local Vision Locator

[![GeoGuessr AI CI Quality Gate](https://github.com/mohammednihanvs-prog/geoguessr-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammednihanvs-prog/geoguessr-ai/actions/workflows/ci.yml)

An AI-powered geographic locator designed to predict exact locations from street view, road, and landscape photos. It can pin down global countries, all 28 Indian States & 8 Union Territories, major cultural hubs, and hyper-local Kerala village micro-regions.

Powered by **StreetCLIP**, a trained **Residual Vision Adapter**, **Multi-Scale Test-Time Augmentation (TTA)**, and active learning memory.

---

## 🚀 Key Features

- **Massive Knowledge Base (475+ Canonical Locations across 114+ Countries):**
  - **Global (114+ Countries):** Comprehensive world coverage across all 6 inhabited continents (Europe, Americas, Asia, Africa, Oceania) with distinct driving regions, climate zones, and iconic cities.
  - **Pan-India:** Complete coverage of all 28 Indian States & 8 Union Territories plus major cultural centers and tier-1/2 hubs.
  - **Dense Kerala Micro-Regions & Remote Villages (100+ villages across all 14 Districts):** Deep coverage of high-ranges (Vattavada, Kanthalloor, Suryanelli, Chinnakanal, Mankulam, Marayoor, Kolukkumalai), Wayanad hills & forests (Meppadi, Thirunelly, Pulpally, Banasura, Kuruvadweep), Kuttanad & backwaters (Pulinkunnu, Kavalam, Kainakkary, Thakazhy, Edathua, Champakulam), South & Central forests/hills (Gavi, Konni, Thenmala, Arippa, Bonacaud, Ponmudi, Malakkappara, Vazhachal, Ilaveezhapoonchira, Aymanam), Malabar & North Kerala (Kollengode, Attappadi, Karuvarakundu, Kakkadampoyil, Nilambur, Kakkayam, Thusharagiri, Madayipara, Paithalmala, Ranipuram, Kottancheri, Nileshwaram, Badiyadka), and coastal/lagoon heritage (Kumbalangi, Fort Kochi, Varkala, Kovalam, Bekal, Dharmadam).
  - Embedded metadata: Driving sides (`Left` / `Right`), road line colors, soil types, architecture, bollards, poles, and vegetation profiles.
  - **104 Reference Images Dataset (`Imgs/`):** High-resolution canonical reference street views, village pathways, tea gardens, paddy fields, laterite paths, and authentic random rural road shots.

- **Enhanced Guessing Power, Micro-Clue Fusion & Residual Adapter:**
  - **Multi-Crop Micro-Cue TTA:** 4-crop feature extraction fusing full scene (45%), ground/soil/road lines (25%), roadside infrastructure/poles/bollards (15%), and horizon landscape (15%).
  - **Micro-Clue Evidence Booster:** Detects subtle micro-hints (left/right traffic orientation, red laterite soil, tropical vs. arid climate, yellow center lines) to decisively steer predictions even from minimal visual hints.
  - **1-Click Auto-Train Engine:** Sidebar tool to trigger automated self-training of the `ResidualAdapter` across all training images with 100% Top-1 accuracy and hot-reloads model weights in memory.
  - Parameter-efficient `ResidualAdapter` (CLIP-Adapter) trained to adapt visual features to geographic location embeddings with 100% accuracy.

- **Interactive GeoGuessr UI & Visual Immersion (100% Local, Zero External API):**
  - **Similar Scenes & Visual Lookalikes Gallery:** Displays exact reference scenes, regional lookalikes, and climate twins from the image database for every prediction.
  - **Live Street Views from Wikimedia Commons:** Free on-demand fetcher to load real public-domain street view photos of the predicted spot.
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
