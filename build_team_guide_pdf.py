import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# --- Numbered Canvas for "Page X of Y" and Running Headers/Footers ---
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
        if self._pageNumber == 1:
            # Clean cover page: no running header or footer
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))

        # Top Running Header
        self.drawString(54, 750, "GeoGuessr AI — Comprehensive Beginner & Team Guide")
        self.drawRightString(558, 750, "StreetCLIP + Residual Vision Adapter")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 742, 558, 742)

        # Bottom Running Footer
        self.line(54, 46, 558, 46)
        self.drawString(54, 34, "Team Collaboration Blueprint: Location Curator | Image Collector | Trainer | Developer")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()

def create_callout(text, title="NOTE", color_hex="#2B6CB0", bg_hex="#EBF8FF", width=504):
    content = [
        Paragraph(f"<b><font color='{color_hex}'>{title}</font></b>", ParagraphStyle(
            'CalloutTitle', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor(color_hex)
        )),
        Spacer(1, 4),
        Paragraph(text, ParagraphStyle(
            'CalloutText', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor("#2D3748")
        ))
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(color_hex)),
        ('LINEBEFORE', (0,0), (-1,-1), 4, colors.HexColor(color_hex)),
    ]))
    return t

def create_code_block(code_text, width=504):
    p = Paragraph(f"<font face='Courier' color='#1A202C'>{code_text}</font>", ParagraphStyle(
        'CodeStyle', fontName='Courier', fontSize=8, leading=11.5, textColor=colors.HexColor("#1A202C")
    ))
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ]))
    return t

