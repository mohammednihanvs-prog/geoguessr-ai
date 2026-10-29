import warnings
# Silence deprecation warnings globally before streamlit or plugins load
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*use_container_width.*")

import os
import sys
import streamlit as st
import torch
import torch.nn as nn
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from geopy.geocoders import Nominatim

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

st.set_page_config(
    page_title="GeoGuessr AI — Global & Village Locator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-End Futuristic Dark UI Design System (Linear / Raycast / Vision Pro Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700;800&display=swap');

    :root {
        --bg-base: #06080F;
        --bg-surface: rgba(13, 17, 28, 0.72);
        --bg-surface-elevated: rgba(20, 27, 45, 0.85);
        --bg-card: rgba(15, 20, 34, 0.65);
        --bg-glass: rgba(10, 14, 24, 0.82);
        --border-glass: rgba(255, 255, 255, 0.08);
        --border-glow: rgba(0, 229, 255, 0.35);
        --accent-cyan: #00E5FF;
        --accent-blue: #0070F3;
        --accent-violet: #7928CA;
        --accent-emerald: #00F5A0;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --font-head: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        --radius-card: 14px;
        --radius-sm: 8px;
        --radius-pill: 9999px;
        --glow-cyan: 0 0 25px rgba(0, 229, 255, 0.25);
        --glow-card: 0 10px 30px -10px rgba(0, 0, 0, 0.7), 0 0 1px 1px rgba(255, 255, 255, 0.08);
        --glow-card-hover: 0 16px 40px -10px rgba(0, 229, 255, 0.2), 0 0 1px 1px rgba(0, 229, 255, 0.45);
        --transition-smooth: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Base Body & Ambient Sci-Fi Background */
    .stApp {
        background-color: var(--bg-base);
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.09) 0%, transparent 45%),
            radial-gradient(circle at 85% 25%, rgba(121, 40, 202, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 15% 75%, rgba(0, 245, 160, 0.05) 0%, transparent 45%),
            linear-gradient(rgba(255, 255, 255, 0.016) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.016) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px;
        color: var(--text-primary);
        font-family: var(--font-body);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-head) !important;
        letter-spacing: -0.025em;
        font-weight: 700;
        color: var(--text-primary) !important;
    }

    p, span, div, label {
        font-family: var(--font-body);
    }

    code, kbd, samp, pre {
        font-family: var(--font-mono) !important;
    }

    /* Futuristic Header with Neon Underglow */
    .main-header {
        font-family: var(--font-head);
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 30%, #00E5FF 70%, #0070F3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        display: inline-block;
        filter: drop-shadow(0 2px 18px rgba(0, 229, 255, 0.3));
    }

    /* Glassmorphic Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border-right: 1px solid var(--border-glass) !important;
    }

    [data-testid="stSidebar"] hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.12) 50%, transparent 100%) !important;
    }

    /* Glassmorphic Metric Cards */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-card) !important;
        padding: 14px 18px !important;
        box-shadow: var(--glow-card);
        transition: var(--transition-smooth);
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: var(--border-glow) !important;
        box-shadow: var(--glow-card-hover);
    }

    [data-testid="stMetricLabel"] {
        font-family: var(--font-mono) !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-secondary) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: var(--font-head) !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        color: var(--accent-cyan) !important;
        text-shadow: 0 0 16px rgba(0, 229, 255, 0.3);
    }

    /* Futuristic Primary Buttons (Neon Cyan to Blue Gradient) */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #00E5FF 0%, #0070F3 60%, #7928CA 100%) !important;
        color: #040814 !important;
        font-family: var(--font-head) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: -0.01em;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 22px rgba(0, 229, 255, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
        transition: var(--transition-smooth) !important;
    }

    .stButton button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.008) !important;
        box-shadow: 0 8px 32px rgba(0, 229, 255, 0.55), inset 0 1px 1px rgba(255, 255, 255, 0.6) !important;
        color: #000000 !important;
    }

    /* Secondary Glass Buttons */
    .stButton button[kind="secondary"] {
        background: rgba(18, 24, 38, 0.72) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: #F1F5F9 !important;
        font-family: var(--font-head) !important;
        font-weight: 600 !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition-smooth) !important;
    }

    .stButton button[kind="secondary"]:hover {
        background: rgba(26, 36, 58, 0.85) !important;
        border-color: var(--accent-cyan) !important;
        color: var(--accent-cyan) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--glow-cyan) !important;
    }

    /* Link Action Buttons (Google Maps / Earth / Street View) */
    .stLinkButton a {
        background: rgba(15, 21, 35, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-head) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: var(--transition-smooth) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
    }

    .stLinkButton a:hover {
        border-color: var(--accent-cyan) !important;
        color: var(--accent-cyan) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(0, 229, 255, 0.28) !important;
    }

    /* Inputs, Selectboxes & Dropdowns */
    .stTextInput input {
        background: rgba(11, 15, 26, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: var(--radius-sm) !important;
        color: #F8FAFC !important;
        font-family: var(--font-body) !important;
        transition: var(--transition-smooth) !important;
    }

    .stTextInput input:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.25) !important;
        outline: none !important;
    }

    div[data-baseweb="select"] {
        background: rgba(11, 15, 26, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition-smooth) !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: rgba(0, 229, 255, 0.4) !important;
    }

    /* File Uploader Dropzone */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(13, 18, 30, 0.5) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1.5px dashed rgba(0, 229, 255, 0.25) !important;
        border-radius: var(--radius-card) !important;
        transition: var(--transition-smooth) !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: rgba(18, 25, 42, 0.72) !important;
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 28px rgba(0, 229, 255, 0.16) !important;
    }

    /* Neon Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00E5FF 0%, #0070F3 50%, #7928CA 100%) !important;
        box-shadow: 0 0 14px rgba(0, 229, 255, 0.4) !important;
        border-radius: var(--radius-pill) !important;
    }

    .stProgress > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: var(--radius-pill) !important;
    }

    /* Notifications & Alert Cards */
    .stAlert, div[data-testid="stNotification"] {
        background: var(--bg-card) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid var(--border-glass) !important;
        border-left: 4px solid var(--accent-cyan) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        box-shadow: var(--glow-card) !important;
    }

    /* Custom Futuristic Badges */
    .clue-badge {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: var(--radius-pill);
        font-family: var(--font-mono);
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: var(--transition-smooth);
        letter-spacing: 0.02em;
    }

    .clue-badge:hover {
        transform: translateY(-1px);
    }

    .badge-left {
        background: rgba(0, 229, 255, 0.1);
        color: #38BDF8;
        border: 1px solid rgba(0, 229, 255, 0.3);
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
    }

    .badge-right {
        background: rgba(251, 146, 60, 0.1);
        color: #FB923C;
        border: 1px solid rgba(251, 146, 60, 0.3);
        box-shadow: 0 0 12px rgba(251, 146, 60, 0.15);
    }

    .badge-cat {
        background: rgba(168, 85, 247, 0.1);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.15);
    }

    /* Folium Map Container Frame */
    iframe {
        border-radius: var(--radius-card) !important;
        border: 1px solid rgba(0, 229, 255, 0.22) !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7), 0 0 20px rgba(0, 229, 255, 0.1) !important;
        transition: var(--transition-smooth);
    }

    iframe:hover {
        border-color: rgba(0, 229, 255, 0.45) !important;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8), 0 0 30px rgba(0, 229, 255, 0.2) !important;
    }

    /* Image Element Frame */
    [data-testid="stImage"] img {
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border-glass) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }

    /* Dividers with Gradient Glow */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, rgba(0, 229, 255, 0.25) 50%, transparent 100%) !important;
        margin: 28px 0 !important;
    }

    /* Radio Buttons */
    div[data-testid="stRadio"] label {
        font-family: var(--font-body);
        font-size: 0.92rem;
        color: var(--text-primary) !important;
        transition: var(--transition-smooth);
    }

    div[data-testid="stRadio"] label:hover {
        color: var(--accent-cyan) !important;
    }

    /* Accessibility: Respect Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)

CACHE_FILE = "embeddings_cache.pt"
CORRECTIONS_FILE = "corrections_cache.pt"
ADAPTER_FILE = "clip_adapter.pt"

geolocator = Nominatim(user_agent="geoguessr_ai_global_locator")

# --- Residual Vision Adapter Architecture (Tip-Adapter / CLIP-Adapter) ---
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

# --- Load StreetCLIP, Embeddings, Adapter & Correction Memory ---
@st.cache_resource
def load_resources():
    cache_data = torch.load(CACHE_FILE, weights_only=False)
    text_embeddings = cache_data["embeddings"]
    locations = cache_data["locations"]

    # Strict deduplication on load
    seen_names = set()
    unique_indices = []
    unique_locations = []
    for idx, loc in enumerate(locations):
        norm_n = loc["name"].strip().lower()
        if norm_n not in seen_names:
            seen_names.add(norm_n)
            unique_indices.append(idx)
            unique_locations.append(loc)
    if len(unique_locations) < len(locations):
        locations = unique_locations
        text_embeddings = text_embeddings[unique_indices]

    corrections = []
    if os.path.exists(CORRECTIONS_FILE):
        try:
            corrections = torch.load(CORRECTIONS_FILE, weights_only=False)
        except Exception:
            corrections = []

    model_name = "geolocal/StreetCLIP"
    try:
        processor = CLIPProcessor.from_pretrained(model_name, local_files_only=True)
        model = CLIPModel.from_pretrained(model_name, local_files_only=True)
    except Exception:
        processor = CLIPProcessor.from_pretrained(model_name)
        model = CLIPModel.from_pretrained(model_name)

    model.eval()

    # Load Residual Adapter if trained
    adapter = None
    if os.path.exists(ADAPTER_FILE):
        try:
            adapter = ResidualAdapter()
            adapter.load_state_dict(torch.load(ADAPTER_FILE, map_location="cpu", weights_only=True))
            adapter.eval()
        except Exception:
            adapter = None

    return processor, model, text_embeddings, locations, corrections, adapter

processor, model, text_embeddings, locations, corrections, adapter = load_resources()

# --- Multi-Scale Test-Time Augmentation (TTA) Feature Extraction ---
def extract_visual_representation(image):
    """
    Extracts multi-scale visual features:
    1. Full scene (60% weight)
    2. Lower road / soil / markings crop (25% weight)
    3. Center landscape crop (15% weight)
    Captures both ground-level road cues and horizon architecture.
    """
    w, h = image.size
    crops = [
        image,
        image.crop((0, int(h * 0.25), w, h)),
        image.crop((int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9)))
    ]
    weights = [0.60, 0.25, 0.15]

    inputs = processor(images=crops, return_tensors="pt")
    with torch.no_grad():
        out = model.get_image_features(pixel_values=inputs["pixel_values"])
        raw = out.pooler_output if hasattr(out, "pooler_output") else out
        norms = raw / raw.norm(dim=-1, keepdim=True)
        w_tensor = torch.tensor(weights, device=norms.device).unsqueeze(1)
        combined = (norms * w_tensor).sum(dim=0, keepdim=True)
        image_embedding = combined / combined.norm(dim=-1, keepdim=True)

        # Apply trained residual adapter if present
        if adapter is not None:
            image_embedding = adapter(image_embedding)

    return image_embedding

# --- Prediction Pipeline with Multi-Scale TTA and Visual Memory Matching ---
def predict_location(image, current_embeddings, current_locations, corrections_list=None, category_filter="All"):
    # Filter candidates if requested
    if category_filter != "All":
        indices = [i for i, loc in enumerate(current_locations) if loc.get("category") == category_filter]
        active_embeddings = current_embeddings[indices]
        active_locations = [current_locations[i] for i in indices]
    else:
        active_embeddings = current_embeddings
        active_locations = current_locations

    image_embedding = extract_visual_representation(image)

    # Baseline text-image cosine similarities: [1, 768] @ [768, N] -> [N]
    sim_scores = torch.matmul(image_embedding, active_embeddings.T).squeeze(0)

    # Strict Visual Correction Memory Boost (only exact/near-exact image >= 0.92)
    if corrections_list:
        for item in corrections_list:
            corr_emb = item["embedding"].to(image_embedding.device)
            cos_sim = torch.dot(image_embedding.squeeze(0), corr_emb.squeeze(0)).item()
            if cos_sim >= 0.92:
                corr_target = item["location_name"].strip().lower()
                for idx, loc in enumerate(active_locations):
                    if loc["name"].strip().lower() == corr_target:
                        sim_scores[idx] += (cos_sim - 0.90) * 15.0 + 1.2
                        break

    # Scaled softmax for clean confidence distribution
    probabilities = torch.softmax(sim_scores * 35.0, dim=-1).tolist()

    ranked = []
    for loc, prob in zip(active_locations, probabilities):
        ranked.append({
            "name": loc["name"],
            "lat": loc.get("lat", 9.3175),
            "lon": loc.get("lon", 76.6114),
            "country": loc.get("country", "Unknown"),
            "region": loc.get("region", ""),
            "category": loc.get("category", "General"),
            "driving_side": loc.get("driving_side", "Unknown"),
            "prompt": loc.get("prompt", ""),
            "confidence": prob
        })
    ranked.sort(key=lambda x: x["confidence"], reverse=True)
    return ranked

# --- Register Human Feedback & Retrain Prompt Embeddings ---
def apply_user_correction(
    image,
    target_location_name,
    visual_clues,
    country,
    region,
    category,
    driving_side,
    current_embeddings,
    current_locations,
    corrections_list
):
    # Extract image embedding fingerprint
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        im_out = model.get_image_features(pixel_values=inputs["pixel_values"])
        im_raw = im_out.pooler_output if hasattr(im_out, "pooler_output") else im_out
        img_emb = (im_raw / im_raw.norm(dim=-1, keepdim=True)).cpu().squeeze(0)

    # 1. Register in Visual Correction Cache (prevent duplicate image fingerprints)
    if corrections_list is None:
        corrections_list = []
    
    matched_corr_idx = None
    for c_i, c_item in enumerate(corrections_list):
        c_emb = c_item["embedding"]
        cos_sim = torch.dot(img_emb, c_emb).item()
        if cos_sim >= 0.98:  # Same image already recorded
            matched_corr_idx = c_i
            break
    
    if matched_corr_idx is not None:
        corrections_list[matched_corr_idx] = {
            "location_name": target_location_name.strip(),
            "embedding": img_emb
        }
    else:
        corrections_list.append({
            "location_name": target_location_name.strip(),
            "embedding": img_emb
        })
    torch.save(corrections_list, CORRECTIONS_FILE)

    # 2. Build target text prompt and re-encode
    target_prompt = (
        f"a street view photo in {target_location_name.strip()}, {visual_clues}"
        if visual_clues
        else f"a street view photo in {target_location_name.strip()}"
    )

    with torch.no_grad():
        target_input = processor(text=[target_prompt], return_tensors="pt", padding=True, truncation=True, max_length=77)
        tx_out = model.get_text_features(input_ids=target_input["input_ids"])
        tx_raw = tx_out.pooler_output if hasattr(tx_out, "pooler_output") else tx_out
        updated_text_vec = (tx_raw / tx_raw.norm(dim=-1, keepdim=True)).cpu()

    # 3. Update location index with STRICT DEDUPLICATION
    norm_target = target_location_name.strip().lower()
    existing_idx = None
    for idx, loc in enumerate(current_locations):
        if loc["name"].strip().lower() == norm_target:
            existing_idx = idx
            break

    if existing_idx is not None:
        # UPDATE in-place: guaranteed NO duplicate added
        new_embeddings = current_embeddings.clone()
        new_embeddings[existing_idx] = updated_text_vec
        new_locations = [dict(loc) for loc in current_locations]
        new_locations[existing_idx]["prompt"] = target_prompt
        if visual_clues:
            new_locations[existing_idx]["visual_clues"] = visual_clues
        if country:
            new_locations[existing_idx]["country"] = country
        if region:
            new_locations[existing_idx]["region"] = region
        if category and category != "User Added":
            new_locations[existing_idx]["category"] = category
        if driving_side and driving_side != "Unknown":
            new_locations[existing_idx]["driving_side"] = driving_side
        was_added = False
    else:
        # ADD as new location only if it doesn't exist
        lat, lon = 9.3175, 76.6114
        try:
            geo_res = geolocator.geocode(target_location_name.strip(), timeout=5)
            if geo_res:
                lat, lon = geo_res.latitude, geo_res.longitude
        except Exception:
            pass

        new_embeddings = torch.cat([current_embeddings, updated_text_vec], dim=0)
        new_locations = [dict(loc) for loc in current_locations] + [{
            "name": target_location_name.strip(),
            "lat": lat,
            "lon": lon,
            "country": country or "Unknown",
            "region": region or "",
            "category": category or "User Added",
            "driving_side": driving_side or "Unknown",
            "prompt": target_prompt
        }]
        was_added = True

    # 4. Mandatory safety deduplication pass before persisting
    seen_names = set()
    deduped_locations = []
    deduped_indices = []
    for idx, loc in enumerate(new_locations):
        k = loc["name"].strip().lower()
        if k not in seen_names:
            seen_names.add(k)
            deduped_locations.append(loc)
            deduped_indices.append(idx)

    if len(deduped_locations) < len(new_locations):
        new_locations = deduped_locations
        new_embeddings = new_embeddings[deduped_indices]

    torch.save({"embeddings": new_embeddings, "locations": new_locations}, CACHE_FILE)
    st.cache_resource.clear()

    return new_embeddings, new_locations, corrections_list, was_added

# --- Helper: Generate External Maps & Earth URLs ---
def get_map_urls(lat, lon):
    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    gearth_url = f"https://earth.google.com/web/search/{lat},{lon}"
    streetview_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"
    return gmaps_url, gearth_url, streetview_url

# --- Sidebar UI ---
with st.sidebar:
    st.markdown("### 🌐 AI Model Telemetry")
    adapter_status = "✅ Active (Trained)" if adapter is not None else "⚡ Zero-Shot Mode"
    st.info(f"**Vision Adapter:** {adapter_status}\n\n**Total Indexed Places:** `{len(locations)}`\n\n**Visual Corrections:** `{len(corrections)}`")

    st.divider()
    st.subheader("🎯 Prediction Scope Lens")
    scope_choice = st.selectbox(
        "Filter prediction scope:",
        [
            "All (Global + Pan-India + Kerala)",
            "Global (International Countries)",
            "Kerala - Micro-Region (Villages & Towns)",
            "India - State/UT",
            "India - City/Hub"
        ]
    )

    scope_mapping = {
        "All (Global + Pan-India + Kerala)": "All",
        "Global (International Countries)": "Global",
        "Kerala - Micro-Region (Villages & Towns)": "Kerala - Micro-Region",
        "India - State/UT": "India - State/UT",
        "India - City/Hub": "India - City/Hub"
    }
    selected_scope = scope_mapping[scope_choice]

    st.divider()
    st.markdown("### 🗺️ Satellite & Earth Meta")
    st.caption("Includes direct integration with **Google Maps, Google Earth 3D, and Google Street View**.")

# --- Main Page Header ---
st.markdown("<h1 class='main-header'>🌍 Global & Hyper-Local GeoGuessr AI</h1>", unsafe_allow_html=True)
st.markdown("Pins street view and outdoor landscape photos down to **exact global countries, Indian states, and Kerala village micro-regions** using multi-scale vision AI and satellite telemetry.")

# Show correction success alert if just updated
if "just_corrected" in st.session_state:
    corr = st.session_state["just_corrected"]
    act_str = f" • *{corr['action']}*" if "action" in corr else ""
    st.success(
        f"🎉 **Correction Applied Successfully!** Previously: `{corr['old']}` ➡️ Now Corrected to: **{corr['new']}** (`{corr['conf']*100:.2f}%` confidence)!{act_str}"
    )
    del st.session_state["just_corrected"]

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("1. Select or Upload Image")
    uploaded_file = st.file_uploader("Upload an outdoor or street photo...", type=["jpg", "jpeg", "png"])

    # Categorized Sample Picker for instant testing
    sample_categories = {
        "🌴 Kerala Villages & Towns": [
            "Munnar_Idukki_Kerala_India.jpg",
            "Fort_Kochi_Ernakulam_Kerala_India.jpg",
            "Kuttanad_Alappuzha_Kerala_India.jpg",
            "Varkala_Cliff_Thiruvananthapuram_Kerala_India.jpg",
            "Athirappilly_Thrissur_Kerala_India.jpg",
            "Bekal_Fort_Kasaragod_Kerala_India.jpg",
            "Vagamon_Idukki_Kerala_India.jpg",
            "Kumarakom_Kottayam_Kerala_India.jpg",
            "Calicut_Beach_Kozhikode_Kerala_India.jpg",
            "Thrissur_Swaraj_Round_Kerala_India.jpg",
            "Ponmudi_Hill_Thiruvananthapuram_Kerala_India.jpg",
            "Munroe_Island_Kollam_Kerala_India.jpg",
            "kerala-main-scaled.jpg"
        ],
        "🇮🇳 Pan-India Heritage & Metros": [
            "Varanasi_Ghats_Uttar_Pradesh_India.jpg",
            "Jaipur_Pink_City_Rajasthan_India.jpg",
            "Old_Delhi_Chandni_Chowk_Delhi_India.jpg",
            "Hampi_Bellary_Karnataka_India.jpg",
            "Mumbai_Marine_Drive_Maharashtra_India.jpg",
            "Kolkata_Howrah_Bridge_West_Bengal_India.jpg",
            "Amritsar_Golden_Temple_Punjab_India.jpg",
            "Shimla_Mall_Road_Himachal_Pradesh_India.jpg",
            "Ladakh_Pangong_Tso_India.jpg",
            "Goa_Panaji_Latin_Quarter_India.jpg",
            "Bengaluru_Vidhana_Soudha_Karnataka_India.jpg",
            "Meghalaya_Living_Root_Bridge_India.jpg",
            "Agra_Taj_Mahal_Uttar_Pradesh_India.jpg",
            "Hyderabad_Charminar_Telangana_India.jpg",
            "Kashmir_Dal_Lake_Srinagar_India.jpg"
        ],
        "🌐 International Cities & Landscapes": [
            "Tokyo_Shinjuku_Japan.jpg",
            "Kyoto_Gion_Japan.jpg",
            "Paris_Haussmann_Boulevard_France.jpg",
            "London_Westminster_United_Kingdom.jpg",
            "New_York_City_Manhattan_United_States.jpg",
            "Amsterdam_Canal_Netherlands.jpg",
            "Rome_Street_Colosseum_Italy.jpg",
            "Swiss_Alps_Lauterbrunnen_Switzerland.jpg",
            "Sydney_Harbour_Australia.jpg",
            "Rio_de_Janeiro_Copacabana_Brazil.jpg",
            "Reykjavik_Iceland.jpg",
            "Cairo_Giza_Pyramids_Egypt.jpg",
            "Cape_Town_Table_Mountain_South_Africa.jpg",
            "Bavaria_Neuschwanstein_Germany.jpg",
            "San_Francisco_Golden_Gate_United_States.jpg",
            "Singapore_Marina_Bay_Singapore.jpg",
            "Scottish_Highlands_Scotland_UK.jpg"
        ]
    }

    # Flatten existing available samples
    available_samples = []
    if os.path.exists("Imgs"):
        existing_disk = set(os.listdir("Imgs"))
        sample_options = ["(Upload your own image)"]
        for cat_name, cat_files in sample_categories.items():
            for f in cat_files:
                if f in existing_disk:
                    sample_options.append(f"{cat_name.split()[0]} {f}")
    else:
        sample_options = ["(Upload your own image)"]

    selected_sample = st.selectbox("Or choose a pre-loaded GeoGuessr challenge photo:", sample_options)

    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
    elif selected_sample != "(Upload your own image)":
        clean_filename = selected_sample.split(" ", 1)[1]
        sample_path = os.path.join("Imgs", clean_filename)
        if os.path.exists(sample_path):
            image = Image.open(sample_path).convert("RGB")

    if image is not None:
        st.image(image, caption="Query Photo", use_container_width=True)
        predict_btn = st.button("📍 Geoguess & Analyze Location", type="primary", use_container_width=True)

with col_right:
    st.subheader("2. AI GeoGuessr Analysis")

    if image is not None and "predict_btn" in locals() and predict_btn:
        with st.spinner(f"Running multi-scale vision inference across {len(locations)} locations..."):
            ranked = predict_location(image, text_embeddings, locations, corrections_list=corrections, category_filter=selected_scope)
            st.session_state["ranked"] = ranked
            st.session_state["last_image"] = image

    if "ranked" in st.session_state and len(st.session_state["ranked"]) > 0:
        ranked = st.session_state["ranked"]
        top_pick = ranked[0]
        top_lat = top_pick["lat"]
        top_lon = top_pick["lon"]

        # URLs for Google Maps and Google Earth
        gmaps_url, gearth_url, gstreet_url = get_map_urls(top_lat, top_lon)

        # Top Match Hero Card
        st.success(f"### 🎯 Top Match: **{top_pick['name']}**")

        # Metrics row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("AI Confidence", f"{top_pick['confidence']*100:.2f}%")
        with m2:
            st.metric("Country", top_pick['country'])
        with m3:
            driving_icon = "🚗 Driving: Left" if top_pick['driving_side'] == "Left" else "🚙 Driving: Right"
            st.metric("Road Rules", driving_icon)

        # Prominent Google Earth & Maps Action Buttons
        st.markdown("**🌐 Explore in Satellite & 3D Maps:**")
        b1, b2, b3 = st.columns(3)
        with b1:
            st.link_button("🗺️ Google Maps", gmaps_url, use_container_width=True)
        with b2:
            st.link_button("🌐 Google Earth 3D", gearth_url, use_container_width=True)
        with b3:
            st.link_button("🚶 Street View", gstreet_url, use_container_width=True)

        st.write("")

        # Dynamic Folium Map with Satellite Layer Control
        zoom_level = 12 if "Micro-Region" in top_pick["category"] else (7 if "State" in top_pick["category"] else 5)
        m = folium.Map(location=[top_lat, top_lon], zoom_start=zoom_level, tiles=None)

        # Base Layers: Street View & Satellite Imagery
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery',
            name='🛰️ Satellite (Esri Aerial)'
        ).add_to(m)
        folium.TileLayer('OpenStreetMap', name='🗺️ Street Map').add_to(m)

        # Heatmap of top 15 candidate matches
        heat_data = [[item["lat"], item["lon"], item["confidence"]] for item in ranked[:15]]
        HeatMap(heat_data, radius=25, blur=18, max_zoom=14).add_to(m)

        # Add top 5 ranked markers with custom popups including Google Earth links
        for i, item in enumerate(ranked[:5], start=1):
            color = "red" if i == 1 else ("orange" if i == 2 else "blue")
            pin_icon = "star" if i == 1 else "info-sign"
            m_gmaps, m_earth, _ = get_map_urls(item["lat"], item["lon"])
            
            popup_html = f"""
            <div style='font-family:Inter,-apple-system,sans-serif; min-width:210px; background:#0c101c; color:#f1f5f9; padding:12px 14px; border-radius:12px; border:1px solid rgba(0,229,255,0.25); box-shadow:0 12px 32px rgba(0,0,0,0.7);'>
                <b style='font-size:13px; color:#00E5FF; font-family:Space Grotesk,sans-serif; letter-spacing:-0.01em;'>#{i} {item['name']}</b><br/>
                <span style='color:#94a3b8; font-size:11px;'>Confidence: <b style='color:#f8fafc;'>{item['confidence']*100:.1f}%</b></span><br/>
                <span style='color:#cbd5e1; font-size:11px;'>Driving: <b>{item['driving_side']}</b></span><br/>
                <hr style='margin:8px 0; border:none; height:1px; background:rgba(255,255,255,0.1);'/>
                <a href='{m_gmaps}' target='_blank' style='color:#38bdf8; font-weight:600; text-decoration:none; margin-right:10px; font-size:11.5px;'>📍 Google Maps</a>
                <a href='{m_earth}' target='_blank' style='color:#00F5A0; font-weight:600; text-decoration:none; font-size:11.5px;'>🌐 Google Earth</a>
            </div>
            """
            
            folium.Marker(
                [item["lat"], item["lon"]],
                popup=folium.Popup(popup_html, max_width=280),
                icon=folium.Icon(color=color, icon=pin_icon)
            ).add_to(m)

        folium.LayerControl(position="topright").add_to(m)
        st_folium(m, width=650, height=380)

        # GeoGuessr Clues Inspector
        st.markdown("#### 🕵️ GeoGuessr Detective Breakdown")
        st.markdown(
            f"<span class='clue-badge badge-cat'>🏷️ {top_pick['category']}</span>"
            f"<span class='clue-badge badge-left'>{driving_icon}</span>"
            f"<span class='clue-badge badge-cat'>📍 Lat: {top_lat:.3f}, Lon: {top_lon:.3f}</span>",
            unsafe_allow_html=True
        )
        if top_pick.get("prompt"):
            st.caption(f"**Visual Meta Clues:** *{top_pick['prompt']}*")

        # Top 5 Candidates List with Direct Maps/Earth shortcuts
        st.markdown("#### 🏆 Top Ranked Candidates")
        for i, item in enumerate(ranked[:5], start=1):
            col_rank, col_bar = st.columns([3, 2])
            item_gmaps, item_earth, _ = get_map_urls(item["lat"], item["lon"])
            with col_rank:
                st.write(f"**{i}. {item['name']}**")
                st.caption(
                    f"`{item['category']}` | 🚗 `{item['driving_side']}` | "
                    f"[Maps]({item_gmaps}) · [Earth]({item_earth})"
                )
            with col_bar:
                st.progress(min(1.0, float(item['confidence'] * 2.0)))
                st.caption(f"**{item['confidence']*100:.2f}%**")

        # Feedback & Active Retraining
        st.divider()
        st.subheader("3. Human-in-the-Loop Active Retraining")
        st.caption("Did the AI get it wrong? Correct it here. The visual fingerprint memory will permanently remember this scene without catastrophic forgetting.")

        feedback_choice = st.radio(
            "Did the AI guess correctly?",
            (
                "✅ Yes, prediction is correct",
                "🔍 No, choose from available options (Search database)",
                "➕ No, register a new location"
            ),
            index=0,
            horizontal=False
        )

        # Unique locations pool (strictly deduplicated by lowercase name)
        unique_loc_pool = {}
        for loc in locations:
            k = loc["name"].strip().lower()
            if k not in unique_loc_pool:
                unique_loc_pool[k] = loc
        unique_loc_list = list(unique_loc_pool.values())

        target_name = None
        descriptors = ""
        reg_country = ""
        reg_region = ""
        reg_category = ""
        reg_driving = "Left"

        if feedback_choice == "✅ Yes, prediction is correct":
            target_name = top_pick["name"]
            descriptors = ""
            reg_country = top_pick.get("country", "")
            reg_region = top_pick.get("region", "")
            reg_category = top_pick.get("category", "")
            reg_driving = top_pick.get("driving_side", "Left")
            st.info(f"Retraining on this image will reinforce the AI's confidence for **{target_name}**.")

        elif feedback_choice == "🔍 No, choose from available options (Search database)":
            st.markdown("##### 🔍 Search Available Locations")
            
            c_s1, c_s2 = st.columns([3, 2])
            with c_s1:
                search_query = st.text_input(
                    "Search locations by name, city, state, or country:",
                    placeholder="Type to filter... (e.g. Kozhikode, Munich, Tokyo, Wayanad, France, Kerala)",
                    key="loc_search_query"
                )
            with c_s2:
                all_cats = ["All Categories"] + sorted(list({l.get("category", "") for l in unique_loc_list if l.get("category")}))
                selected_cat = st.selectbox("Filter by Category:", all_cats, key="loc_filter_cat")

            # Real-time search filtering
            q = search_query.strip().lower() if search_query else ""
            matching_locations = []
            for loc in unique_loc_list:
                if selected_cat != "All Categories" and loc.get("category") != selected_cat:
                    continue
                if not q:
                    matching_locations.append(loc)
                else:
                    search_haystack = f"{loc['name']} {loc.get('country', '')} {loc.get('region', '')} {loc.get('category', '')} {loc.get('prompt', '')}".lower()
                    if q in search_haystack:
                        matching_locations.append(loc)

            if not matching_locations:
                st.warning(f"❌ No existing location matches **'{search_query}'**.")
                st.info("💡 To keep the database clean and prevent duplicate entries, check your search spelling. If this place is genuinely not in the database, choose **'➕ No, register a new location'** above.")
            else:
                st.caption(f"Showing **{len(matching_locations)}** matching location(s) out of {len(unique_loc_list)} total places:")

                # Build options map with rich informative labels
                option_map = {}
                for loc in matching_locations:
                    driving_str = "🚗 Driving: Left" if loc.get("driving_side") == "Left" else "🚙 Driving: Right"
                    country_info = f" | {loc.get('country', '')}" if loc.get('country') else ""
                    label = f"📍 {loc['name']} — [{loc.get('category', 'Place')}{country_info} | {driving_str}]"
                    option_map[label] = loc

                chosen_label = st.selectbox(
                    "Select correct location from matching results:",
                    options=list(option_map.keys()),
                    key="selected_loc_dropdown"
                )

                matched_loc = option_map[chosen_label]
                target_name = matched_loc["name"]
                reg_country = matched_loc.get("country", "")
                reg_region = matched_loc.get("region", "")
                reg_category = matched_loc.get("category", "")
                reg_driving = matched_loc.get("driving_side", "Left")
                descriptors = ""

                # Display card confirming selection & duplicate prevention guarantee
                st.markdown(
                    f"<div style='background:rgba(12,24,20,0.72); backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); border:1px solid rgba(0,245,160,0.25); border-left:4px solid #00F5A0; padding:12px 16px; border-radius:10px; margin:8px 0 12px 0; box-shadow:0 8px 24px rgba(0,0,0,0.5);'>"
                    f"<b style='color:#f8fafc; font-family:Space Grotesk,sans-serif;'>Selected Target:</b> <span style='color:#00E5FF; font-weight:600;'>{matched_loc['name']}</span><br/>"
                    f"<span style='color:#94a3b8; font-size:0.88rem;'>Category: <code style='background:rgba(255,255,255,0.06); color:#38bdf8; border:1px solid rgba(255,255,255,0.08);'>{reg_category}</code> | Country: <b style='color:#f1f5f9;'>{reg_country}</b> | Region: <b style='color:#f1f5f9;'>{reg_region}</b> | Driving: <b style='color:#00F5A0;'>{reg_driving}</b></span><br/>"
                    f"<span style='color:#00F5A0; font-size:0.82rem; font-weight:600;'>🛡️ Duplicate Protection Active: Updates existing place in-place without duplicating.</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        else:
            st.markdown("##### ➕ Register a New Location")
            target_name = st.text_input(
                "Exact Place Name:",
                placeholder="e.g. Kozhencherry, Pathanamthitta, Kerala, India",
                help="Enter the canonical name for this place."
            )

            # Active Duplicate Detection & Warning
            if target_name and target_name.strip():
                clean_input = target_name.strip().lower()
                
                # 1. Exact match check
                exact_dup = next((l for l in unique_loc_list if l["name"].strip().lower() == clean_input), None)
                if exact_dup:
                    st.warning(
                        f"⚠️ **Duplicate Alert:** '{exact_dup['name']}' already exists in the database!\n\n"
                        f"Retraining with this name will update the existing location in-place, preventing any duplicate entries."
                    )
                else:
                    # 2. Similar / Substring match check
                    similar_matches = [
                        l for l in unique_loc_list
                        if clean_input in l["name"].strip().lower() or l["name"].strip().lower() in clean_input
                    ]
                    if similar_matches:
                        similar_names = [f"**'{l['name']}'**" for l in similar_matches[:3]]
                        st.info(
                            f"💡 **Similar place found in database:** {', '.join(similar_names)}.\n\n"
                            f"If this is the same place, please choose **'🔍 No, choose from available options'** above to avoid creating a duplicate entry."
                        )

            descriptors = st.text_input(
                "Visual clues (soil, flora, roads, architecture, signage):",
                placeholder="e.g. red laterite soil, rubber plantations, Malayalam shop boards, white roadside bollards"
            )
            c_a, c_b, c_c = st.columns(3)
            with c_a:
                reg_country = st.text_input("Country:", value="India")
            with c_b:
                reg_region = st.text_input("State / Region:", value="Kerala")
            with c_c:
                reg_driving = st.selectbox("Driving Side:", ["Left", "Right"])
            reg_category = "User Added"

        train_btn = st.button("🧠 Retrain Model on this Image", type="secondary", use_container_width=True)

        if train_btn:
            if not target_name or target_name.strip() == "":
                st.warning("Please specify or select a location name.")
            else:
                old_top_name = top_pick["name"]
                with st.spinner(f"Updating visual memory and text embeddings for '{target_name}'..."):
                    new_embeddings, new_locations, corrections, was_added = apply_user_correction(
                        st.session_state["last_image"],
                        target_name.strip(),
                        descriptors.strip() if descriptors else "",
                        reg_country.strip() if reg_country else "",
                        reg_region.strip() if reg_region else "",
                        reg_category,
                        reg_driving,
                        text_embeddings,
                        locations,
                        corrections
                    )

                    # Immediately re-evaluate the image with updated memory
                    new_ranked = predict_location(
                        st.session_state["last_image"],
                        new_embeddings,
                        new_locations,
                        corrections_list=corrections,
                        category_filter=selected_scope
                    )

                    st.session_state["ranked"] = new_ranked
                    action_text = "Registered new location" if was_added else "Updated existing location in-place (no duplicate)"
                    st.session_state["just_corrected"] = {
                        "old": old_top_name,
                        "new": new_ranked[0]["name"],
                        "conf": new_ranked[0]["confidence"],
                        "action": action_text
                    }
                    st.rerun()