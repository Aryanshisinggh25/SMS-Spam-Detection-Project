"""
Generate Comprehensive PDF Project Documentation for SMS Spam Detection (Sentinel-SMS)
Using ReportLab
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_PDF = os.path.join(BASE_DIR, "SMS_Spam_Detection_Project_Documentation.pdf")

# Custom Canvas for Page Numbers & Running Headers
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
            return  # Suppress headers/footers on cover page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running Top Header
        self.drawString(54, letter[1] - 36, "SENTINEL // SMS • Machine Learning & NLP Project Documentation")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Running Footer
        self.line(54, 46, letter[0] - 54, 46)
        self.drawString(54, 34, "Confidential • NLP Capstone Project")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Color definitions
    c_primary   = colors.HexColor("#0f172a")  # Deep Slate Navy
    c_blue      = colors.HexColor("#2563eb")  # Cyber Blue
    c_teal      = colors.HexColor("#0d9488")  # Tech Teal
    c_gray      = colors.HexColor("#475569")  # Slate Gray
    c_light_bg  = colors.HexColor("#f8fafc")  # Off-white

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=c_primary,
        alignment=0,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=c_gray,
        spaceAfter=24
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=c_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f766e"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceAfter=8
    )

    badge_style = ParagraphStyle(
        "Badge_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=c_blue,
        spaceAfter=8
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b")
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("NLP CAPSTONE PROJECT 2 • TECHNICAL REPORT", badge_style))
    story.append(Paragraph("SENTINEL // SMS<br/>Intelligent SMS Spam & Phishing Detection System", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_blue, spaceBefore=4, spaceAfter=14))
    story.append(Paragraph(
        "A comprehensive end-to-end Natural Language Processing system and machine learning security engine "
        "designed to detect mobile smishing, lottery lures, banking fraud, and unsolicited commercial text messages. "
        "Engineered with hybrid TF-IDF n-grams, custom heuristic metadata sensors, 5-fold cross-validation, and an interactive Streamlit graphical web application.",
        subtitle_style
    ))
    story.append(Spacer(1, 30))

    # Meta Info Card Table
    meta_data = [
        [Paragraph("<b>Project Title:</b>", table_cell), Paragraph("Sentinel-SMS: AI Spam & Phishing Detection System", table_cell)],
        [Paragraph("<b>Domain:</b>", table_cell), Paragraph("Natural Language Processing (NLP) & Cybersecurity", table_cell)],
        [Paragraph("<b>Dataset:</b>", table_cell), Paragraph("UCI Machine Learning Repository — SMS Spam Collection (5,572 records)", table_cell)],
        [Paragraph("<b>Champion Model:</b>", table_cell), Paragraph("Random Forest Ensemble (200 Trees) — 98.48% Accuracy, 0.9915 ROC-AUC", table_cell)],
        [Paragraph("<b>Web Architecture:</b>", table_cell), Paragraph("Streamlit Full-Stack Reactive Web Application", table_cell)],
        [Paragraph("<b>GitHub Repository:</b>", table_cell), Paragraph("<font color='#2563eb'><u>https://github.com/Aryanshisinggh25/SMS-Spam-Detection-Project</u></font>", table_cell)],
        [Paragraph("<b>Implementation:</b>", table_cell), Paragraph("Python 3.14 x64, Scikit-Learn, NLTK, Streamlit, Pandas, Joblib", table_cell)],
    ]
    meta_table = Table(meta_data, colWidths=[1.8 * inch, 4.8 * inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Table of Contents:</b>", h2_style))
    toc_items = [
        "1. Executive Summary & Problem Formulation",
        "2. Complete Technology Stack & Specifications",
        "3. System Architecture & Processing Workflow",
        "4. Dataset Analysis & Exploratory Data Analysis (EDA)",
        "5. NLP Preprocessing & Feature Engineering Pipeline",
        "6. Machine Learning Algorithms & Theoretical Foundations",
        "7. 5-Fold Stratified Cross-Validation & Benchmark Comparison",
        "8. Performance Evaluation, Confusion Matrix & ROC Analysis",
        "9. Graphical User Interface (GUI) & Interactive Tools",
        "10. Real-World Applications, Industrial Security & Future Scope",
        "11. Local Execution & GitHub Repository Structure"
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Formulation", h1_style))
    story.append(Paragraph(
        "Short Message Service (SMS) remains one of the world's most ubiquitous, universal communication channels, "
        "delivering time-critical communications including banking One-Time Passwords (OTPs), parcel delivery notices, "
        "and emergency alerts. SMS messages have open rates exceeding 98%, making them a prime target for adversarial "
        "threat actors deploying <b>smishing (SMS phishing)</b>, fake prize lotteries, account suspension hoaxes, and predatory loans.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Technical Challenge:</b> Unlike long-form emails or news articles, SMS messages are characterized by extreme brevity "
        "(often under 160 characters), phonetic abbreviations, leetspeak (e.g., 'Fr€€'), irregular punctuation, and missing formal syntax. "
        "Standard keyword filters often result in unacceptably high False Positive rates—blocking legitimate banking notifications—which "
        "severely impairs user trust.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Project Objective:</b> Sentinel-SMS was engineered to solve this challenge by deploying a robust, hybrid machine learning "
        "pipeline combining sublinear n-gram Term Frequency-Inverse Document Frequency (TF-IDF) representation with seven domain-specific "
        "heuristic metadata sensors. The system achieves <b>98.48% test accuracy</b> and a <b>99.0% spam precision</b>, practically eliminating "
        "false alarms on legitimate communications while running entirely offline with sub-15ms inference latency.",
        body_style
    ))

    # =========================================================================
    # SECTION 2: TECHNOLOGIES & TOOLS USED
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Complete Technology Stack & System Specifications", h1_style))
    story.append(Paragraph(
        "The project is built on modern, open-source Python data science and machine learning libraries:",
        body_style
    ))

    tech_table_data = [
        [Paragraph("Layer", table_header), Paragraph("Technology / Library", table_header), Paragraph("Version", table_header), Paragraph("Functional Role", table_header)],
        [Paragraph("Core Runtime", table_cell), Paragraph("Python", table_cell), Paragraph("3.14.0 x64", table_cell), Paragraph("Primary programming runtime & script orchestration", table_cell)],
        [Paragraph("NLP Preprocessing", table_cell), Paragraph("NLTK", table_cell), Paragraph("3.10.4", table_cell), Paragraph("Tokenization, WordNet lemmatization, stopword exclusion", table_cell)],
        [Paragraph("Machine Learning", table_cell), Paragraph("Scikit-Learn", table_cell), Paragraph("1.9.1", table_cell), Paragraph("TF-IDF vectorizer, 4 ML classifiers, cross-validation, metrics", table_cell)],
        [Paragraph("Data Manipulation", table_cell), Paragraph("Pandas & NumPy", table_cell), Paragraph("3.1.1 / 2.5.5", table_cell), Paragraph("Corpus ingestion, feature transformation, sparse-dense matrix binding", table_cell)],
        [Paragraph("Visualization", table_cell), Paragraph("Matplotlib & Seaborn", table_cell), Paragraph("3.11.2 / 0.13.2", table_cell), Paragraph("Confusion matrix heatmaps, ROC plots, distribution histograms", table_cell)],
        [Paragraph("Web Application", table_cell), Paragraph("Streamlit", table_cell), Paragraph("1.67.0", table_cell), Paragraph("Reactive web UI with single/batch scanner & analytics tabs", table_cell)],
        [Paragraph("Model Persistence", table_cell), Paragraph("Joblib", table_cell), Paragraph("1.6.0", table_cell), Paragraph("High-efficiency serialization of trained pipelines and vectorizers", table_cell)],
        [Paragraph("Documentation", table_cell), Paragraph("ReportLab", table_cell), Paragraph("5.1.1", table_cell), Paragraph("Automated programmatic PDF documentation generator", table_cell)],
    ]
    tech_table = Table(tech_table_data, colWidths=[1.1 * inch, 1.5 * inch, 0.9 * inch, 3.1 * inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tech_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: SYSTEM ARCHITECTURE & WORKFLOW
    # =========================================================================
    story.append(Paragraph("3. System Architecture & Processing Pipeline", h1_style))
    story.append(Paragraph(
        "The Sentinel-SMS architecture follows a modular, 5-stage pipeline transitioning from raw unstructured text to a calibrated safety verdict:",
        body_style
    ))

    arch_steps = [
        "<b>Stage 1: Raw Ingestion & Feature Extraction:</b> Captures incoming SMS string; computes character length, word count, uppercase character counts (shouting), digit density, currency occurrences, URL hyperlinks, and exclamation marks prior to text alteration.",
        "<b>Stage 2: Lexical Normalization:</b> Lowercases text; maps external web links to a standardized <code>url</code> token; substitutes contact numbers with a <code>phone</code> token; substitutes currency amounts (£, $, €) with a <code>money</code> token; removes punctuation.",
        "<b>Stage 3: Tokenization & Lemmatization:</b> Tokenizes text via NLTK; strips standard English stopwords; lemmatizes remaining tokens via WordNet to reduce inflected forms to semantic roots.",
        "<b>Stage 4: Hybrid Sparse-Dense Vectorization:</b> Transforms normalized lemmas into an 8,000-dimensional unigram/bigram TF-IDF sparse matrix with sublinear scaling, then horizontally stacks the 7 engineered numeric features.",
        "<b>Stage 5: Ensemble Classification & Threat Scoring:</b> The Random Forest ensemble evaluates the 8,007-dimensional vector across 200 decision trees to produce the final classification (Ham vs Spam) and calibrated confidence probability."
    ]
    for s in arch_steps:
        story.append(Paragraph(s, bullet_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Dataset Analysis & Exploratory Data Analysis (EDA)", h1_style))
    story.append(Paragraph(
        "The project utilizes the gold-standard <b>UCI SMS Spam Collection</b> corpus containing 5,572 real mobile messages collected from "
        "Grumbletext (a UK spam reporting forum) and the NUS SMS Corpus. The dataset properties include:",
        body_style
    ))
    story.append(Paragraph("• <b>Total Messages:</b> 5,572", bullet_style))
    story.append(Paragraph("• <b>Legitimate (Ham):</b> 4,825 instances (86.6%)", bullet_style))
    story.append(Paragraph("• <b>Spam Instances:</b> 747 instances (13.4%)", bullet_style))
    story.append(Paragraph("• <b>Class Imbalance Ratio:</b> Approximately 6.5 : 1", bullet_style))

    # Embed Class & Length Distribution images
    img_class = os.path.join(REPORT_DIR, "class_distribution.png")
    img_len   = os.path.join(REPORT_DIR, "length_distribution.png")

    eda_imgs_data = []
    if os.path.exists(img_class) and os.path.exists(img_len):
        eda_imgs_data.append([
            Image(img_class, width=3.2 * inch, height=1.35 * inch),
            Image(img_len, width=3.2 * inch, height=1.35 * inch)
        ])
        eda_imgs_data.append([
            Paragraph("<b>Figure 1:</b> Class Distribution & Imbalance", body_style),
            Paragraph("<b>Figure 2:</b> Character Length Distribution Discrepancy", body_style)
        ])
        eda_tbl = Table(eda_imgs_data, colWidths=[3.3 * inch, 3.3 * inch])
        eda_tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(eda_tbl)

    story.append(Paragraph(
        "<b>Key EDA Observations:</b><br/>"
        "1. <b>Bimodal Length Contrast:</b> Legitimate SMS messages average 38.3 characters (brief conversational queries), "
        "whereas spam messages average 138.8 characters—nearly saturating the 160-character mobile ceiling with promotional terms.<br/>"
        "2. <b>Vocabulary Divergence:</b> Spam clusters overwhelmingly on financial promises (<code>free</code>, <code>claim</code>, "
        "<code>prize</code>, <code>won</code>, <code>cash</code>, <code>urgent</code>), while Ham contains conversational connectors "
        "(<code>go</code>, <code>come</code>, <code>get</code>, <code>know</code>, <code>love</code>, <code>ok</code>).",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: PREPROCESSING & FEATURE ENGINEERING
    # =========================================================================
    story.append(Paragraph("5. NLP Preprocessing & Feature Engineering Methodology", h1_style))
    story.append(Paragraph(
        "To maximize signal retention from noisy text while avoiding out-of-vocabulary degradation, Sentinel-SMS uses a dual feature strategy:",
        body_style
    ))

    feat_table_data = [
        [Paragraph("Feature Component", table_header), Paragraph("Type", table_header), Paragraph("Dimensionality", table_header), Paragraph("Engineering Rationale", table_header)],
        [Paragraph("TF-IDF Unigrams & Bigrams", table_cell), Paragraph("Sparse Float", table_cell), Paragraph("8,000 features", table_cell), Paragraph("Captures word pairs ('call now', 'free prize') with sublinear scaling (1 + log(tf))", table_cell)],
        [Paragraph("Message Length", table_cell), Paragraph("Integer", table_cell), Paragraph("1 feature", table_cell), Paragraph("High discrimination signal: spam messages are consistently ~3.5x longer than ham", table_cell)],
        [Paragraph("Word Count", table_cell), Paragraph("Integer", table_cell), Paragraph("1 feature", table_cell), Paragraph("Total token count per SMS", table_cell)],
        [Paragraph("Digit Density", table_cell), Paragraph("Integer", table_cell), Paragraph("1 feature", table_cell), Paragraph("Detects premium phone numbers, monetary prize sums, and OTP lure codes", table_cell)],
        [Paragraph("Uppercase Character Count", table_cell), Paragraph("Integer", table_cell), Paragraph("1 feature", table_cell), Paragraph("Captures psychological urgency / 'shouting' ('FREE', 'URGENT', 'WINNER')", table_cell)],
        [Paragraph("URL Presence Indicator", table_cell), Paragraph("Binary (0/1)", table_cell), Paragraph("1 feature", table_cell), Paragraph("Smishing indicator: flags external hyperlinks (http://, www, bit.ly)", table_cell)],
        [Paragraph("Currency Symbol Indicator", table_cell), Paragraph("Binary (0/1)", table_cell), Paragraph("1 feature", table_cell), Paragraph("Directly flags financial fraud targeting victims with £, $, or € symbols", table_cell)],
        [Paragraph("Exclamation Mark Count", table_cell), Paragraph("Integer", table_cell), Paragraph("1 feature", table_cell), Paragraph("Signals aggressive sales pressure and emotional urgency", table_cell)],
    ]
    feat_tbl = Table(feat_table_data, colWidths=[1.7 * inch, 0.9 * inch, 1.0 * inch, 3.0 * inch])
    feat_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(feat_tbl)

    # Embed Top Words & Correlation Heatmap
    img_words = os.path.join(REPORT_DIR, "top_words.png")
    img_corr  = os.path.join(REPORT_DIR, "correlation_heatmap.png")

    if os.path.exists(img_words) and os.path.exists(img_corr):
        story.append(Spacer(1, 8))
        f_imgs = [
            [Image(img_words, width=3.2 * inch, height=1.3 * inch), Image(img_corr, width=3.2 * inch, height=1.3 * inch)],
            [Paragraph("<b>Figure 3:</b> Top Words by Category", body_style), Paragraph("<b>Figure 4:</b> Metadata Correlation Heatmap", body_style)]
        ]
        f_tbl = Table(f_imgs, colWidths=[3.3 * inch, 3.3 * inch])
        f_tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(f_tbl)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: ALGORITHMS & 5-FOLD CV BENCHMARK
    # =========================================================================
    story.append(Paragraph("6. Model Development & Comparative Benchmarking", h1_style))
    story.append(Paragraph(
        "Four candidate machine learning algorithms spanning linear, probabilistic, and ensemble paradigms were trained and evaluated "
        "using <b>5-Fold Stratified Cross-Validation</b> on the training set (80% / 4,457 messages):",
        body_style
    ))

    story.append(Paragraph("• <b>Multinomial Naive Bayes (MNB):</b> Classic probabilistic text baseline using Bayes' theorem with Laplace smoothing (α=0.1).", bullet_style))
    story.append(Paragraph("• <b>Logistic Regression:</b> Regularized linear model (L2 penalty, C=5.0) predicting calibrated log-odds.", bullet_style))
    story.append(Paragraph("• <b>Linear Support Vector Machine (LinearSVC):</b> Maximum-margin hyper-plane separator optimized for high-dimensional sparse representations.", bullet_style))
    story.append(Paragraph("• <b>Random Forest Ensemble:</b> 200 de-correlated randomized decision trees combining sparse text features with dense metadata non-linear interactions.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>5-Fold Stratified Cross-Validation Tournament:</b>", h2_style))

    bench_data = [
        [Paragraph("Algorithm", table_header), Paragraph("5-Fold Mean F1", table_header), Paragraph("Standard Dev", table_header), Paragraph("Test Accuracy", table_header), Paragraph("Spam Precision", table_header), Paragraph("ROC-AUC", table_header)],
        [Paragraph("<b>Random Forest (Selected)</b>", table_cell), Paragraph("<b>0.9463</b>", table_cell), Paragraph("± 0.0174", table_cell), Paragraph("<b>98.48%</b>", table_cell), Paragraph("<b>99.0%</b>", table_cell), Paragraph("<b>0.9915</b>", table_cell)],
        [Paragraph("Logistic Regression", table_cell), Paragraph("0.9341", table_cell), Paragraph("± 0.0100", table_cell), Paragraph("97.85%", table_cell), Paragraph("97.0%", table_cell), Paragraph("0.9880", table_cell)],
        [Paragraph("Linear SVM (LinearSVC)", table_cell), Paragraph("0.9063", table_cell), Paragraph("± 0.0100", table_cell), Paragraph("97.40%", table_cell), Paragraph("94.0%", table_cell), Paragraph("0.9810", table_cell)],
        [Paragraph("Multinomial Naive Bayes", table_cell), Paragraph("0.8681", table_cell), Paragraph("± 0.0164", table_cell), Paragraph("95.96%", table_cell), Paragraph("92.0%", table_cell), Paragraph("0.9750", table_cell)],
    ]
    b_table = Table(bench_data, colWidths=[1.8 * inch, 1.0 * inch, 0.9 * inch, 0.9 * inch, 1.0 * inch, 1.0 * inch])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(b_table)

    # Embed Confusion Matrix and ROC Curve
    img_cm  = os.path.join(REPORT_DIR, "confusion_matrix.png")
    img_roc = os.path.join(REPORT_DIR, "roc_curve.png")

    if os.path.exists(img_cm) and os.path.exists(img_roc):
        story.append(Spacer(1, 8))
        eval_imgs = [
            [Image(img_cm, width=3.2 * inch, height=1.6 * inch), Image(img_roc, width=3.2 * inch, height=1.6 * inch)],
            [Paragraph("<b>Figure 5:</b> Held-Out Test Confusion Matrix (1,115 messages)", body_style),
             Paragraph("<b>Figure 6:</b> Receiver Operating Characteristic (ROC-AUC = 0.9915)", body_style)]
        ]
        e_tbl = Table(eval_imgs, colWidths=[3.3 * inch, 3.3 * inch])
        e_tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(e_tbl)

    story.append(Paragraph(
        "<b>Evaluation Insights:</b><br/>"
        "• <b>99% Spam Precision (1 False Positive out of 966):</b> In mobile security, false positives are catastrophic (blocking an authentic bank OTP or medical alert). The model achieves near-zero false alarms.<br/>"
        "• <b>0.9915 ROC-AUC:</b> Confirms outstanding class separability across arbitrary operational decision thresholds.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 7: WEB GUI ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("7. Graphical User Interface (GUI) & Interactive System", h1_style))
    story.append(Paragraph(
        "In accordance with mandatory capstone requirements, a production-ready, reactive web application was implemented using Streamlit:",
        body_style
    ))

    gui_features = [
        "<b>Live Single Payload Scanner:</b> Real-time classification engine with instant threat confidence percentage meters, character & word counters, and 1-click test presets (Lottery scam, Bank phishing, Casual chat, Meeting reminder).",
        "<b>Heuristic Sensor Array:</b> Live visual badges indicating detected danger indicators: currency symbols, external URLs, high digit density, excessive capitalization, and urgency punctuation.",
        "<b>Deep Inspection Console:</b> Side-by-side terminal highlighting flagged trigger words in red and displaying the normalized NLTK lemma stream.",
        "<b>Mass Ingestion Pipeline (Batch CSV):</b> Allows telecom operators or enterprises to upload a CSV file with thousands of messages, executes batch predictions with progress telemetry, and generates downloadable annotated CSVs.",
        "<b>Interactive EDA & Telemetry Hub:</b> Embedded dashboard visualizing class distributions, length histograms, top words, and interactive corpus keyword grep search.",
        "<b>Model Benchmark Matrix:</b> Transparent leaderboard displaying cross-validation F1 scores, confusion matrices, and ROC curves."
    ]
    for g in gui_features:
        story.append(Paragraph(f"• {g}", bullet_style))

    img_gui = os.path.join(REPORT_DIR, "gui_screenshot.png")
    if os.path.exists(img_gui):
        story.append(Spacer(1, 8))
        story.append(Image(img_gui, width=6.2 * inch, height=2.2 * inch))
        story.append(Paragraph("<b>Figure 7:</b> Streamlit Web Application Interface running on localhost:8501", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Real-World Applications, Limitations & Future Scope", h1_style))
    story.append(Paragraph(
        "<b>Industrial Applications:</b><br/>"
        "• <b>Telecom Gateway Defense:</b> Deployed at SMS carrier switching centers to quarantine mass smishing campaigns before reaching user antennas.<br/>"
        "• <b>Mobile OS Filtering Extensions:</b> Integrated into native mobile messaging clients (iOS SMS Filter / Android Spam Protection) for on-device privacy-first filtering.<br/>"
        "• <b>Fintech & Banking Portals:</b> Real-time sanitization of customer feedback channels and verification of outbound promotional SMS delivery.<br/><br/>"
        "<b>Limitations & Adversarial Vectors:</b><br/>"
        "• <b>Adversarial Perturbations:</b> Attackers increasingly use homoglyphs (Cyrillic characters mimicking Latin letters) and zero-width spaces to bypass simple tokenizers.<br/>"
        "• <b>Multilingual & Hinglish Blends:</b> Romanized Hindi/Tamil/Bengali SMS require multilingual tokenizers (e.g., IndicBERT or XLM-RoBERTa).<br/><br/>"
        "<b>Future Roadmap:</b><br/>"
        "1. Transformer distillation into ONNX / TensorFlow Lite for sub-5ms on-device mobile inference without cloud privacy risks.<br/>"
        "2. Multilingual fine-tuning on Indic smishing datasets.<br/>"
        "3. Real-time active learning loop capturing newly emerging smishing lures reported by users.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documentation PDF generated successfully at: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_pdf()
