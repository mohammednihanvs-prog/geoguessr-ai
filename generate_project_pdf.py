import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ==============================================================================
# Numbered Canvas for "Page X of Y" and Running Headers/Footers
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0369A1"))

        if self._pageNumber > 1:
            # Top Running Header
            self.drawString(54, 752, "GEOGUESSR AI &mdash; ARCHITECTURAL & SYSTEM REFERENCE")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(558, 752, "StreetCLIP + Residual Vision Adapter + Streamlit HUD")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 744, 558, 744)

        # Bottom Running Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 44, 558, 44)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "GeoGuessr AI Platform Guide &bull; 100% Offline Machine Learning &bull; Zero External APIs")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


# ==============================================================================
# UI Component Helpers: Callout Boxes, Metric Cards, Clean Badges
# ==============================================================================
def make_callout(title, body_text, col_hex="#0284C7", bg_hex="#F0F9FF", width=504):
    content = [
        Paragraph(f"<b><font color='{col_hex}'>{title}</font></b>", ParagraphStyle(
            'CTitle', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor(col_hex)
        )),
        Spacer(1, 2.5),
        Paragraph(body_text, ParagraphStyle(
            'CBody', fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor("#1E293B")
        ))
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(col_hex)),
        ('LINEBEFORE', (0,0), (-1,-1), 3.5, colors.HexColor(col_hex)),
    ]))
    return t

def make_metric_card(val, label, subtext, width=120, height=52, border_hex="#0284C7"):
    content = [
        Paragraph(f"<b><font color='{border_hex}' size='13'>{val}</font></b>", ParagraphStyle('MVal', fontName='Helvetica-Bold', fontSize=13, leading=15, alignment=1)),
        Spacer(1, 1),
        Paragraph(f"<b><font color='#0F172A' size='7.5'>{label}</font></b>", ParagraphStyle('MLbl', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, alignment=1)),
        Paragraph(f"<font color='#64748B' size='6.5'>{subtext}</font>", ParagraphStyle('MSub', fontName='Helvetica', fontSize=6.5, leading=8.5, alignment=1))
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_hex)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    return t


