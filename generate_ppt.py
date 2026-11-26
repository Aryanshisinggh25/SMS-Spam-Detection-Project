"""
Generate Comprehensive Widescreen PowerPoint Presentation for Sentinel-SMS
Based on the Technical Documentation PDF
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_PPT = os.path.join(BASE_DIR, "SMS_Spam_Detection_Presentation.pptx")

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Deep Cyber Dark Theme)
C_BG_DARK    = RGBColor(11, 15, 25)      # #0B0F19 Dark Canvas
C_SURFACE    = RGBColor(19, 27, 46)      # #131B2E Card Surface
C_BORDER     = RGBColor(40, 53, 84)      # #283554 Card Border
C_TEXT_WHITE = RGBColor(248, 250, 252)   # #F8FAFC Heading Text
C_TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Body Text
C_CYAN       = RGBColor(56, 189, 248)    # #38BDF8 Accent Cyan
C_BLUE       = RGBColor(37, 99, 235)     # #2563EB Accent Blue
C_GREEN      = RGBColor(16, 185, 129)    # #10B981 Accent Green
C_RED        = RGBColor(244, 63, 94)     # #F43F5E Accent Red
C_AMBER      = RGBColor(245, 158, 11)    # #F59E0B Accent Amber

blank_layout = prs.slide_layouts[6]

def apply_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = C_BG_DARK
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category="NLP CAPSTONE PROJECT 2 • TECHNICAL REPORT"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_CYAN
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_WHITE

def create_card(slide, left, top, width, height, bg_color=C_SURFACE, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1: TITLE SLIDE (Cover)
# ═══════════════════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank_layout)
apply_background(s1)

# Subtle decorative accent bar
accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(1.8), Inches(0.06))
accent.fill.solid()
accent.fill.fore_color.rgb = C_CYAN
accent.line.fill.background()

# Title and Subtitle Block
tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(2.1))
tf = tb_title.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "SENTINEL // SMS"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = C_TEXT_WHITE

p = tf.add_paragraph()
p.text = "Intelligent SMS Spam & Phishing Detection System"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_CYAN
p.space_after = Pt(6)

p = tf.add_paragraph()
p.text = "Natural Language Processing & Machine Learning Capstone Project • AI Cyber Threat Intelligence Platform"
p.font.size = Pt(12)
p.font.color.rgb = C_TEXT_MUTED

# Left Card: Submitted To (Supervisor / Guide)
c_left = create_card(s1, Inches(0.8), Inches(3.1), Inches(5.5), Inches(3.8))
tb_left = s1.shapes.add_textbox(Inches(1.1), Inches(3.3), Inches(4.9), Inches(3.4))
tf_left = tb_left.text_frame
tf_left.word_wrap = True

p_left_cat = tf_left.paragraphs[0]
p_left_cat.text = "PROJECT SUPERVISION"
p_left_cat.font.size = Pt(11)
p_left_cat.font.bold = True
p_left_cat.font.color.rgb = C_CYAN
p_left_cat.space_after = Pt(12)

p_sub = tf_left.add_paragraph()
p_sub.text = "Submitted to :- Kavish Mudgal"
p_sub.font.size = Pt(22)
p_sub.font.bold = True
p_sub.font.color.rgb = C_TEXT_WHITE
p_sub.space_after = Pt(18)

p_meta1 = tf_left.add_paragraph()
p_meta1.text = "• Domain: Natural Language Processing & Cybersecurity"
p_meta1.font.size = Pt(11)
p_meta1.font.color.rgb = C_TEXT_MUTED
p_meta1.space_after = Pt(4)

p_meta2 = tf_left.add_paragraph()
p_meta2.text = "• Solution: Hybrid TF-IDF + Heuristic Metadata Threat Pipeline"
p_meta2.font.size = Pt(11)
p_meta2.font.color.rgb = C_TEXT_MUTED
p_meta2.space_after = Pt(4)

p_meta3 = tf_left.add_paragraph()
p_meta3.text = "• Tech Stack: Python 3.14 • Scikit-Learn • NLTK • Streamlit"
p_meta3.font.size = Pt(11)
p_meta3.font.color.rgb = C_TEXT_MUTED
p_meta3.space_after = Pt(4)

p_meta4 = tf_left.add_paragraph()
p_meta4.text = "• Repository: github.com/Aryanshisinggh25/SMS-Spam-Detection-Project"
p_meta4.font.size = Pt(10)
p_meta4.font.color.rgb = C_CYAN

# Right Card: Submitted By (Team Members & Roll Numbers)
c_right = create_card(s1, Inches(6.6), Inches(3.1), Inches(5.9), Inches(3.8))

tb_right_header = s1.shapes.add_textbox(Inches(6.9), Inches(3.3), Inches(5.3), Inches(0.4))
tf_right_h = tb_right_header.text_frame
tf_right_h.word_wrap = True
p_right_cat = tf_right_h.paragraphs[0]
p_right_cat.text = "SUBMITTED BY (PROJECT TEAM)"
p_right_cat.font.size = Pt(11)
p_right_cat.font.bold = True
p_right_cat.font.color.rgb = C_CYAN

# Column Header (Name | Roll No.)
tb_names = s1.shapes.add_textbox(Inches(6.9), Inches(3.75), Inches(3.4), Inches(3.0))
tf_names = tb_names.text_frame
tf_names.word_wrap = True

p_nh = tf_names.paragraphs[0]
p_nh.text = "Name"
p_nh.font.size = Pt(12)
p_nh.font.bold = True
p_nh.font.color.rgb = C_CYAN
p_nh.space_after = Pt(6)

tb_rolls = s1.shapes.add_textbox(Inches(10.3), Inches(3.75), Inches(2.0), Inches(3.0))
tf_rolls = tb_rolls.text_frame
tf_rolls.word_wrap = True

p_rh = tf_rolls.paragraphs[0]
p_rh.text = "Roll No."
p_rh.font.size = Pt(12)
p_rh.font.bold = True
p_rh.font.color.rgb = C_CYAN
p_rh.space_after = Pt(6)

team_members = [
    ("Aryanshi Singh", "2401201190"),
    ("Preeti Chaurasia", "2401201191"),
    ("Ashish Bhatt", "2401201187"),
    ("Ashish", "2401201188"),
    ("Ayush Verma", "2401201186"),
    ("Abhishek Kumar Yadav", "2401201193"),
]

for name, roll in team_members:
    pn = tf_names.add_paragraph()
    pn.text = name
    pn.font.size = Pt(11)
    pn.font.bold = True
    pn.font.color.rgb = C_TEXT_WHITE
    pn.space_after = Pt(4)
    
    pr = tf_rolls.add_paragraph()
    pr.text = roll
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = C_TEXT_MUTED
    pr.space_after = Pt(4)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2: PROBLEM STATEMENT & CHALLENGES
# ═══════════════════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank_layout)
apply_background(s2)
add_header(s2, "1. Executive Summary & Problem Formulation")

c2_1 = create_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
c2_2 = create_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))

# Left Card: The Real-World Problem
tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "The Adversarial Landscape"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_RED
p.space_after = Pt(10)

points_left = [
    ("Ubiquitous Mobile Target:", "SMS enjoys >98% open rates, making it the primary conduit for smishing (SMS phishing), fraudulent OTP lures, and lottery scams."),
    ("Severe Brevity Constraints:", "SMS messages average <160 characters, with heavy phonetic abbreviations, irregular punctuation, and zero formal grammatical cues."),
    ("Adversarial Evasion:", "Threat actors deploy leetspeak (e.g., 'Fr€€', 'cl@im') and obfuscated short URLs to bypass standard keyword filters."),
    ("High Cost of False Positives:", "Blocking a single authentic banking OTP or family emergency text ruins user trust. Precision must be near 100%.")
]
for title, desc in points_left:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_WHITE
    p = tf.add_paragraph()
    p.text = f"   {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

# Right Card: The Sentinel-SMS Solution
tb2 = s2.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.3), Inches(4.8))
tf2 = tb2.text_frame
tf2.word_wrap = True

p = tf2.paragraphs[0]
p.text = "The Sentinel-SMS Solution"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_GREEN
p.space_after = Pt(10)

points_right = [
    ("Hybrid NLP Representation:", "Fuses 8,000 sublinear TF-IDF unigram & bigram features with 7 custom domain metadata sensors (URLs, currency symbols, shouting CAPS, digits)."),
    ("High Precision Optimization:", "Engineered to minimize False Positives. Achieves 99.0% spam precision on unseen test messages."),
    ("Real-Time Offline Execution:", "Runs sub-15ms local inference without transmitting private SMS conversations to external APIs."),
    ("Production-Grade GUI:", "Complete interactive Streamlit web dashboard featuring single SMS inspection, batch CSV ingestion, and embedded telemetry.")
]
for title, desc in points_right:
    p = tf2.add_paragraph()
    p.text = f"• {title} "
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = f"   {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3: COMPLETE TECHNOLOGY STACK
# ═══════════════════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank_layout)
apply_background(s3)
add_header(s3, "2. Technology Stack & Implementation Frameworks")

tech_cards = [
    ("Python 3.14 x64", "Core Runtime", "Underlying high-performance Python runtime executing script pipelines, threading, and environment isolation.", C_CYAN),
    ("Scikit-Learn 1.9.1", "Machine Learning Core", "TF-IDF vectorizer, Multinomial Naive Bayes, Logistic Regression, Linear SVM, and Random Forest ensemble.", C_BLUE),
    ("NLTK 3.10.4", "NLP Preprocessing", "Punkt tokenizer, WordNet lemmatizer, stopword dictionaries, and regular expression entity mapping.", C_GREEN),
    ("Streamlit 1.67.0", "Reactive Web GUI", "Full-stack web application providing real-time text analysis, batch CSV ingestion, and telemetry charts.", C_AMBER),
    ("Pandas & NumPy", "Data Matrix Engine", "Corpus loading, feature manipulation, and sparse-dense matrix horizontal stacking (SciPy).", C_CYAN),
    ("Matplotlib & Seaborn", "Telemetry Analytics", "Confusion matrix heatmaps, ROC curves, class distributions, and correlation matrices.", C_BLUE),
]

for idx, (title, role, desc, accent_c) in enumerate(tech_cards):
    col = idx % 3
    row = idx // 3
    x = Inches(0.8 + col * 3.9)
    y = Inches(1.8 + row * 2.6)
    
    create_card(s3, x, y, Inches(3.7), Inches(2.4))
    
    tb = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.3), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = role.upper()
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = accent_c
    
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE
    p.space_after = Pt(6)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_MUTED

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4: SYSTEM ARCHITECTURE & 5-STAGE WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(blank_layout)
apply_background(s4)
add_header(s4, "3. System Architecture & 5-Stage Processing Pipeline")

stages = [
    ("Stage 01", "Raw Ingestion & Feature Sensor Scan", "Captures raw SMS text; extracts 7 metadata signals (char length, word count, uppercase count, digits, URLs, currency, exclamation marks) before text alteration."),
    ("Stage 02", "Entity Normalization & Regex Mapping", "Lowercases text; standardizes web hyperlinks -> 'url'; maps phone numbers -> 'phone'; substitutes currency amounts (£, $, €) -> 'money'; removes punctuation."),
    ("Stage 03", "Tokenization & WordNet Lemmatization", "Applies NLTK word tokenization; strips English stopwords; reduces remaining tokens to their morphological base lemma using WordNet."),
    ("Stage 04", "Hybrid Sparse-Dense Matrix Vectorization", "Builds an 8,000-dimensional unigram/bigram TF-IDF sparse matrix with sublinear term-frequency scaling, then horizontally stacks the 7 engineered numeric features."),
    ("Stage 05", "Ensemble Classification & Calibrated Score", "The Random Forest ensemble evaluates the 8,007-dimensional vector across 200 de-correlated decision trees to output the classification verdict and confidence percentage.")
]

for idx, (stg, title, desc) in enumerate(stages):
    y = Inches(1.7 + idx * 1.05)
    create_card(s4, Inches(0.8), y, Inches(11.7), Inches(0.95))
    
    tb = s4.shapes.add_textbox(Inches(1.0), y + Inches(0.12), Inches(11.3), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"{stg}  //  {title}"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5: DATASET PROFILE & EDA
# ═══════════════════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(blank_layout)
apply_background(s5)
add_header(s5, "4. Dataset Profile & Exploratory Data Analysis (EDA)")

create_card(s5, Inches(0.8), Inches(1.7), Inches(5.2), Inches(5.2))

tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(4.8), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "UCI SMS Spam Collection Corpus"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TEXT_WHITE
p.space_after = Pt(10)

stats = [
    ("Total Messages:", "5,572 mobile SMS records"),
    ("Legitimate (Ham):", "4,825 instances (86.6%)"),
    ("Adversarial (Spam):", "747 instances (13.4%)"),
    ("Imbalance Ratio:", "6.5 to 1 class imbalance"),
    ("Splitting Strategy:", "80% Training (4,457), 20% Test (1,115) - Stratified"),
    ("Bimodal Length Contrast:", "Ham averages ~38 chars (brief chats), while Spam averages ~138 chars (promo pitch + phone + link)"),
    ("Dominant Spam Tokens:", "'free', 'claim', 'prize', 'won', 'cash', 'urgent', 'call', 'txt'")
]
for lbl, val in stats:
    p = tf.add_paragraph()
    p.text = f"• {lbl} {val}"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

# Embed Class & Length Distribution images on right side
img_class = os.path.join(REPORT_DIR, "class_distribution.png")
img_len   = os.path.join(REPORT_DIR, "length_distribution.png")

if os.path.exists(img_class):
    s5.shapes.add_picture(img_class, Inches(6.3), Inches(1.7), width=Inches(6.2))
if os.path.exists(img_len):
    s5.shapes.add_picture(img_len, Inches(6.3), Inches(4.3), width=Inches(6.2))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6: FEATURE ENGINEERING & TOP WORDS
# ═══════════════════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(blank_layout)
apply_background(s6)
add_header(s6, "5. NLP Feature Engineering & Signal Correlation")

create_card(s6, Inches(0.8), Inches(1.7), Inches(5.2), Inches(5.2))

tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(4.8), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Engineered Feature Matrix (8,007 Dims)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_CYAN
p.space_after = Pt(8)

feats = [
    ("TF-IDF Unigrams & Bigrams:", "8,000 sparse dimensions capturing word co-occurrences ('free ringtone', 'call now') with sublinear scaling (1 + log(tf))."),
    ("Message Length:", "Spam messages are ~3.5x longer than legitimate chats."),
    ("Digit Count:", "Detects premium call-rate numbers and monetary sums (+0.43 correlation with spam)."),
    ("Uppercase Characters:", "Detects aggressive emotional urgency and shouting (+0.38 correlation)."),
    ("Currency Indicators (£, $, €):", "Direct indicator of prize lottery and financial scam payloads (+0.38 correlation)."),
    ("Hyperlink Indicators (URLs):", "Identifies smishing and credential harvesting domains."),
    ("Exclamation Marks:", "Signals pressure-based sales solicitations.")
]
for lbl, val in feats:
    p = tf.add_paragraph()
    p.text = f"• {lbl} {val}"
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(3)

img_words = os.path.join(REPORT_DIR, "top_words.png")
img_corr  = os.path.join(REPORT_DIR, "correlation_heatmap.png")

if os.path.exists(img_words):
    s6.shapes.add_picture(img_words, Inches(6.3), Inches(1.7), width=Inches(6.2))
if os.path.exists(img_corr):
    s6.shapes.add_picture(img_corr, Inches(6.3), Inches(4.3), width=Inches(6.2))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7: ALGORITHM BENCHMARKING (5-Fold CV Tournament)
# ═══════════════════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(blank_layout)
apply_background(s7)
add_header(s7, "6. Machine Learning Model Tournament & 5-Fold Cross-Validation")

create_card(s7, Inches(0.8), Inches(1.7), Inches(6.2), Inches(5.2))

tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.8), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Benchmark Leaderboard (5-Fold CV)"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = C_TEXT_WHITE
p.space_after = Pt(10)

models_eval = [
    ("🥇 Random Forest (Selected Champion)", "F1 = 0.9463 ± 0.017 | Accuracy = 98.48% | ROC-AUC = 0.9915", "Ensemble of 200 trees combining sparse n-grams with non-linear dense metadata interactions. Highest overall discrimination."),
    ("🥈 Logistic Regression (L2 C=5.0)", "F1 = 0.9341 ± 0.010 | Accuracy = 97.85% | ROC-AUC = 0.9880", "High-performing linear model with well-calibrated probabilistic confidence."),
    ("🥉 Linear SVM (LinearSVC)", "F1 = 0.9063 ± 0.010 | Accuracy = 97.40% | ROC-AUC = 0.9810", "Effective maximum-margin hyperplane separator across 8,000 sparse dimensions."),
    ("4th Multinomial Naive Bayes (α=0.1)", "F1 = 0.8681 ± 0.016 | Accuracy = 95.96% | ROC-AUC = 0.9750", "Classical probabilistic baseline, but penalizes feature independence assumptions.")
]
for title, metrics, desc in models_eval:
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p = tf.add_paragraph()
    p.text = f"   {metrics}"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE
    p = tf.add_paragraph()
    p.text = f"   {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

img_comp = os.path.join(REPORT_DIR, "model_comparison.png")
if os.path.exists(img_comp):
    s7.shapes.add_picture(img_comp, Inches(7.3), Inches(1.8), width=Inches(5.2))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8: EVALUATION RESULTS & CONFUSION MATRIX
# ═══════════════════════════════════════════════════════════════════════════════
s8 = prs.slides.add_slide(blank_layout)
apply_background(s8)
add_header(s8, "7. Performance Evaluation & Test Set Metrics (1,115 SMS)")

# Key Metric Badges
kpis = [
    ("TEST ACCURACY", "98.48%", C_GREEN),
    ("SPAM PRECISION", "99.0%", C_CYAN),
    ("ROC-AUC SCORE", "0.9915", C_BLUE),
    ("FALSE POSITIVES", "1 of 966", C_AMBER),
]
for idx, (label, val, col) in enumerate(kpis):
    x = Inches(0.8 + idx * 2.95)
    create_card(s8, x, Inches(1.7), Inches(2.8), Inches(1.1))
    tb = s8.shapes.add_textbox(x + Inches(0.1), Inches(1.75), Inches(2.6), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MUTED
    p = tf.add_paragraph()
    p.text = val
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = col

img_cm  = os.path.join(REPORT_DIR, "confusion_matrix.png")
img_roc = os.path.join(REPORT_DIR, "roc_curve.png")

if os.path.exists(img_cm):
    s8.shapes.add_picture(img_cm, Inches(0.8), Inches(3.0), width=Inches(5.7))
if os.path.exists(img_roc):
    s8.shapes.add_picture(img_roc, Inches(6.8), Inches(3.0), width=Inches(5.7))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9: STREAMLIT WEB GUI DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════
s9 = prs.slides.add_slide(blank_layout)
apply_background(s9)
add_header(s9, "8. Web Application Interface (Streamlit GUI)")

create_card(s9, Inches(0.8), Inches(1.7), Inches(5.2), Inches(5.2))

tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(4.8), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Interactive GUI Architecture"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = C_CYAN
p.space_after = Pt(8)

gui_bullets = [
    ("Real-Time Ingestion Console:", "Input custom SMS or trigger 1-click presets (Lottery scam, Bank phishing, Casual chat, Meeting reminder)."),
    ("Dynamic Threat Score HUD:", "Renders instant high-contrast verdicts with calibrated probability confidence percentages."),
    ("Heuristic Sensor Array:", "Displays live badges indicating detected threat signals (currency, URLs, phone numbers, shouting CAPS)."),
    ("Deep Inspection Console:", "Highlights high-weight trigger keywords in red and displays the normalized NLTK lemma stream."),
    ("Mass Ingestion Pipeline (CSV):", "Uploads, batch-scans, and annotates thousands of messages with downloadable CSV results."),
    ("Corpus Telemetry & Leaderboard:", "Interactive data explorer and model benchmark matrices.")
]
for lbl, val in gui_bullets:
    p = tf.add_paragraph()
    p.text = f"• {lbl} {val}"
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

img_gui = os.path.join(REPORT_DIR, "gui_screenshot.png")
if os.path.exists(img_gui):
    s9.shapes.add_picture(img_gui, Inches(6.3), Inches(1.7), width=Inches(6.2))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10: REAL-WORLD APPLICATIONS & FUTURE SCOPE
# ═══════════════════════════════════════════════════════════════════════════════
s10 = prs.slides.add_slide(blank_layout)
apply_background(s10)
add_header(s10, "9. Real-World Applications, Industrial Security & Future Scope")

c10_1 = create_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
c10_2 = create_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))

# Left: Industrial Deployment
tb = s10.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Industrial Security Applications"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_CYAN
p.space_after = Pt(10)

ind_apps = [
    ("Telecom Gateway Smishing Defense:", "Filter fraudulent SMS traffic at telecommunication transit switching centers before it reaches subscriber towers."),
    ("Mobile OS Integration:", "On-device native message filtering extension for iOS SMS Filtering and Android Messages protecting end-users."),
    ("Fintech & Banking Security:", "Real-time verification of transactional notifications and outbound marketing campaigns to protect brand trust."),
    ("Enterprise Log Sanitization:", "Automated batch auditing of customer support messages and inbound communications.")
]
for lbl, val in ind_apps:
    p = tf.add_paragraph()
    p.text = f"• {lbl} "
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_WHITE
    p = tf.add_paragraph()
    p.text = f"   {val}"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

# Right: Limitations & Future Roadmap
tb2 = s10.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.3), Inches(4.8))
tf2 = tb2.text_frame
tf2.word_wrap = True

p = tf2.paragraphs[0]
p.text = "Future Technical Roadmap"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_AMBER
p.space_after = Pt(10)

future_items = [
    ("Transformer Edge Distillation:", "Compress models via TinyBERT or MobileBERT into ONNX / TensorFlow Lite for sub-5ms on-device mobile execution."),
    ("Multilingual & Indic Language Support:", "Incorporate IndicBERT / XLM-RoBERTa embeddings to capture Romanized Hindi (Hinglish), Tamil, and Bengali smishing lures."),
    ("Adversarial Robustness Hardening:", "Implement homoglyph normalization and adversarial perturbation training against leetspeak evasion."),
    ("Active Threat Intelligence Feedback:", "Continuous online learning pipeline updating decision boundaries as emerging phishing campaigns are reported.")
]
for lbl, val in future_items:
    p = tf2.add_paragraph()
    p.text = f"• {lbl} "
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = f"   {val}"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11: CONCLUSION & GITHUB REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════
s11 = prs.slides.add_slide(blank_layout)
apply_background(s11)
add_header(s11, "10. Project Summary & Deliverables")

create_card(s11, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.2))

tb = s11.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Key Project Achievements"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = C_GREEN
p.space_after = Pt(14)

achievements = [
    "✅ End-to-End NLP Application: Built from scratch covering dataset exploration, preprocessing, feature extraction, cross-validation, and web deployment.",
    "✅ Superior Empirical Performance: Champion Random Forest model achieved 98.48% Accuracy, 99.0% Precision, and 0.9915 ROC-AUC.",
    "✅ Production Streamlit GUI: Fully functional multi-page web application featuring live single-message scanning, batch CSV ingestion, and telemetry dashboard.",
    "✅ Comprehensive Documentation & Artifacts: Complete Jupyter Notebook (.ipynb), technical PDF report, 16:9 presentation deck, and serialized model binaries.",
    "✅ Verified GitHub Deployment: Clean, dedicated repository with 100% verified contributions under Aryanshisinggh25."
]
for a in achievements:
    p = tf.add_paragraph()
    p.text = a
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEXT_WHITE
    p.space_after = Pt(8)

p = tf.add_paragraph()
p.text = "\nGitHub Repository URL:"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_CYAN

p = tf.add_paragraph()
p.text = "https://github.com/Aryanshisinggh25/SMS-Spam-Detection-Project"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TEXT_WHITE

prs.save(OUTPUT_PPT)
print(f"Presentation saved successfully to: {OUTPUT_PPT}")