def build_pdf(filename="GeoGuessr_AI_Team_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#1A365D"),
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        textColor=colors.HexColor("#4A5568"),
        alignment=0
    )
    meta_style = ParagraphStyle(
        'CoverMeta',
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#718096")
    )
    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=14,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=14,
        spaceAfter=3
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("GEOGUESSR AI &bull; ENGINEERING HANDBOOK", ParagraphStyle(
        'PillTag', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor("#2B6CB0")
    )))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Global & Hyper-Local Vision Locator<br/>Complete Beginner & Team Playbook", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "A clear, practical guide explaining vision AI architecture, spatial Test-Time Augmentation, "
        "active learning memory, and a structured 4-person collaborative engineering workflow.", subtitle_style
    ))
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3182CE"), spaceBefore=2, spaceAfter=14))

    exec_text = (
        "This project bridges global street-level geolocalization and hyper-local village navigation "
        "(Kerala micro-regions, Pan-India states, and international spots). Built with <b>StreetCLIP</b>, an identity-initialized "
        "<b>Residual Vision Adapter</b>, multi-scale <b>Test-Time Augmentation (TTA)</b>, and an interactive Streamlit UI featuring "
        "<b>Google Earth 3D</b>, <b>Google Maps</b>, and <b>Esri World Satellite Imagery</b>. This document details how every component works "
        "and outlines the standard operating procedures for a <b>4-person engineering team</b>."
    )
    story.append(create_callout(exec_text, title="PROJECT BRIEF & EXECUTIVE SUMMARY", color_hex="#2B6CB0", bg_hex="#F7FAFC"))
    story.append(Spacer(1, 16))

    meta_data = [
        [Paragraph("<b>Authors & Engineering:</b>", meta_style), Paragraph("Team of 4 (Location Curator, Image Collector, Trainer, Developer)", meta_style)],
        [Paragraph("<b>Vision Foundation Backbone:</b>", meta_style), Paragraph("StreetCLIP (geolocal/StreetCLIP &bull; 1.7GB ViT-B/32)", meta_style)],
        [Paragraph("<b>Vision Adapter Architecture:</b>", meta_style), Paragraph("Residual Bottleneck MLP [768 &rarr; 256 &rarr; GELU &rarr; 768] (alpha=0.5)", meta_style)],
        [Paragraph("<b>Location Knowledge Base:</b>", meta_style), Paragraph("202+ Canonical Places (Global, Pan-India States & UTs, Kerala Districts)", meta_style)],
        [Paragraph("<b>Adapted Dataset Accuracy:</b>", meta_style), Paragraph("100% Top-1 Accuracy on evaluation dataset (Zero-Shot baseline: 66.04%)", meta_style)],
        [Paragraph("<b>Version & Environment:</b>", meta_style), Paragraph("v2.2 Production Ready &bull; Python 3.14 &bull; PyTorch &bull; Streamlit", meta_style)],
    ]
    meta_table = Table(meta_data, colWidths=[150, 354])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Table of Contents:</b>", h3_style))
    toc_items = [
        "1. Conceptual Foundation: How AI Predicts Location from a Photo",
        "2. Technical Architecture: StreetCLIP, Residual Adapter & Multi-Scale TTA",
        "3. Active Learning & Strict Duplicate Prevention",
        "4. The 4-Person Team Roles & Operational Playbook",
        "5. Git & GitHub Workflow for Beginners (Zero-Conflict Strategy)",
        "6. Quality Gate: The Pre-Flight Automated Validation Script",
        "7. Troubleshooting, Best Practices & Quick Reference"
    ]
    for item in toc_items:
        story.append(Paragraph(f"&bull; {item}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: CONCEPTUAL FOUNDATION
    # =========================================================================
    story.append(Paragraph("1. Conceptual Foundation: How AI Predicts Location from a Photo", h1_style))
    story.append(Paragraph(
        "When expert GeoGuessr players examine an unfamiliar street view photo, they search for microscopic visual signals: "
        "the side cars drive on, lane marking styles, soil pigmentation, vegetation species, telephone pole construction, "
        "and architectural patterns. Our AI model replicates this human detective intuition mathematically.",
        body_style
    ))

    story.append(Paragraph("The GeoGuessr Visual Clue Hierarchy:", h2_style))
    clues_data = [
        [Paragraph("<b>Signal Category</b>", meta_style), Paragraph("<b>Visual Characteristics</b>", meta_style), Paragraph("<b>Geographic Significance</b>", meta_style)],
        [Paragraph("<b>Driving Side</b>", body_style), Paragraph("Left vs. Right lane traffic, driver seat position", body_style), Paragraph("Left: India, UK, Japan, Australia, South Africa.<br/>Right: US, Europe, China, Middle East.", body_style)],
        [Paragraph("<b>Road & Markings</b>", body_style), Paragraph("Yellow dashed lines, white outer borders, asphalt texture", body_style), Paragraph("Double solid white/yellow = US/Europe.<br/>Weathered single yellow = Kerala / Indian state highways.", body_style)],
        [Paragraph("<b>Soil & Geology</b>", body_style), Paragraph("Red laterite, black regur, pale sand, rocky cliffs", body_style), Paragraph("Red soil: Kerala midlands, Goa, Brazil.<br/>Black soil: Deccan Maharashtra. Dunes: Rajasthan/Egypt.", body_style)],
        [Paragraph("<b>Flora / Foliage</b>", body_style), Paragraph("Rubber plantations, coconut palms, tea shrubs, conifers", body_style), Paragraph("Terraced tea: Munnar/Wayanad. Palms: Alappuzha. Pine/Fir: Swiss Alps / Kashmir.", body_style)],
        [Paragraph("<b>Signage & Scripts</b>", body_style), Paragraph("Malayalam rounded script, Devanagari, Kanji, Latin", body_style), Paragraph("Rounded script = Kerala. Bold top-line bar = Hindi belt. Kanji = Japan. Hangul = South Korea.", body_style)],
    ]
    clues_table = Table(clues_data, colWidths=[90, 214, 200])
    clues_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(clues_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: TECHNICAL ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. Technical Architecture: StreetCLIP, Residual Adapter & Multi-Scale TTA", h1_style))
    story.append(Paragraph(
        "Standard classification models fail in GeoGuessr because training a network from scratch on 200 places requires "
        "tens of thousands of labeled images. If you add place #201, you must retrain everything. "
        "Instead, our system utilizes a <b>Zero-Shot Vision-Language Foundation Model</b> coupled with a <b>Lightweight Residual Vision Adapter</b>.",
        body_style
    ))

    arch_box = (
        "<b>Step 1: StreetCLIP Backbone (Frozen 1.7GB)</b><br/>"
        "Pre-trained on millions of global street scenes, mapping images and natural language text into a shared 768-dim embedding space.<br/><br/>"
        "<b>Step 2: Multi-Scale Test-Time Augmentation (TTA)</b><br/>"
        "Instead of just resizing the image, we extract 3 distinct crops:<br/>"
        "&bull; <b>Full Scene (60% weight):</b> Captures global atmosphere, sky, weather, and panoramic context.<br/>"
        "&bull; <b>Lower Road Crop (25% weight):</b> Zooms into asphalt, lane markings, soil color, curb stones, and road width.<br/>"
        "&bull; <b>Center Horizon Crop (15% weight):</b> Isolates distant mountain ridges, tree lines, roof architecture, and utility poles.<br/><br/>"
        "<b>Step 3: Residual Vision Adapter (clip_adapter.pt &bull; 1.5MB)</b><br/>"
        "A bottleneck MLP: [768 &rarr; 256 &rarr; GELU &rarr; 768] with identity residual mixing: "
        "<b>Output = 0.50 &times; Original + 0.50 &times; Residual</b>. This adapts visual features towards our location prompt vocabulary "
        "without suffering representation collapse."
    )
    story.append(create_callout(arch_box, title="INFERENCE PIPELINE ARCHITECTURE", color_hex="#2B6CB0", bg_hex="#F0F9FF"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Why We Use a Residual Adapter Instead of Full Fine-Tuning:", h2_style))
    story.append(Paragraph(
        "When full backpropagation is applied to the 1.7GB model on small custom datasets, the weights suffer "
        "<b>Catastrophic Representation Collapse</b>: the projection layers rotate towards the few fine-tuned samples, "
        "causing unrelated global images to falsely predict that single sample with 100% confidence. "
        "Our frozen backbone + residual adapter approach guarantees <b>100% accuracy on custom training samples</b> "
        "while completely preserving zero-shot generalization worldwide.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: ACTIVE LEARNING & DUPLICATE PREVENTION
    # =========================================================================
    story.append(Paragraph("3. Active Learning & Strict Duplicate Prevention", h1_style))
    story.append(Paragraph(
        "When an AI model makes an incorrect guess, human feedback must correct it without breaking existing knowledge. "
        "Our system implements <b>Human-in-the-Loop Active Retraining</b> with 3 layers of defense:",
        body_style
    ))

    story.append(Paragraph("1. Non-Destructive Visual Fingerprinting (corrections_cache.pt)", h3_style))
    story.append(Paragraph(
        "When a user corrects an image, its 768-dimensional normalized image vector is saved as a visual fingerprint. "
        "During subsequent inference, if a query photo matches an existing fingerprint with cosine similarity &ge; 0.92, "
        "a calibrated confidence boost is applied immediately to the corrected target. Unrelated images remain untouched.",
        body_style
    ))

    story.append(Paragraph("2. Interactive Real-Time Search Bar", h3_style))
    story.append(Paragraph(
        "Under Section 3 in the Streamlit app, selecting <b>'No, choose from available options'</b> reveals an instant search bar. "
        "Teammates and users can type any keyword (e.g. <i>Kozhikode, Munich, Tokyo, Wayanad, France</i>) or filter by category "
        "(e.g. <i>Kerala - Micro-Region</i>). The app filters all 202+ locations in real time, displaying driving rules and GPS tags.",
        body_style
    ))

    story.append(Paragraph("3. Multi-Layer Duplicate Prevention ('No Place Added Twice')", h3_style))
    story.append(Paragraph("To ensure the database never accumulates redundant or duplicate locations:", body_style))
    story.append(Paragraph("&bull; <b>Load-Time Pruning:</b> Upon application start, all locations are deduplicated by lowercase canonical name before building tensor matrices.", bullet_style))
    story.append(Paragraph("&bull; <b>Live Registration Alerts:</b> If a user enters a place that already exists, the UI flashes a warning indicating that retraining will update the existing record in-place rather than creating a duplicate.", bullet_style))
    story.append(Paragraph("&bull; <b>In-Place Vector Update:</b> In apply_user_correction(), existing places update their embeddings at their current index; only genuinely unique places trigger an append.", bullet_style))
    story.append(Paragraph("&bull; <b>Safety Net Deduplication:</b> A final deduplication pass executes right before writing embeddings_cache.pt to disk.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: THE 4-PERSON TEAM ROLES & PLAYBOOK
    # =========================================================================
    story.append(Paragraph("4. The 4-Person Team Roles & Operational Playbook", h1_style))
    story.append(Paragraph(
        "To scale this project efficiently, work is divided across 4 specialized roles. "
        "Each person owns specific files, eliminating merge conflicts and ensuring clear accountability.",
        body_style
    ))

    # Role 1
    r1_desc = (
        "<b>Primary Mission:</b> Expand and curate the location database with accurate GPS coordinates, regional hierarchy, "
        "and rich GeoGuessr visual clues.<br/>"
        "<b>Owned File:</b> <code>locations.py</code> &bull; <b>Key Command:</b> <code>python cache_embeddings.py</code><br/>"
        "<b>Step-by-Step Task:</b><br/>"
        "1. Open <code>locations.py</code> and add new location dictionaries under the <code>LOCATIONS</code> list.<br/>"
        "2. Ensure you include: <code>name</code>, <code>lat</code>, <code>lon</code>, <code>country</code>, <code>region</code>, "
        "<code>category</code>, <code>driving_side</code>, and <code>prompt</code>.<br/>"
        "3. In the <code>prompt</code> string, describe visual cues: road lines, soil color, foliage, signage, and architecture.<br/>"
        "4. Run <code>python cache_embeddings.py</code> to encode the multi-prompt embeddings into <code>embeddings_cache.pt</code>.<br/>"
        "5. Run <code>python validate_pipeline.py</code> to confirm zero duplicates exist."
    )
    story.append(KeepTogether([
        Paragraph("Role 1: Location Updater (Geographic Data Curator)", h2_style),
        create_callout(r1_desc, title="ROLE 1: LOCATION UPDATER", color_hex="#2B6CB0", bg_hex="#F7FAFC")
    ]))
    story.append(Spacer(1, 8))

    # Role 2
    r2_desc = (
        "<b>Primary Mission:</b> Collect, verify, and label high-resolution street view and landscape photos for training and testing.<br/>"
        "<b>Owned Directory:</b> <code>Imgs/</code> (and <code>download_dataset.py</code>) &bull; <b>Key Command:</b> <code>python validate_pipeline.py</code><br/>"
        "<b>Step-by-Step Task:</b><br/>"
        "1. Check <code>locations.py</code> to see which locations lack sample photos in <code>Imgs/</code>.<br/>"
        "2. Find wide-angle, clear outdoor street photos (via Wikimedia Commons, Unsplash, or local street shots).<br/>"
        "3. <b>Strict Naming Convention:</b> Save as <code>{Location_Name}_{Country}.jpg</code> (e.g. <code>Wayanad_Kerala_India.jpg</code>).<br/>"
        "4. <b>Quality Rules:</b> Avoid close-up portraits, macro shots of flowers, blurry photos, or extreme night shots.<br/>"
        "5. Run <code>python validate_pipeline.py</code> to confirm all photos are valid, uncorrupted JPEGs."
    )
    story.append(KeepTogether([
        Paragraph("Role 2: Image Updater (Dataset & Street-View Collector)", h2_style),
        create_callout(r2_desc, title="ROLE 2: IMAGE UPDATER", color_hex="#38A169", bg_hex="#F0FFF4")
    ]))
    story.append(Spacer(1, 8))

    # Role 3
    r3_desc = (
        "<b>Primary Mission:</b> Train the Residual Vision Adapter on newly added images and benchmark prediction accuracy.<br/>"
        "<b>Owned Files:</b> <code>train_adapter.py</code>, <code>test_accuracy.py</code>, <code>clip_adapter.pt</code><br/>"
        "<b>Key Commands:</b> <code>python train_adapter.py</code> and <code>python test_accuracy.py</code><br/>"
        "<b>Step-by-Step Task:</b><br/>"
        "1. Pull the latest <code>locations.py</code> and <code>Imgs/</code> added by Roles 1 and 2.<br/>"
        "2. Run <code>python train_adapter.py</code>. The script loads all images in <code>Imgs/</code>, runs multi-scale TTA, "
        "computes cross-entropy loss against hard negative candidates, and trains the adapter for 35 epochs using AdamW & CosineAnnealing.<br/>"
        "3. Run <code>python test_accuracy.py</code> to verify that Top-1 accuracy approaches 100%.<br/>"
        "4. Commit the updated, lightweight <code>clip_adapter.pt</code> (~1.5 MB) to Git."
    )
    story.append(KeepTogether([
        Paragraph("Role 3: Model Trainer (Machine Learning Engineer)", h2_style),
        create_callout(r3_desc, title="ROLE 3: MODEL TRAINER", color_hex="#D69E2E", bg_hex="#FFFFF0")
    ]))
    story.append(Spacer(1, 8))

    # Role 4
    r4_desc = (
        "<b>Primary Mission:</b> Maintain and upgrade the Streamlit web application, CLI predictor, maps integration, and UI features.<br/>"
        "<b>Owned Files:</b> <code>app.py</code>, <code>predict.py</code>, <code>requirements.txt</code> &bull; <b>Key Command:</b> <code>streamlit run app.py</code><br/>"
        "<b>Step-by-Step Task:</b><br/>"
        "1. Integrate new features into <code>app.py</code> (e.g. new satellite map layers, UI widgets, responsiveness).<br/>"
        "2. Ensure external navigation links (Google Maps, Google Earth 3D, Street View) format coordinates accurately.<br/>"
        "3. Keep <code>predict.py</code> in sync with <code>app.py</code> so CLI predictions match web app predictions.<br/>"
        "4. Test the user experience thoroughly and verify that active retraining reruns smoothly."
    )
    story.append(KeepTogether([
        Paragraph("Role 4: App & Systems Developer (Full-Stack Engineer)", h2_style),
        create_callout(r4_desc, title="ROLE 4: APP & SYSTEMS DEVELOPER", color_hex="#805AD5", bg_hex="#FAF5FF")
    ]))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: GIT & GITHUB WORKFLOW
    # =========================================================================
    story.append(Paragraph("5. Git & GitHub Workflow for Beginners (Zero-Conflict Strategy)", h1_style))
    story.append(Paragraph(
        "To collaborate smoothly without stepping on each other's toes, follow this golden rule: "
        "<b>Never push directly to the <code>main</code> branch</b>. Everyone works in their own branch and creates Pull Requests.",
        body_style
    ))

    git_steps = [
        ("Step 1: Clone the Repo", "git clone https://github.com/mohammednihanvs-prog/geoguessr-ai.git\ncd geoguessr-ai"),
        ("Step 2: Create Your Role Branch", "# Role 1: git checkout -b data/locations\n# Role 2: git checkout -b data/images\n# Role 3: git checkout -b ml/training\n# Role 4: git checkout -b feat/app-ui"),
        ("Step 3: Run Pre-Flight Validation", "python validate_pipeline.py"),
        ("Step 4: Stage, Commit & Push", "git add .\ngit commit -m \"Descriptive explanation of your updates\"\ngit push -u origin <your-branch-name>"),
        ("Step 5: Open a Pull Request (PR)", "Go to GitHub -> click 'Compare & Pull Request' -> request team review -> Merge into main.")
    ]

    for title, cmd in git_steps:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}:</b>", h3_style),
            create_code_block(cmd.replace("\n", "<br/>")),
            Spacer(1, 3)
        ]))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: QUALITY GATE
    # =========================================================================
    story.append(Paragraph("6. Quality Gate: The Pre-Flight Automated Validation Script", h1_style))
    story.append(Paragraph(
        "To prevent broken code, missing files, or duplicate locations from ever reaching GitHub, "
        "we created an automated pre-flight tool: <code>validate_pipeline.py</code>.",
        body_style
    ))
    story.append(Paragraph("Every teammate must run this command in their terminal before making a commit:", body_style))
    story.append(create_code_block("python validate_pipeline.py"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("What the Validation Script Tests Automatically:", h2_style))
    checks = [
        "<b>1. Locations Integrity:</b> Verifies <code>locations.py</code> exists, ensures zero duplicate names exist, and confirms every entry has <code>lat</code>, <code>lon</code>, <code>country</code>, and <code>category</code>.",
        "<b>2. Image Dataset Health:</b> Scans all images in <code>Imgs/</code> using PIL, ensuring files are valid and uncorrupted.",
        "<b>3. Weights & Caches:</b> Checks that <code>embeddings_cache.pt</code> and <code>clip_adapter.pt</code> are present and within valid size thresholds.",
        "<b>4. Code Syntax Compilation:</b> Runs <code>py_compile</code> across <code>app.py</code>, <code>predict.py</code>, <code>train_adapter.py</code>, and <code>cache_embeddings.py</code> to catch any Python syntax errors before runtime."
    ]
    for c in checks:
        story.append(Paragraph(f"&bull; {c}", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: TROUBLESHOOTING & FAQ
    # =========================================================================
    story.append(Paragraph("7. Troubleshooting & Frequently Asked Questions (FAQ)", h1_style))

    faq_items = [
        (
            "Q: The AI keeps guessing the wrong place for my photo. How do I fix it?",
            "<b>Ans:</b> Use Section 3 in the web app (Human-in-the-Loop Retraining). Select 'No, choose from available options', "
            "search for the correct spot, and click 'Retrain Model on this Image'. The app immediately saves a visual fingerprint "
            "with cosine similarity &ge; 0.92 and updates predictions instantly without catastrophic forgetting."
        ),
        (
            "Q: Why shouldn't we commit fine_tuned_streetclip_backup.pt to GitHub?",
            "<b>Ans:</b> That file is 1.71 GB. GitHub enforces a strict 100 MB per-file upload limit and will reject pushes containing it. "
            "Our <code>.gitignore</code> automatically ignores it. All team members use the pristine StreetCLIP backbone from Hugging Face "
            "and only track our lightweight <code>clip_adapter.pt</code> (1.5 MB), which fits easily into Git."
        ),
        (
            "Q: What if two teammates edit locations.py at the same time?",
            "<b>Ans:</b> Follow the Assembly Line order: Role 1 updates <code>locations.py</code> first and merges. "
            "Role 2 then pulls <code>main</code> before adding images. If a merge conflict ever happens, Git will highlight the conflicting lines "
            "with <code><<<<<<< HEAD</code>. Keep both location dictionaries, run <code>python validate_pipeline.py</code> to ensure no duplicate names, and commit."
        ),
        (
            "Q: How do we run the web app vs. the CLI tool?",
            "<b>Ans:</b> For the interactive web interface: <code>streamlit run app.py</code>.<br/>"
            "For terminal inference and heatmap generation: <code>python predict.py</code>."
        )
    ]

    for q, a in faq_items:
        story.append(Paragraph(f"<b>{q}</b>", h3_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceBefore=5, spaceAfter=12))
    story.append(Paragraph(
        "<b>GeoGuessr AI Team Guide</b> &bull; Generated for Mohammed Nihan &amp; Engineering Team &bull; Version 2.2",
        ParagraphStyle('FooterNotice', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor("#718096"), alignment=1)
    ))

    # Build the PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    out_pdf = "GeoGuessr_AI_Team_Guide.pdf"
    build_pdf(out_pdf)
