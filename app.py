import warnings
# Silence deprecation warnings globally before streamlit or plugins load
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*use_container_width.*")

import os
import sys
import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from PIL import Image, ExifTags
from transformers import CLIPModel, CLIPProcessor
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

st.set_page_config(
    page_title="GeoGuessr AI — Global & Village Locator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apple-Inspired Bright Light UI Design System (SF Pro Typography • Clean Light Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    :root {
        --apple-bg: #F5F5F7;
        --apple-surface: #FFFFFF;
        --apple-surface-hover: #FBFBFD;
        --apple-border: #E5E5EA;
        --apple-border-focus: #0071E3;
        --apple-blue: #0071E3;
        --apple-blue-hover: #0077ED;
        --apple-green: #34C759;
        --apple-purple: #5856D6;
        --apple-orange: #FF9500;
        --apple-text-primary: #1D1D1F;
        --apple-text-secondary: #86868B;
        --apple-text-tertiary: #6E6E73;
        --font-apple: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "SF Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
        --font-mono: "SF Mono", Menlo, Monaco, Consolas, "JetBrains Mono", monospace;
        --radius-card: 16px;
        --radius-pill: 980px;
        --radius-sm: 10px;
        --shadow-subtle: 0 2px 12px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02);
        --shadow-card-hover: 0 12px 36px rgba(0, 0, 0, 0.08), 0 2px 6px rgba(0, 0, 0, 0.03);
        --shadow-button: 0 2px 8px rgba(0, 113, 227, 0.25);
        --transition-apple: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Bright Apple Product Page Background */
    .stApp {
        background-color: var(--apple-bg) !important;
        background-image: linear-gradient(180deg, #FFFFFF 0%, #F5F5F7 280px) !important;
        color: var(--apple-text-primary) !important;
        font-family: var(--font-apple) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Hide Streamlit default chrome & deploy clutter */
    #MainMenu, header, footer, .stDeployButton, div[data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        pointer-events: none !important;
    }

    /* Apple Ergonomic Page Container Spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1280px !important;
        margin: 0 auto !important;
    }

    /* Apple SF Pro Typography System */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-apple) !important;
        letter-spacing: -0.028em;
        font-weight: 700;
        color: var(--apple-text-primary) !important;
    }

    p, label {
        font-family: var(--font-apple) !important;
        color: var(--apple-text-primary);
    }

    div, span {
        color: var(--apple-text-primary);
    }

    /* Never override Streamlit Material ligature icon fonts */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [class*="material-symbols"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        font-feature-settings: 'liga' 1 !important;
        -webkit-font-smoothing: antialiased !important;
    }

    code, kbd, samp, pre {
        font-family: var(--font-mono) !important;
    }

    /* Text Selection Highlight (Apple Translucent Blue) */
    ::selection {
        background: rgba(0, 113, 227, 0.2) !important;
        color: #1D1D1F !important;
    }

    /* Apple Signature Title Header */
    .main-header {
        font-family: var(--font-apple);
        font-size: 2.7rem;
        font-weight: 700;
        letter-spacing: -0.035em;
        color: #1D1D1F !important;
        background: linear-gradient(135deg, #1D1D1F 0%, #0071E3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        display: inline-block;
    }

    .main-subtitle {
        font-family: var(--font-apple) !important;
        font-size: 1.05rem !important;
        color: var(--apple-text-tertiary) !important;
        line-height: 1.55 !important;
        margin-top: -0.1rem !important;
        margin-bottom: 1.6rem !important;
    }

    /* Clean Bright Sidebar with macOS Glass Frost */
    [data-testid="stSidebar"] {
        background: rgba(245, 245, 247, 0.88) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border-right: 1px solid var(--apple-border) !important;
    }

    [data-testid="stSidebar"] hr {
        border: none !important;
        height: 1px !important;
        background: var(--apple-border) !important;
    }

    /* Bright Apple Metric Cards */
    [data-testid="stMetric"] {
        background: var(--apple-surface) !important;
        border: 1px solid var(--apple-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 16px 20px !important;
        box-shadow: var(--shadow-card) !important;
        transition: var(--transition-apple) !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-card-hover) !important;
        border-color: rgba(0, 113, 227, 0.3) !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: var(--font-apple) !important;
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--apple-text-secondary) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: var(--font-apple) !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        color: var(--apple-text-primary) !important;
        letter-spacing: -0.02em !important;
    }

    /* Apple Signature Pill Buttons (Primary Apple Blue) */
    .stButton button[kind="primary"] {
        background: var(--apple-blue) !important;
        color: #FFFFFF !important;
        font-family: var(--font-apple) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        letter-spacing: -0.01em;
        border: none !important;
        border-radius: var(--radius-pill) !important;
        padding: 12px 26px !important;
        box-shadow: var(--shadow-button) !important;
        transition: var(--transition-apple) !important;
    }

    .stButton button[kind="primary"]:hover {
        background: var(--apple-blue-hover) !important;
        transform: scale(1.01) !important;
        box-shadow: 0 4px 14px rgba(0, 113, 227, 0.35) !important;
    }

    /* Secondary Apple Soft Gray Buttons */
    .stButton button[kind="secondary"] {
        background: #E8E8ED !important;
        color: var(--apple-text-primary) !important;
        font-family: var(--font-apple) !important;
        font-weight: 500 !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-pill) !important;
        padding: 10px 22px !important;
        transition: var(--transition-apple) !important;
    }

    .stButton button[kind="secondary"]:hover {
        background: #DCDCE2 !important;
        color: var(--apple-text-primary) !important;
        transform: translateY(-1px) !important;
    }

    /* Apple White Link Buttons (Maps / Earth / Street View) */
    .stLinkButton a {
        background: var(--apple-surface) !important;
        border: 1px solid #D2D2D7 !important;
        border-radius: var(--radius-pill) !important;
        color: var(--apple-blue) !important;
        font-family: var(--font-apple) !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: var(--transition-apple) !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
    }

    .stLinkButton a:hover {
        border-color: var(--apple-blue) !important;
        background: var(--apple-surface-hover) !important;
        color: var(--apple-blue-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 10px rgba(0, 113, 227, 0.15) !important;
    }

    /* Bright Apple Form Controls & Inputs */
    .stTextInput input {
        background: var(--apple-surface) !important;
        border: 1px solid #D2D2D7 !important;
        border-radius: var(--radius-sm) !important;
        color: var(--apple-text-primary) !important;
        font-family: var(--font-apple) !important;
        font-size: 0.95rem !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        transition: var(--transition-apple) !important;
    }

    .stTextInput input:focus {
        border-color: var(--apple-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.16) !important;
        outline: none !important;
    }

    div[data-baseweb="select"] {
        background: var(--apple-surface) !important;
        border: 1px solid #D2D2D7 !important;
        border-radius: var(--radius-sm) !important;
        color: var(--apple-text-primary) !important;
        font-family: var(--font-apple) !important;
        transition: var(--transition-apple) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: #B0B0B8 !important;
    }

    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: #1D1D1F !important;
        border-radius: var(--radius-sm) !important;
    }

    /* BaseWeb Popover Menus & Dropdown Options */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #E5E5EA !important;
        box-shadow: 0 10px 32px rgba(0, 0, 0, 0.12) !important;
        color: #1D1D1F !important;
        padding: 6px !important;
    }

    li[role="option"] {
        background: #FFFFFF !important;
        color: #1D1D1F !important;
        font-family: var(--font-apple) !important;
        font-size: 0.92rem !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 2px !important;
        transition: var(--transition-apple) !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background: #F0F6FE !important;
        color: #0071E3 !important;
        font-weight: 500 !important;
    }

    /* Apple Squircle Border Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--apple-surface) !important;
        border: 1px solid var(--apple-border) !important;
        border-radius: 14px !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03) !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        transition: var(--transition-apple) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #D2D2D7 !important;
        box-shadow: var(--shadow-card) !important;
        transform: translateY(-1px);
    }

    /* Apple Dropzone & Upload Button */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--apple-surface) !important;
        border: 1.5px dashed #C7C7CC !important;
        border-radius: var(--radius-card) !important;
        box-shadow: var(--shadow-subtle) !important;
        transition: var(--transition-apple) !important;
        padding: 22px 18px !important;
        cursor: pointer !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: var(--apple-surface-hover) !important;
        border-color: var(--apple-blue) !important;
        box-shadow: 0 4px 18px rgba(0, 113, 227, 0.10) !important;
    }

    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploader"] button[kind="secondary"] {
        background: #EBF5FF !important;
        color: var(--apple-blue) !important;
        font-family: var(--font-apple);
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        letter-spacing: -0.01em !important;
        border: 1px solid #CCE4FF !important;
        border-radius: var(--radius-pill) !important;
        padding: 8px 22px !important;
        box-shadow: 0 1px 4px rgba(0, 113, 227, 0.12) !important;
        transition: var(--transition-apple) !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
    }

    [data-testid="stFileUploaderDropzone"] button [data-testid="stIconMaterial"],
    [data-testid="stFileUploaderDropzone"] button .material-symbols-rounded {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-size: 1.15rem !important;
        line-height: 1 !important;
        display: inline-block !important;
        vertical-align: middle !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stFileUploader"] button[kind="secondary"]:hover {
        background: var(--apple-blue) !important;
        color: #FFFFFF !important;
        border-color: var(--apple-blue) !important;
        box-shadow: 0 4px 14px rgba(0, 113, 227, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    [data-testid="stFileUploaderDropzone"] button:active,
    [data-testid="stFileUploader"] button[kind="secondary"]:active {
        transform: scale(0.98) !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: var(--apple-text-secondary) !important;
        font-family: var(--font-apple) !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: var(--apple-text-primary) !important;
        font-family: var(--font-apple) !important;
        font-weight: 500 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: var(--apple-text-secondary) !important;
        font-family: var(--font-apple) !important;
        font-size: 0.82rem !important;
    }

    [data-testid="stFileUploaderFile"] {
        background: #FFFFFF !important;
        border: 1px solid var(--apple-border) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        margin-top: 8px !important;
    }

    [data-testid="stFileUploaderDeleteBtn"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 4px !important;
        color: #86868B !important;
        border-radius: 50% !important;
    }

    [data-testid="stFileUploaderDeleteBtn"]:hover {
        background: #F2F2F7 !important;
        color: #FF3B30 !important;
    }

    /* Apple Vibrant Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0071E3 0%, #34C759 100%) !important;
        border-radius: var(--radius-pill) !important;
    }

    .stProgress > div > div > div {
        background: #E5E5EA !important;
        border-radius: var(--radius-pill) !important;
    }

    /* Bright Apple Notification Cards */
    .stAlert, div[data-testid="stNotification"] {
        background: var(--apple-surface) !important;
        border: 1px solid var(--apple-border) !important;
        border-left: 4px solid var(--apple-blue) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--apple-text-primary) !important;
        box-shadow: var(--shadow-card) !important;
    }

    /* Apple Pastel Pill Badges */
    .clue-badge {
        display: inline-flex;
        align-items: center;
        padding: 5px 13px;
        border-radius: var(--radius-pill);
        font-family: var(--font-apple);
        font-size: 0.80rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        transition: var(--transition-apple);
        letter-spacing: -0.01em;
    }

    .clue-badge:hover {
        transform: translateY(-1px);
    }

    .badge-left {
        background: #EBF5FF;
        color: #0071E3;
        border: 1px solid #CCE4FF;
    }

    .badge-right {
        background: #FFF4E6;
        color: #E06C00;
        border: 1px solid #FFE0B2;
    }

    .badge-cat {
        background: #F4EFFF;
        color: #5856D6;
        border: 1px solid #E1D4FF;
    }

    /* Folium Map Container in Clean Apple Frame */
    iframe {
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--apple-border) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        width: 100% !important;
        display: block !important;
        transition: var(--transition-apple);
    }

    iframe:hover {
        border-color: #C7C7CC !important;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.09) !important;
    }

    /* Image Element Frame */
    [data-testid="stImage"] img {
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--apple-border) !important;
        box-shadow: var(--shadow-card) !important;
    }

    /* Clean Subtle Dividers */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--apple-border) !important;
        margin: 24px 0 !important;
    }

    /* Radio Buttons in Card Group */
    div[data-testid="stRadio"] > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        border-radius: 12px !important;
        padding: 8px 14px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }

    div[data-testid="stRadio"] label {
        font-family: var(--font-apple);
        font-size: 0.92rem;
        color: var(--apple-text-primary) !important;
        transition: var(--transition-apple);
    }

    div[data-testid="stRadio"] label:hover {
        color: var(--apple-blue) !important;
    }

    /* Spinner */
    [data-testid="stSpinner"] > div {
        border-top-color: var(--apple-blue) !important;
    }

    /* Accessibility */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    /* Apple Hierarchical Geographic Breadcrumb */
    .breadcrumb-bar {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        background: #FFFFFF;
        border: 1px solid var(--apple-border);
        border-radius: var(--radius-pill);
        padding: 7px 16px;
        margin-bottom: 14px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
    }
    .bc-node {
        font-family: var(--font-apple);
        font-size: 0.83rem;
        font-weight: 500;
        color: var(--apple-text-secondary);
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .bc-node b {
        color: var(--apple-text-primary);
        font-weight: 600;
    }
    .bc-node.active {
        color: var(--apple-blue);
        font-weight: 600;
    }
    .bc-node.active b {
        color: var(--apple-blue);
    }
    .bc-sep {
        color: #C7C7CC;
        font-size: 0.8rem;
        user-select: none;
    }

    /* Apple GeoScore Benchmark Card */
    .geo-score-card {
        background: #FFFFFF;
        border: 1px solid #D2E4F9;
        border-left: 4px solid var(--apple-blue);
        border-radius: var(--radius-card);
        padding: 14px 18px;
        box-shadow: var(--shadow-card);
        margin: 12px 0 16px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .score-title {
        font-family: var(--font-apple);
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--apple-text-secondary);
    }
    .score-pts {
        font-family: var(--font-apple);
        font-size: 1.55rem;
        font-weight: 700;
        color: var(--apple-text-primary);
        letter-spacing: -0.02em;
    }
    .score-badge {
        font-family: var(--font-apple);
        font-size: 0.82rem;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: var(--radius-pill);
        background: #EBF5FF;
        color: var(--apple-blue);
        border: 1px solid #CCE4FF;
    }

    /* Geo Clue Inspector Card */
    .clue-inspector-card {
        background: #FFFFFF;
        border: 1px solid var(--apple-border);
        border-radius: var(--radius-card);
        padding: 14px 18px;
        box-shadow: var(--shadow-card);
        margin: 12px 0;
    }
    .clue-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 7px 0;
        border-bottom: 1px solid #F2F2F7;
        font-size: 0.86rem;
    }
    .clue-row:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    .clue-label {
        font-weight: 600;
        color: var(--apple-text-primary);
        font-size: 0.84rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .clue-val {
        color: var(--apple-blue);
        font-weight: 600;
        font-size: 0.84rem;
        text-align: right;
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

GEO_CLUE_DEFINITIONS = [
    (
        "🌿 Vegetation & Flora",
        [
            ("Tropical palms & lush foliage", "tropical coconut palms banana trees lush green monsoon foliage"),
            ("Arid scrub & desert sand", "arid desert landscape dry red sand sparse scrub dry rocky terrain"),
            ("Temperate meadows & deciduous woods", "temperate green agricultural fields deciduous forest pastures"),
            ("Alpine conifers & snow peaks", "alpine evergreen pine conifers rugged mountain peaks cool climate"),
            ("Coastal shoreline & ocean water", "coastal beach shoreline ocean waves maritime coastline")
        ]
    ),
    (
        "🛣️ Road & Surface",
        [
            ("Asphalt with white markings", "paved asphalt road with white pavement line markings"),
            ("Asphalt with yellow markings", "paved asphalt road with yellow pavement line markings"),
            ("Unpaved dirt / gravel track", "unpaved dirt gravel rural country road or mud trail"),
            ("Historic stone / cobblestone", "historic cobblestone stone paved ancient alley street")
        ]
    ),
    (
        "🚗 Traffic Flow Hint",
        [
            ("Left-hand drive layout", "left-hand drive traffic driving on the left side of the road"),
            ("Right-hand drive layout", "right-hand drive traffic driving on the right side of the road")
        ]
    ),
    (
        "🏔️ Terrain & Topography",
        [
            ("Mountainous winding hillside", "mountainous terrain winding hillside roads tea estates hills"),
            ("Dense urban commercial cityscape", "dense multi-story modern urban cityscape commercial downtown"),
            ("Rural village settlement", "quiet rural village countryside settlement with small houses"),
            ("Flat open agricultural plains", "flat agricultural crop plains open landscape wide horizon")
        ]
    )
]

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

    # Pre-encode Geo Clue definitions for fast zero-shot probing
    clue_cache = []
    for cat_name, items in GEO_CLUE_DEFINITIONS:
        prompts = [it[1] for it in items]
        t_in = processor(text=prompts, return_tensors="pt", padding=True, truncation=True, max_length=77)
        with torch.no_grad():
            t_out = model.get_text_features(input_ids=t_in["input_ids"])
            t_raw = t_out.pooler_output if hasattr(t_out, "pooler_output") else t_out
            t_norm = (t_raw / t_raw.norm(dim=-1, keepdim=True)).cpu()
        clue_cache.append((cat_name, items, t_norm))

    return processor, model, text_embeddings, locations, corrections, adapter, clue_cache

processor, model, text_embeddings, locations, corrections, adapter, clue_cache = load_resources()

# --- Explainable AI: Patch-Level Attention Heatmap ---
def generate_attention_heatmap(image, target_text_embedding):
    """
    Computes patch-level visual similarity with the predicted location embedding.
    Interpolates to original resolution and returns a normalized 2D float heatmap [0, 1].
    """
    inp = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        v_out = model.vision_model(pixel_values=inp["pixel_values"])
        patches = v_out.last_hidden_state[:, 1:, :]  # [1, 576, 1024]
        proj = model.visual_projection(patches)       # [1, 576, 768]
        proj_norm = proj / proj.norm(dim=-1, keepdim=True)

        t_norm = target_text_embedding / target_text_embedding.norm(dim=-1, keepdim=True)
        t_norm = t_norm.to(proj_norm.device)

        sim = torch.matmul(proj_norm, t_norm.T).reshape(1, 1, 24, 24)
        w, h = image.size
        upsampled = F.interpolate(sim, size=(h, w), mode="bicubic", align_corners=False)
        heat = upsampled.squeeze().cpu().numpy()

        h_min, h_max = heat.min(), heat.max()
        if h_max > h_min:
            heat = (heat - h_min) / (h_max - h_min + 1e-8)
        else:
            heat = np.zeros_like(heat)
    return heat

def blend_heatmap_overlay(image, heat, alpha=0.45):
    """
    Overlays a smooth, high-contrast thermal colormap onto the original photo.
    """
    h = np.clip(heat, 0.0, 1.0)
    r = np.clip(1.5 - np.abs(h * 4.0 - 3.0), 0.0, 1.0)
    g = np.clip(1.5 - np.abs(h * 4.0 - 2.0), 0.0, 1.0)
    b = np.clip(1.5 - np.abs(h * 4.0 - 1.0), 0.0, 1.0)
    rgb_heat = (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)

    im_np = np.array(image.convert("RGB"))
    blended = (im_np * (1.0 - alpha) + rgb_heat * alpha).astype(np.uint8)
    return Image.fromarray(blended)

# --- Automated Geo Clue Detection (Zero-shot StreetCLIP Probe) ---
def detect_geo_clues(image_embedding, clue_cache):
    """
    Probes image representation against GeoGuessr attribute dimensions.
    Returns list of dicts: {"category": ..., "label": ..., "confidence": ...}
    """
    detected = []
    emb = image_embedding.cpu().squeeze(0)
    for cat_name, items, t_norm in clue_cache:
        scores = torch.matmul(t_norm, emb)
        probs = torch.softmax(scores * 18.0, dim=-1).tolist()
        best_idx = int(scores.argmax().item())
        best_label = items[best_idx][0]
        best_conf = probs[best_idx]
        detected.append({
            "category": cat_name,
            "label": best_label,
            "confidence": best_conf
        })
    return detected

# --- Local EXIF GPS Ground-Truth Extractor ---
def extract_exif_gps(image):
    """
    Extracts authentic GPS coordinates from image EXIF metadata locally.
    Returns (lat, lon) tuple in decimal degrees or None.
    """
    try:
        exif = image.getexif()
        if not exif:
            return None
        gps_ifd = exif.get_ifd(0x8825)
        if not gps_ifd or 2 not in gps_ifd or 4 not in gps_ifd:
            return None

        def to_deg(dms):
            if isinstance(dms, (int, float)):
                return float(dms)
            d, m, s = dms
            return float(d) + float(m) / 60.0 + float(s) / 3600.0

        lat = to_deg(gps_ifd[2])
        if gps_ifd.get(1) == 'S':
            lat = -lat
        lon = to_deg(gps_ifd[4])
        if gps_ifd.get(3) == 'W':
            lon = -lon

        if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0:
            return (lat, lon)
    except Exception:
        pass
    return None

def calc_geoguessr_score(distance_km):
    """
    Official GeoGuessr exponential scoring curve (0 to 5,000 points).
    Score = 5000 * exp(-distance / 2000 km)
    """
    return int(max(0, min(5000, 5000.0 * np.exp(-distance_km / 2000.0))))

# --- Hierarchical Geographic Aggregation ---
def compute_hierarchical_rollup(ranked_candidates):
    """
    Aggregates top candidate confidences by Country and Region.
    """
    country_weights = {}
    region_weights = {}
    for item in ranked_candidates:
        c = item.get("country", "Unknown")
        r = item.get("region", "")
        p = item.get("confidence", 0.0)
        country_weights[c] = country_weights.get(c, 0.0) + p
        if r:
            reg_key = f"{r}, {c}" if c and c != "Unknown" else r
            region_weights[reg_key] = region_weights.get(reg_key, 0.0) + p

    top_country = max(country_weights.items(), key=lambda x: x[1]) if country_weights else ("Unknown", 0.0)
    top_region = max(region_weights.items(), key=lambda x: x[1]) if region_weights else ("", 0.0)
    return top_country, top_region

# --- Canonical Reference Exemplar Finder ---
def find_reference_exemplar(location_name):
    """
    Finds a canonical reference image from the local Imgs/ repository matching the location.
    """
    if not os.path.exists("Imgs"):
        return None
    loc_clean = location_name.lower().replace(",", " ").replace("-", " ")
    tokens = [t.strip() for t in loc_clean.split() if len(t.strip()) > 2 and t.strip() not in {"the", "and", "near", "district", "town", "city"}]

    best_img = None
    best_score = 0
    for fname in os.listdir("Imgs"):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        fn_clean = fname.lower().replace(".jpg", "").replace(".jpeg", "").replace(".png", "").replace("_", " ").replace("-", " ")
        fn_tokens = set(fn_clean.split())
        matched = [t for t in tokens if t in fn_tokens]
        score = len(matched)
        if score > best_score and score >= 2:
            best_score = score
            best_img = fname

    if best_img:
        return os.path.join("Imgs", best_img)
    return None

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
    return ranked, image_embedding

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
    # Extract image embedding fingerprint using the exact same multi-scale TTA & Adapter as inference
    img_emb = extract_visual_representation(image).cpu().squeeze(0)

    # 1. Register in Visual Correction Cache (prevent duplicate image fingerprints)
    if corrections_list is None:
        corrections_list = []
    
    matched_corr_idx = None
    for c_i, c_item in enumerate(corrections_list):
        c_emb = c_item["embedding"].to(img_emb.device)
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

    # 2. Check if location already exists
    norm_target = target_location_name.strip().lower()
    existing_idx = None
    for idx, loc in enumerate(current_locations):
        if loc["name"].strip().lower() == norm_target:
            existing_idx = idx
            break

    # 3. Compute or preserve ensembled text prompt embedding
    if existing_idx is not None and not visual_clues:
        # Validating an already-correct place: preserve the rich ensembled embedding and original prompt!
        updated_text_vec = current_embeddings[existing_idx:existing_idx+1]
        target_prompt = current_locations[existing_idx].get("prompt", f"a street view photo in {target_location_name.strip()}")
    else:
        # When new clues are provided or registering a new place, build a 3-way ensemble (50% visual, 30% canonical, 20% geo)
        prompt_vis = (
            f"a street view photo in {target_location_name.strip()}, {visual_clues}"
            if visual_clues
            else (current_locations[existing_idx].get("prompt") if existing_idx is not None else f"a street view photo in {target_location_name.strip()}")
        )
        prompt_can = f"a street view photo in {target_location_name.strip()}"
        prompt_geo = f"a photo taken in {target_location_name.strip()}, {country or ''}"

        with torch.no_grad():
            t_in = processor(text=[prompt_vis, prompt_can, prompt_geo], return_tensors="pt", padding=True, truncation=True, max_length=77)
            t_out = model.get_text_features(input_ids=t_in["input_ids"])
            t_raw = t_out.pooler_output if hasattr(t_out, "pooler_output") else t_out
            t_norm = t_raw / t_raw.norm(dim=-1, keepdim=True)
            comb_t = 0.50 * t_norm[0:1] + 0.30 * t_norm[1:2] + 0.20 * t_norm[2:3]
            updated_text_vec = (comb_t / comb_t.norm(dim=-1, keepdim=True)).cpu()
        target_prompt = prompt_vis

    # 4. Update location index with STRICT DEDUPLICATION
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
st.markdown("<p class='main-subtitle'>Pins street view and outdoor landscape photos down to <b>exact global countries, Indian states, and Kerala village micro-regions</b> using multi-scale vision AI and satellite telemetry.</p>", unsafe_allow_html=True)

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
    img_source_key = None
    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            image = Image.open(uploaded_file).convert("RGB")
            img_source_key = f"upload_{uploaded_file.name}_{uploaded_file.size}"
        except Exception:
            st.error("Could not read uploaded image. Please ensure it is a valid JPG or PNG file.")
            image = None
    elif selected_sample != "(Upload your own image)":
        clean_filename = selected_sample.split(" ", 1)[1]
        sample_path = os.path.join("Imgs", clean_filename)
        if os.path.exists(sample_path):
            image = Image.open(sample_path).convert("RGB")
            img_source_key = f"sample_{clean_filename}"

    # Reset stale prediction if active image changed or was removed
    if st.session_state.get("active_img_source") != img_source_key:
        st.session_state["active_img_source"] = img_source_key
        if "ranked" in st.session_state:
            del st.session_state["ranked"]
        if "last_image" in st.session_state:
            del st.session_state["last_image"]
        if "image_embedding" in st.session_state:
            del st.session_state["image_embedding"]
        if "heat_cache" in st.session_state:
            del st.session_state["heat_cache"]

    if image is not None:
        if "ranked" in st.session_state and len(st.session_state["ranked"]) > 0:
            show_attention = st.checkbox("👁️ Show AI Vision Focus (Attention Heatmap)", value=False)
            if show_attention:
                heat_alpha = st.slider("Heatmap Intensity:", min_value=0.20, max_value=0.85, value=0.45, step=0.05)
                top_name = st.session_state["ranked"][0]["name"]
                if st.session_state.get("heat_cache_key") != f"{img_source_key}_{top_name}":
                    top_idx = next((i for i, l in enumerate(locations) if l["name"] == top_name), 0)
                    t_emb = text_embeddings[top_idx:top_idx+1]
                    st.session_state["heat_cache"] = generate_attention_heatmap(image, t_emb)
                    st.session_state["heat_cache_key"] = f"{img_source_key}_{top_name}"

                blended_im = blend_heatmap_overlay(image, st.session_state["heat_cache"], alpha=heat_alpha)
                st.image(blended_im, caption=f"🔥 StreetCLIP Vision Focus on {top_name.split(',')[0]}", use_container_width=True)
            else:
                st.image(image, caption="Query Photo", use_container_width=True)
        else:
            st.image(image, caption="Query Photo", use_container_width=True)

        predict_btn = st.button("📍 Geoguess & Analyze Location", type="primary", use_container_width=True)

with col_right:
    st.subheader("2. AI GeoGuessr Analysis")

    if image is not None and "predict_btn" in locals() and predict_btn:
        with st.spinner(f"Running multi-scale vision inference across {len(locations)} locations..."):
            ranked, img_emb = predict_location(image, text_embeddings, locations, corrections_list=corrections, category_filter=selected_scope)
            st.session_state["ranked"] = ranked
            st.session_state["last_image"] = image
            st.session_state["image_embedding"] = img_emb

    if "ranked" in st.session_state and len(st.session_state["ranked"]) > 0:
        ranked = st.session_state["ranked"]
        top_pick = ranked[0]
        top_lat = top_pick["lat"]
        top_lon = top_pick["lon"]
        img_emb = st.session_state.get("image_embedding", None)
        if img_emb is None and "last_image" in st.session_state:
            img_emb = extract_visual_representation(st.session_state["last_image"])

        # URLs for Google Maps and Google Earth
        gmaps_url, gearth_url, gstreet_url = get_map_urls(top_lat, top_lon)

        # 1. Hierarchical Geographic Breadcrumb
        top_country, top_region = compute_hierarchical_rollup(ranked)
        c_name, c_conf = top_country
        r_name, r_conf = top_region
        reg_clean = r_name.split(",")[0].strip() if "," in r_name else r_name
        st.markdown(f"""
        <div class="breadcrumb-bar">
            <span class="bc-node">🌍 <b>Global</b></span>
            <span class="bc-sep">›</span>
            <span class="bc-node">🚩 <b>{c_name}</b> <small>({c_conf*100:.1f}%)</small></span>
            <span class="bc-sep">›</span>
            <span class="bc-node">📍 <b>{reg_clean}</b> <small>({r_conf*100:.1f}%)</small></span>
            <span class="bc-sep">›</span>
            <span class="bc-node active">🎯 <b>{top_pick['name'].split(',')[0]}</b> <small>({top_pick['confidence']*100:.1f}%)</small></span>
        </div>
        """, unsafe_allow_html=True)

        # 2. Local EXIF GPS Ground-Truth Auto-Benchmarking
        exif_coords = extract_exif_gps(image)
        benchmark_coords = None
        benchmark_source = None
        dist_err = None

        if exif_coords is not None:
            benchmark_coords = exif_coords
            benchmark_source = "Camera GPS EXIF"
            dist_err = geodesic((top_lat, top_lon), benchmark_coords).kilometers
            score = calc_geoguessr_score(dist_err)
            badge_text = "🎯 Pinpoint (<25km)" if dist_err < 25 else ("🌟 Regional (<150km)" if dist_err < 150 else "✈️ Continental")
            st.markdown(f"""
            <div class="geo-score-card">
                <div>
                    <div class="score-title">🏆 GeoGuessr Match Score ({benchmark_source})</div>
                    <div class="score-pts">{score:,} <span style="font-size:0.95rem; font-weight:500; color:var(--apple-text-secondary);">/ 5,000 pts</span></div>
                    <div style="font-size:0.83rem; color:var(--apple-text-secondary); margin-top:3px;">
                        Error: <b style="color:var(--apple-text-primary);">{dist_err:.1f} km</b> from authentic GPS coordinates
                    </div>
                </div>
                <div>
                    <span class="score-badge">{badge_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='margin-bottom: 12px;'><span class='score-badge' style='background:#F2F2F7; color:#6E6E73; border-color:#E5E5EA;'>🛡️ Blind Evaluation: 100% Vision-Based Prediction (No EXIF GPS in photo)</span></div>", unsafe_allow_html=True)
            with st.expander("🎯 Benchmark AI Against Known Ground Truth", expanded=False):
                st.caption("Select the known location where this photo was taken to calculate the model's distance error and GeoGuessr score:")
                bench_choice = st.selectbox("Ground Truth Location:", [l["name"] for l in locations], key="bench_gt_loc")
                bench_loc = next((l for l in locations if l["name"] == bench_choice), None)
                if bench_loc:
                    dist_err = geodesic((top_lat, top_lon), (bench_loc["lat"], bench_loc["lon"])).kilometers
                    score = calc_geoguessr_score(dist_err)
                    badge_text = "🎯 Pinpoint (<25km)" if dist_err < 25 else ("🌟 Regional (<150km)" if dist_err < 150 else "✈️ Continental")
                    st.markdown(f"""
                    <div class="geo-score-card">
                        <div>
                            <div class="score-title">🎯 Manual Ground Truth Score</div>
                            <div class="score-pts">{score:,} <span style="font-size:0.95rem; font-weight:500; color:var(--apple-text-secondary);">/ 5,000 pts</span></div>
                            <div style="font-size:0.83rem; color:var(--apple-text-secondary); margin-top:3px;">
                                Error: <b style="color:var(--apple-text-primary);">{dist_err:.1f} km</b> to {bench_choice.split(',')[0]}
                            </div>
                        </div>
                        <div>
                            <span class="score-badge">{badge_text}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    benchmark_coords = (bench_loc["lat"], bench_loc["lon"])
                    benchmark_source = "Selected Benchmark"

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

        # Dynamic Confidence Uncertainty Radius Circle
        uncert_km = int(max(15, min(650, (1.0 - top_pick["confidence"]) * 750)))
        folium.Circle(
            location=[top_lat, top_lon],
            radius=uncert_km * 1000,
            color="#0071E3",
            weight=1.5,
            fill=True,
            fill_color="#0071E3",
            fill_opacity=0.12,
            tooltip=f"Confidence Margin: ±{uncert_km} km"
        ).add_to(m)

        # Alternative Candidate Flight Lines (Top 2 & 3)
        for alt in ranked[1:3]:
            alt_dist = geodesic((top_lat, top_lon), (alt["lat"], alt["lon"])).kilometers
            folium.PolyLine(
                locations=[[top_lat, top_lon], [alt["lat"], alt["lon"]]],
                color="#5856D6",
                weight=1.5,
                dash_array="5, 8",
                opacity=0.6,
                tooltip=f"Alternative: {alt['name']} ({alt_dist:.0f} km away)"
            ).add_to(m)

        # Benchmark Ground-Truth Marker & Distance Error Line
        if benchmark_coords is not None and dist_err is not None:
            folium.Marker(
                [benchmark_coords[0], benchmark_coords[1]],
                popup=f"🎯 Ground Truth ({benchmark_source})",
                icon=folium.Icon(color="green", icon="ok-sign")
            ).add_to(m)
            folium.PolyLine(
                locations=[[top_lat, top_lon], [benchmark_coords[0], benchmark_coords[1]]],
                color="#FF3B30",
                weight=2.5,
                dash_array="6, 8",
                tooltip=f"Distance Error: {dist_err:.1f} km"
            ).add_to(m)

        # Add top 5 ranked markers with custom popups including Google Earth links
        for i, item in enumerate(ranked[:5], start=1):
            color = "red" if i == 1 else ("orange" if i == 2 else "blue")
            pin_icon = "star" if i == 1 else "info-sign"
            m_gmaps, m_earth, _ = get_map_urls(item["lat"], item["lon"])
            
            popup_html = f"""
            <div style='font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text",sans-serif; min-width:210px; background:#FFFFFF; color:#1D1D1F; padding:12px 14px; border-radius:12px; border:1px solid #E5E5EA; box-shadow:0 8px 24px rgba(0,0,0,0.12);'>
                <b style='font-size:13px; color:#1D1D1F; font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display",sans-serif; letter-spacing:-0.01em;'>#{i} {item['name']}</b><br/>
                <span style='color:#86868B; font-size:11px;'>Confidence: <b style='color:#1D1D1F;'>{item['confidence']*100:.1f}%</b></span><br/>
                <span style='color:#6E6E73; font-size:11px;'>Driving: <b style='color:#1D1D1F;'>{item['driving_side']}</b></span><br/>
                <hr style='margin:8px 0; border:none; height:1px; background:#E5E5EA;'/>
                <a href='{m_gmaps}' target='_blank' style='color:#0071E3; font-weight:600; text-decoration:none; margin-right:10px; font-size:11.5px;'>📍 Google Maps</a>
                <a href='{m_earth}' target='_blank' style='color:#34C759; font-weight:600; text-decoration:none; font-size:11.5px;'>🌐 Google Earth</a>
            </div>
            """
            
            folium.Marker(
                [item["lat"], item["lon"]],
                popup=folium.Popup(popup_html, max_width=280),
                icon=folium.Icon(color=color, icon=pin_icon)
            ).add_to(m)

        folium.LayerControl(position="topright").add_to(m)
        st_folium(m, use_container_width=True, height=400)

        # Automated Geo Detective Clue Inspector (Feature 2)
        st.markdown("#### 🕵️ GeoGuessr Detective Breakdown")
        if img_emb is not None:
            clue_results = detect_geo_clues(img_emb, clue_cache)
            st.markdown("""<div class="clue-inspector-card">""", unsafe_allow_html=True)
            for cr in clue_results:
                st.markdown(f"""
                <div class="clue-row">
                    <span class="clue-label">{cr['category']}</span>
                    <span class="clue-val">{cr['label']} <small style="color:var(--apple-text-secondary); font-weight:normal;">({cr['confidence']*100:.1f}%)</small></span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f"<span class='clue-badge badge-cat'>🏷️ {top_pick['category']}</span>"
            f"<span class='clue-badge badge-left'>{driving_icon}</span>"
            f"<span class='clue-badge badge-cat'>📍 Lat: {top_lat:.3f}, Lon: {top_lon:.3f}</span>",
            unsafe_allow_html=True
        )
        if top_pick.get("prompt"):
            st.caption(f"**Visual Meta Clues:** *{top_pick['prompt']}*")

        # Canonical Reference Exemplar Comparison (Feature 3)
        ref_image_path = find_reference_exemplar(top_pick["name"])
        if ref_image_path and os.path.exists(ref_image_path):
            st.markdown("#### 🖼️ Canonical Reference Comparison")
            st.caption(f"Comparing your query photo against our ground-truth reference scene for **{top_pick['name']}**:")
            c_orig, c_ref = st.columns(2)
            with c_orig:
                st.image(image, caption="Your Query Photo", use_container_width=True)
            with c_ref:
                ref_im = Image.open(ref_image_path).convert("RGB")
                st.image(ref_im, caption=f"Ground-Truth Reference: {os.path.basename(ref_image_path).replace('_', ' ').replace('.jpg', '')}", use_container_width=True)

        # Top 5 Candidates List with Direct Maps/Earth shortcuts
        st.markdown("#### 🏆 Top Ranked Candidates")
        for i, item in enumerate(ranked[:5], start=1):
            with st.container(border=True):
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
                    f"<div style='background:#F2FAF5; border:1px solid #C6EED8; border-left:4px solid #34C759; padding:12px 16px; border-radius:12px; margin:8px 0 12px 0; box-shadow:0 2px 10px rgba(0,0,0,0.03);'>"
                    f"<b style='color:#1D1D1F; font-family:-apple-system,BlinkMacSystemFont,\"SF Pro Text\",sans-serif;'>Selected Target:</b> <span style='color:#0071E3; font-weight:600;'>{matched_loc['name']}</span><br/>"
                    f"<span style='color:#6E6E73; font-size:0.88rem;'>Category: <code style='background:#EBF5FF; color:#0071E3; border:1px solid #CCE4FF;'>{reg_category}</code> | Country: <b style='color:#1D1D1F;'>{reg_country}</b> | Region: <b style='color:#1D1D1F;'>{reg_region}</b> | Driving: <b style='color:#34C759;'>{reg_driving}</b></span><br/>"
                    f"<span style='color:#248A3D; font-size:0.82rem; font-weight:600;'>🛡️ Duplicate Protection Active: Updates existing place in-place without duplicating.</span>"
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
                    new_ranked, new_emb = predict_location(
                        st.session_state["last_image"],
                        new_embeddings,
                        new_locations,
                        corrections_list=corrections,
                        category_filter=selected_scope
                    )

                    st.session_state["ranked"] = new_ranked
                    st.session_state["image_embedding"] = new_emb
                    action_text = "Registered new location" if was_added else "Updated existing location in-place (no duplicate)"
                    st.session_state["just_corrected"] = {
                        "old": old_top_name,
                        "new": new_ranked[0]["name"],
                        "conf": new_ranked[0]["confidence"],
                        "action": action_text
                    }
                    st.rerun()

    elif image is not None:
        st.info("💡 **Photo loaded!** Click **'📍 Geoguess & Analyze Location'** on the left to run multi-scale vision inference.")
    else:
        st.caption("Upload an outdoor or street photo or select a pre-loaded challenge sample to begin.")