def generate_pdf(output_path="GeoGuessr_AI_Complete_Project_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A")
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#475569")
    )
    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0369A1"),
        spaceBefore=7,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        firstLineIndent=-10,
        spaceAfter=2.5
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_cell_code = ParagraphStyle(
        'TableCellCode',
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#0369A1")
    )
    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER & EXECUTIVE SUMMARY
    # =========================================================================
    banner_text = [
        Paragraph("<b><font color='#0284C7'>GEOGUESSR AI &mdash; SYSTEM ARCHITECTURE & IMPLEMENTATION GUIDE</font></b>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor("#0284C7"))),
        Spacer(1, 2),
        Paragraph("Global &amp; Hyper-Local Vision AI Localization Platform", title_style),
        Spacer(1, 3),
        Paragraph("An end-to-end guide detailing language choices, foundation vision-language models, residual neural adaptation, multi-scale Test-Time Augmentation (TTA), modern cyber-cartography frontend, and offline geographic knowledge bases.", subtitle_style)
    ]
    banner_t = Table([[banner_text]], colWidths=[504])
    banner_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('LINEBEFORE', (0,0), (-1,-1), 4, colors.HexColor("#0284C7")),
    ]))
    story.append(banner_t)
    story.append(Spacer(1, 8))

    # Metric Tiles Row
    m1 = make_metric_card("479 Spots", "Massive Database", "104 Nations + 185 Villages", 121, border_hex="#0284C7")
    m2 = make_metric_card("StreetCLIP", "Vision Transformer", "768-dim Latent Space", 121, border_hex="#059669")
    m3 = make_metric_card("0.03s", "Inference Speed", "Cosine Matrix Fast Path", 121, border_hex="#7C3AED")
    m4 = make_metric_card("100% Local", "Zero External API", "Private, Free &amp; Offline", 121, border_hex="#D97706")

    metrics_table = Table([[m1, m2, m3, m4]], colWidths=[126, 126, 126, 126])
    metrics_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 8))

    # Executive Overview
    story.append(Paragraph("1. Executive Summary &amp; Core Problem Statement", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))
    story.append(Paragraph(
        "Human GeoGuessr champions locate arbitrary street scenes in seconds by observing subtle environmental signatures: road paint patterns, driving side conventions, utility pole shapes, soil coloration, climate indicators, and unique regional architecture. Standard computer vision models fail at this task because they are trained to recognize objects (cars, dogs, trees) rather than geomorphic, infrastructural, and regional clues.",
        body_style
    ))
    story.append(Paragraph(
        "<b>GeoGuessr AI</b> is an engineering breakthrough that models this exact human detective workflow. It pairs <b>StreetCLIP</b> (a specialized vision-language foundation model trained on worldwide street imagery) with a custom <b>Residual Vision Adapter (Tip-Adapter)</b>, a <b>Multi-Crop Test-Time Augmentation (TTA)</b> pipeline, an <b>Automated Micro-Clue Evidence Booster</b>, and an interactive <b>Aero-Orbital Tactical HUD</b>.",
        body_style
    ))

    story.append(Spacer(1, 4))

    # Architecture Flowchart (Structured Flow Diagram Table)
    story.append(Paragraph("High-Level Pipeline &amp; Dataflow Architecture", h2_style))
    flow_data = [
        [
            Paragraph("<b>1. Raw Photo Intake</b><br/><font size='6.5' color='#64748B'>Smartphone / Web / EXIF</font>", table_header),
            Paragraph("<b>2. Multi-Crop TTA</b><br/><font size='6.5' color='#64748B'>4 Sub-Scene Projections</font>", table_header),
            Paragraph("<b>3. StreetCLIP + Adapter</b><br/><font size='6.5' color='#64748B'>768-dim Latent Space</font>", table_header),
            Paragraph("<b>4. Evidence Booster</b><br/><font size='6.5' color='#64748B'>Clues + Memory Bank</font>", table_header),
            Paragraph("<b>5. Geo Resolution</b><br/><font size='6.5' color='#64748B'>Map + XAI + Scoring</font>", table_header)
        ],
        [
            Paragraph("&bull; Auto EXIF Transpose<br/>&bull; Genuine GPS Extracted<br/>&bull; Lanczos Max 1600px<br/>&bull; No metadata wipe", table_cell),
            Paragraph("&bull; Full Context (45%)<br/>&bull; Ground / Asphalt (25%)<br/>&bull; Roadside Poles (15%)<br/>&bull; Horizon Line (15%)", table_cell),
            Paragraph("&bull; ViT-B/16 Vision Model<br/>&bull; Residual Adapter (&alpha;=0.85)<br/>&bull; L2 Unit Normalization<br/>&bull; Sub-sec tensor dot", table_cell),
            Paragraph("&bull; Traffic: Left vs Right<br/>&bull; Soil: Laterite vs Arid<br/>&bull; Road: Yellow vs White<br/>&bull; Human Feedback Sync", table_cell),
            Paragraph("&bull; Esri Satellite + OSM<br/>&bull; Dynamic Error Circle<br/>&bull; ViT Attention Heatmap<br/>&bull; 5,000-Point Score", table_cell)
        ]
    ]
    flow_t = Table(flow_data, colWidths=[100, 101, 101, 101, 101])
    flow_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(flow_t)

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "CORE ARCHITECTURAL PRINCIPLE: 100% LOCAL &amp; ZERO SUBSCRIPTIONS",
        "The entire platform runs completely offline on local CPU or GPU. All geocoding, reverse lookups, image embeddings, spatial attention maps, and distance calculations use local mathematical formulas and pre-cached tensors. No OpenAI tokens, Google Cloud billing, or third-party paid APIs are needed.",
        col_hex="#059669", bg_hex="#F0FDF4"
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: LANGUAGES USED & SOFTWARE STACK
    # =========================================================================
    story.append(Paragraph("2. Languages Used &amp; Software Layer Breakdown", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph(
        "The system coordinates low-level tensor mathematics, geodetic computation, and high-framerate client rendering across four distinct languages:",
        body_style
    ))

    # Languages Table
    lang_data = [
        [Paragraph("Language / Technology", table_header), Paragraph("Role in System", table_header), Paragraph("Key Libraries &amp; Modules", table_header), Paragraph("Technical Highlights &amp; Architecture", table_header)],
        [
            Paragraph("<b>Python 3.11+</b>", table_cell_bold),
            Paragraph("Core AI/ML, backend pipelines, server logic, data engineering", table_cell),
            Paragraph("<font color='#0369A1'>torch, transformers, PIL, numpy, geopy, streamlit, folium</font>", table_cell_code),
            Paragraph("Executes vectorized matrix operations (<b>[1, 768] &times; [768, 479]</b>), multi-scale image slicing, zero-shot probe caching, and sub-millisecond similarity rankings.", table_cell)
        ],
        [
            Paragraph("<b>HTML5 &amp; Modern CSS3</b>", table_cell_bold),
            Paragraph("Aero-Orbital Tactical HUD interface &amp; visual styling", table_cell),
            Paragraph("<font color='#0369A1'>CSS Custom Properties, Keyframe Animations, Google Fonts</font>", table_cell_code),
            Paragraph("Awwwards-level cyber-cartography design, glassmorphic HUD cards, scanlines, responsive clamp() typography, and high-contrast night vision overlays.", table_cell)
        ],
        [
            Paragraph("<b>JavaScript (ES6+)</b>", table_cell_bold),
            Paragraph("Interactive client mapping &amp; live telemetry rendering", table_cell),
            Paragraph("<font color='#0369A1'>Leaflet.js, Folium bridge, HTML Canvas API</font>", table_cell_code),
            Paragraph("Powers dual-layer map switching, dynamic error radius overlays, smooth map pan/zoom transitions, and live flight lines between top candidates.", table_cell)
        ],
        [
            Paragraph("<b>YAML</b>", table_cell_bold),
            Paragraph("Automated DevOps &amp; continuous integration testing", table_cell),
            Paragraph("<font color='#0369A1'>GitHub Actions (.github/workflows/ci.yml)</font>", table_cell_code),
            Paragraph("Runs automated test pipelines on every git push, validating database integrity, model weights, cache parity, and code formatting.", table_cell)
        ]
    ]
    lang_t = Table(lang_data, colWidths=[95, 125, 140, 144])
    lang_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(lang_t)
    story.append(Spacer(1, 10))

    # Python Framework Deep Dive
    story.append(Paragraph("Python AI &amp; Numerical Ecosystem Details", h2_style))
    story.append(Paragraph(
        "• <b>PyTorch (torch &amp; torch.nn):</b> Powers the residual adapter network, L2 vector normalization (<font face='Courier'>x / x.norm()</font>), tensor matrix dot-products, and scaled softmax temperature distribution (<font face='Courier'>sim_scores &times; 35.0</font>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Hugging Face Transformers:</b> Manages automated tokenizer downloads, StreetCLIP processor configuration, and ViT-B/16 visual patch extraction.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Pillow (PIL.Image &amp; PIL.ImageOps):</b> Handles non-destructive raw image loading, EXIF orientation transposing, genuine camera GPS metadata extraction, and Lanczos thumbnail scaling.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>GeoPy (geopy.distance.geodesic):</b> Computes exact ellipsoidal Earth distances in kilometers between the model's coordinate prediction and camera GPS ground truth.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Streamlit (streamlit &amp; streamlit_folium):</b> Lightweight reactive web application framework with session state management and instant multi-component caching.",
        bullet_style
    ))

    story.append(Spacer(1, 8))
    story.append(make_callout(
        "PERFORMANCE NOTE: WHY PYTHON FOR LOW-LATENCY INFERENCE?",
        "While Python is often considered slower than compiled languages, GeoGuessr AI vectorizes all heavy operations into pre-compiled C++/CUDA BLAS routines via PyTorch. Ranking an image against 479 location vectors takes under <b>30 milliseconds</b> on standard CPU hardware.",
        col_hex="#0284C7", bg_hex="#F0F9FF"
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: EXTERNAL MODELS & DEEP LEARNING ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. External AI Models &amp; Neural Foundation Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph(
        "Rather than training a multi-gigabyte computer vision model from scratch on limited hardware, GeoGuessr AI utilizes specialized foundation models tailored for street imagery, augmented by parameter-efficient custom adapters:",
        body_style
    ))

    model_data = [
        [Paragraph("Model / Neural Component", table_header), Paragraph("Source / Authors", table_header), Paragraph("Architecture &amp; Size", table_header), Paragraph("Strategic Purpose in GeoGuessr AI", table_header)],
        [
            Paragraph("<b>StreetCLIP</b><br/><font size='7' color='#0369A1' face='Courier'>geolocal/StreetCLIP</font>", table_cell_bold),
            Paragraph("Stanford University &amp; Haas et al. (Open Source)", table_cell),
            Paragraph("768-dim multimodal embeddings (ViT-B/16 backbone, ~590MB)", table_cell),
            Paragraph("<b>Core Vision-Language Foundation:</b> Fine-tuned specifically on street view images worldwide. Excels at detecting road lines, infrastructure, climate patterns, and architecture where standard CLIP fails completely.", table_cell)
        ],
        [
            Paragraph("<b>OpenAI CLIP ViT-B/16</b><br/><font size='7' color='#0369A1' face='Courier'>openai/clip-vit-base-patch16</font>", table_cell_bold),
            Paragraph("OpenAI Foundation Research", table_cell),
            Paragraph("576 spatial patches (24&times;24 grid), 12 visual transformer layers", table_cell),
            Paragraph("<b>Spatial Attention Extraction:</b> Provides raw patch-level visual tokens before pooling to generate spatial attention heatmaps showing where the AI focused.", table_cell)
        ],
        [
            Paragraph("<b>Residual Vision Adapter</b><br/><font size='7' color='#0369A1' face='Courier'>ResidualAdapter (Custom)</font>", table_cell_bold),
            Paragraph("Custom Built in PyTorch (Tip-Adapter variant)", table_cell),
            Paragraph("Bottleneck: 768 &rarr; 256 &rarr; 768 with GELU &amp; LayerNorm (~1.5MB)", table_cell),
            Paragraph("<b>Parameter-Efficient Fine-Tuning:</b> Fast adaptation with residual blend <i>out = &alpha;&times;x + (1-&alpha;)&times;f(x)</i> (calibrated at &alpha;=0.85) to specialize on local micro-regions without catastrophic forgetting.", table_cell)
        ],
        [
            Paragraph("<b>Zero-Shot Geo Clue Probes</b><br/><font size='7' color='#0369A1' face='Courier'>GEO_CLUE_DEFINITIONS</font>", table_cell_bold),
            Paragraph("Curated Domain Prompt Vectors (Cached)", table_cell),
            Paragraph("4 key dimensions, 15 attribute vectors (sub-millisecond)", table_cell),
            Paragraph("<b>Subtle Hint Detection:</b> Probes visual representations against driving orientation (left/right), road markings (yellow/white lines, dirt), and soil/vegetation profiles.", table_cell)
        ]
    ]
    model_t = Table(model_data, colWidths=[105, 95, 120, 184])
    model_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(model_t)
    story.append(Spacer(1, 10))

    # Mathematical Formulation of Residual Adapter
    story.append(Paragraph("Residual Adapter Formulation &amp; Mathematical Balance", h2_style))
    story.append(Paragraph(
        "Standard fine-tuning of large vision transformers causes <i>catastrophic forgetting</i> &mdash; the model forgets global knowledge when forced to learn subtle local villages. To prevent this, GeoGuessr AI utilizes a residual bottleneck adapter:",
        body_style
    ))
    story.append(Paragraph(
        "<b>Mathematical Formula:</b> &nbsp;&nbsp;&nbsp; <i>x<sub>adapted</sub> = normalize( &alpha; &times; x<sub>clip</sub> + (1 - &alpha;) &times; W<sub>2</sub>( GELU( W<sub>1</sub>( LayerNorm(x<sub>clip</sub>) ) ) ) )</i>",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Input Feature (x<sub>clip</sub>):</b> 768-dimensional unit-normalized visual embedding from StreetCLIP.<br/>"
        "• <b>Bottleneck Compression (W<sub>1</sub>):</b> Projects 768 dimensions down to 256 dimensions with GELU non-linearity.<br/>"
        "• <b>Residual Expansion (W<sub>2</sub>):</b> Re-projects 256 dimensions back to 768 dimensions.<br/>"
        "• <b>Residual Weighting (&alpha; = 0.85):</b> Retains 85% of StreetCLIP's natural zero-shot visual discrimination across all 479 locations, while allowing 15% local fine-tuning flexibility.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "CRITICAL EMPIRICAL LESSON: WHY ALPHA = 0.85 MATTERS",
        "When alpha was set to 0.50, the adapter over-fitted to the few landmark photos it trained on, dragging unfamiliar smartphone shots towards arbitrary trained locations (e.g. Chengannur). Calibrating alpha to 0.85 cured this issue, allowing raw zero-shot generalization to identify diverse scenes (Singapore, Bali, Mysore, and remote Kerala backwaters) with pinpoint precision.",
        col_hex="#D97706", bg_hex="#FFFBEB"
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: FRONTEND, UI & SMARTPHONE HARDENING
    # =========================================================================
    story.append(Paragraph("4. Frontend Experience: Aero-Orbital Tactical HUD", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph(
        "The web interface breaks away from generic AI templates, deploying a custom <b>Aero-Orbital Tactical HUD</b> designed specifically for geospatial immersion and professional cartographic operations:",
        body_style
    ))

    ui_data = [
        [Paragraph("HUD Component", table_header), Paragraph("Implementation Mechanism", table_header), Paragraph("Cartographic &amp; Analytical Value", table_header)],
        [
            Paragraph("<b>Obsidian Void Colorway</b>", table_cell_bold),
            Paragraph("CSS Custom Properties (<font color='#0369A1'>#04060A</font>, Hyper-Cyan <font color='#0369A1'>#00F0FF</font>, Gold <font color='#D97706'>#FFB800</font>)", table_cell),
            Paragraph("Eliminates glare, optimizes dark-mode contrast, and frames satellite imagery with precision aeronautical styling.", table_cell)
        ],
        [
            Paragraph("<b>Dual-Layer Satellite Mapping</b>", table_cell_bold),
            Paragraph("Folium / Leaflet integration with Esri High-Resolution World Imagery + OSM", table_cell),
            Paragraph("Instant 1-click toggle between crisp satellite aerial topography and street-level cartographic road labels.", table_cell)
        ],
        [
            Paragraph("<b>Dynamic Uncertainty Halo</b>", table_cell_bold),
            Paragraph("Circle overlay: <font face='Courier'>radius = max(8, (1-conf)*150) km</font>", table_cell),
            Paragraph("Visualizes AI certainty geographically: high-confidence picks produce tight halos; ambiguous shots show wide search circles.", table_cell)
        ],
        [
            Paragraph("<b>Candidate Flight Lines</b>", table_cell_bold),
            Paragraph("Folium PolyLine connecting Rank 1 pick to Rank 2 &amp; 3 with geodesic lines", table_cell),
            Paragraph("Exposes model decision tension: reveals if the model is debating between two distant continents or two neighboring valleys.", table_cell)
        ],
        [
            Paragraph("<b>Explainable Vision Heatmap</b>", table_cell_bold),
            Paragraph("ViT-B/16 patch spatial cosine similarity projected onto original image pixels", table_cell),
            Paragraph("Reveals exactly which visual features triggered the prediction: yellow curb lines, roof slopes, palm fronds, or mountain ridges.", table_cell)
        ],
        [
            Paragraph("<b>Geographic Breadcrumbs</b>", table_cell_bold),
            Paragraph("Hierarchical confidence rollup: <font face='Courier'>Global &rsaquo; Country &rsaquo; State &rsaquo; Micro-Region</font>", table_cell),
            Paragraph("Shows regional consensus even if exact spot confidence is split across neighboring hamlets.", table_cell)
        ],
        [
            Paragraph("<b>Local EXIF Ground-Truth</b>", table_cell_bold),
            Paragraph("Pillow EXIF GPS IFD tag parsing + Geodesic distance formula + Official GeoGuessr scoring", table_cell),
            Paragraph("Calculates true km error and awards an official <b>0 to 5,000 point score</b> with pinpoint / regional badges completely offline.", table_cell)
        ]
    ]
    ui_t = Table(ui_data, colWidths=[130, 150, 224])
    ui_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ui_t)
    story.append(Spacer(1, 8))

    # Self-Clicked Smartphone Engineering Section
    story.append(Paragraph("5. Mobile &amp; Self-Clicked Smartphone Photo Hardening", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph(
        "Photos taken by users on modern smartphones (iPhone, Android) present unique technical challenges that cause standard vision pipelines to fail silently. GeoGuessr AI includes a specialized mobile preprocessing pipeline:",
        body_style
    ))

    story.append(Paragraph(
        "• <b>Automatic EXIF Transposition (<font face='Courier'>ImageOps.exif_transpose</font>):</b> Smartphone cameras write portrait images with landscape sensor pixels plus an EXIF Orientation tag (tag 6 or 8). Standard libraries load them 90&deg; sideways, confusing the AI and inverting TTA ground crops. The app re-orients the image before tensor conversion.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Pre-Conversion Camera EXIF GPS Extraction:</b> Calling <font face='Courier'>.convert('RGB')</font> creates a fresh buffer that erases EXIF metadata. GeoGuessr AI extracts genuine camera GPS coordinates from the raw file stream first and caches them in session memory.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Lanczos Scale-Capping (Max 1600px):</b> High-resolution 12MP&ndash;48MP mobile photos choke CPU memory during 4-crop TTA bicubic interpolation. Images are cleanly scaled down using Lanczos anti-aliasing to preserve crisp micro-clues while guaranteeing sub-second inference.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Broad Format Support:</b> Seamless ingestion of <font face='Courier'>.jpg</font>, <font face='Courier'>.jpeg</font>, <font face='Courier'>.png</font>, <font face='Courier'>.webp</font>, and <font face='Courier'>.jfif</font> files.",
        bullet_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: KNOWLEDGE BASE & CODEBASE DIRECTORY MAP
    # =========================================================================
    story.append(Paragraph("6. Knowledge Base &amp; Geographic Data Engineering", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph(
        "The model's remarkable localization power stems from its dense, hand-curated knowledge base encompassing <b>479 canonical geographic nodes</b> across 3 distinct tiers:",
        body_style
    ))

    geo_data = [
        [Paragraph("Tier / Geographic Scope", table_header), Paragraph("Count &amp; Coverage", table_header), Paragraph("Embedded Visual Metadata &amp; Geoguessr Meta-Prompts", table_header)],
        [
            Paragraph("<b>Global Tier</b><br/><font size='7' color='#64748B'>World Countries</font>", table_cell_bold),
            Paragraph("<b>104 Countries</b><br/>All 6 inhabited continents", table_cell),
            Paragraph("Driving orientation (Left vs Right), distinctive road line markings (yellow dashed, solid white), utility pole types (ladder, concrete, wooden), bollards, regional license plates, and typical topography.", table_cell)
        ],
        [
            Paragraph("<b>Pan-India Tier</b><br/><font size='7' color='#64748B'>States &amp; Heritage</font>", table_cell_bold),
            Paragraph("<b>All 28 States &amp; 8 UTs</b><br/>+ Major tier-1/2 hubs", table_cell),
            Paragraph("State border highway signs, scripts/languages (Devanagari, Tamil, Bengali, Gurmukhi), arid vs. tropical vegetation, distinctive monument architecture, and highway infrastructure.", table_cell)
        ],
        [
            Paragraph("<b>Kerala Micro-Regions</b><br/><font size='7' color='#64748B'>Dense Villages &amp; Forests</font>", table_cell_bold),
            Paragraph("<b>185 Locations</b><br/>Across all 14 districts", table_cell),
            Paragraph("Micro-regional signatures: high-range tea estates (Vattavada, Kanthalloor, Suryanelli), misty Wayanad hills (Meppadi, Thirunelly), Kuttanad waterways (Pulinkunnu, Kavalam), red laterite soil paths, rubber plantations, and coastal lagoons.", table_cell)
        ]
    ]
    geo_t = Table(geo_data, colWidths=[120, 110, 274])
    geo_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(geo_t)
    story.append(Spacer(1, 8))

    # Repository & File Directory Map
    story.append(Paragraph("7. Codebase Anatomy &amp; Master Directory Map", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    repo_data = [
        [Paragraph("File / Directory", table_header), Paragraph("Category", table_header), Paragraph("Description &amp; Architectural Functionality", table_header)],
        [
            Paragraph("<b>app.py</b>", table_cell_code),
            Paragraph("Primary App", table_cell_bold),
            Paragraph("Main Streamlit application: contains the Aero-Orbital HUD CSS, image intake pipeline, multi-scale TTA, attention heatmap generator, interactive Folium map rendering, and human feedback loop.", table_cell)
        ],
        [
            Paragraph("<b>locations.py</b>", table_cell_code),
            Paragraph("Database", table_cell_bold),
            Paragraph("Master registry of all 479 locations with precise GPS coordinates, regions, categories, driving sides, and descriptive visual prompts.", table_cell)
        ],
        [
            Paragraph("<b>predict.py</b>", table_cell_code),
            Paragraph("CLI Tool", table_cell_bold),
            Paragraph("Headless command-line predictor: evaluates images directly in the terminal, outputs confidence rankings, and exports standalone HTML heatmaps.", table_cell)
        ],
        [
            Paragraph("<b>train_adapter.py</b>", table_cell_code),
            Paragraph("ML Training", table_cell_bold),
            Paragraph("PyTorch training script for the Residual Vision Adapter: tunes adapter weights against exemplar images in Imgs/ with AdamW and Cross-Entropy loss.", table_cell)
        ],
        [
            Paragraph("<b>cache_embeddings.py</b>", table_cell_code),
            Paragraph("Data Pipeline", table_cell_bold),
            Paragraph("Pre-computes and normalizes 768-dim text embeddings for all locations, generating the fast-load embeddings_cache.pt file.", table_cell)
        ],
        [
            Paragraph("<b>Imgs/</b>", table_cell_code),
            Paragraph("Image Assets", table_cell_bold),
            Paragraph("117 canonical reference images: verified street views, tea gardens, backwaters, and recent user-clicked test photos.", table_cell)
        ],
        [
            Paragraph("<b>embeddings_cache.pt</b>", table_cell_code),
            Paragraph("Model Cache", table_cell_bold),
            Paragraph("Pre-computed tensor dictionary allowing cold-start startup in 0.03 seconds without re-encoding prompts on launch.", table_cell)
        ],
        [
            Paragraph("<b>corrections_cache.pt</b>", table_cell_code),
            Paragraph("Memory Bank", table_cell_bold),
            Paragraph("Non-destructive active-learning memory bank storing human feedback corrections for instant recall.", table_cell)
        ]
    ]
    repo_t = Table(repo_data, colWidths=[125, 80, 299])
    repo_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(repo_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: EXECUTION GUIDE, TESTING & SUMMARY SHEET
    # =========================================================================
    story.append(Paragraph("8. Setup, Execution &amp; Testing Quick Start Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph(
        "Getting started with GeoGuessr AI requires only a standard Python environment with PyTorch and Streamlit installed:",
        body_style
    ))

    # Setup Steps Table
    steps_data = [
        [Paragraph("Step", table_header), Paragraph("Action Description", table_header), Paragraph("Terminal Shell Command", table_header)],
        [
            Paragraph("<b>Step 1</b>", table_cell_bold),
            Paragraph("Clone project repository", table_cell),
            Paragraph("<font face='Courier'>git clone https://github.com/mohammednihanvs-prog/geoguessr-ai.git<br/>cd geoguessr-ai</font>", table_cell_code)
        ],
        [
            Paragraph("<b>Step 2</b>", table_cell_bold),
            Paragraph("Create &amp; activate virtual environment", table_cell),
            Paragraph("<font face='Courier'>python -m venv venv<br/>.\\venv\\Scripts\\activate   # (Windows)<br/>source venv/bin/activate  # (Linux/macOS)</font>", table_cell_code)
        ],
        [
            Paragraph("<b>Step 3</b>", table_cell_bold),
            Paragraph("Install required dependencies", table_cell),
            Paragraph("<font face='Courier'>pip install -r requirements.txt</font>", table_cell_code)
        ],
        [
            Paragraph("<b>Step 4</b>", table_cell_bold),
            Paragraph("Launch the Interactive Web HUD", table_cell),
            Paragraph("<font face='Courier'>streamlit run app.py</font><br/><font size='6.5' color='#059669'>Opens http://localhost:8501 automatically</font>", table_cell_code)
        ],
        [
            Paragraph("<b>Step 5</b>", table_cell_bold),
            Paragraph("Run standalone headless prediction", table_cell),
            Paragraph("<font face='Courier'>python predict.py</font><br/><font size='6.5' color='#64748B'>Outputs rankings to console + world_heatmap.html</font>", table_cell_code)
        ],
        [
            Paragraph("<b>Step 6</b>", table_cell_bold),
            Paragraph("Trigger automated 1-click self-training", table_cell),
            Paragraph("<font face='Courier'>python train_adapter.py</font><br/><font size='6.5' color='#64748B'>Trains Residual Adapter across exemplar images</font>", table_cell_code)
        ]
    ]
    steps_t = Table(steps_data, colWidths=[55, 175, 274])
    steps_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(steps_t)
    story.append(Spacer(1, 8))

    # Summary Checklist Callout
    story.append(Paragraph("9. Master Architecture Specification Sheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=2))

    summary_data = [
        [Paragraph("Dimension", table_header), Paragraph("System Specification &amp; Implementation Details", table_header)],
        [Paragraph("<b>Primary Language</b>", table_cell_bold), Paragraph("Python 3.11+ (Backend, Machine Learning, Data Pipelines, Geodesy)", table_cell)],
        [Paragraph("<b>Frontend Framework</b>", table_cell_bold), Paragraph("Streamlit + Custom Aero-Orbital Tactical HUD (HTML5, Modern CSS3, Google Fonts)", table_cell)],
        [Paragraph("<b>Mapping Engine</b>", table_cell_bold), Paragraph("Folium / Leaflet (Esri High-Res Satellite Imagery + OpenStreetMap Cartography)", table_cell)],
        [Paragraph("<b>Vision Foundation</b>", table_cell_bold), Paragraph("StreetCLIP (geolocal/StreetCLIP) based on ViT-B/16 (590MB)", table_cell)],
        [Paragraph("<b>Adapter Architecture</b>", table_cell_bold), Paragraph("Residual Vision Adapter (Bottleneck 768 &rarr; 256 &rarr; 768, GELU, &alpha;=0.85)", table_cell)],
        [Paragraph("<b>Explainability (XAI)</b>", table_cell_bold), Paragraph("ViT patch-level spatial attention heatmap with bicubic interpolation overlay", table_cell)],
        [Paragraph("<b>Input Ingestion</b>", table_cell_bold), Paragraph("EXIF transpose auto-orientation, EXIF GPS ground-truth preservation, Lanczos max 1600px scaling", table_cell)],
        [Paragraph("<b>Knowledge Scale</b>", table_cell_bold), Paragraph("479 Locations: 104 Countries, 28 Indian States &amp; 8 UTs, 185 Kerala Micro-Regions", table_cell)],
        [Paragraph("<b>Offline Capability</b>", table_cell_bold), Paragraph("100% Local Inference, Zero External API Keys, Zero Subscription Costs", table_cell)]
    ]
    sum_t = Table(summary_data, colWidths=[140, 364])
    sum_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sum_t)
    story.append(Spacer(1, 8))

    story.append(make_callout(
        "CONCLUSION: PRODUCTION-READY GEOSPATIAL INTELLIGENCE",
        "GeoGuessr AI demonstrates how combining specialized vision-language foundation models with domain-informed multi-scale augmentation and parameter-efficient adapters can achieve superhuman geographical deduction while running completely offline on standard commodity hardware.",
        col_hex="#0284C7", bg_hex="#F0F9FF"
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    out_pdf = "GeoGuessr_AI_Complete_Project_Guide.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    generate_pdf(out_pdf)
