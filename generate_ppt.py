"""
Generates PowerPoint Presentation (PPT) matching Section 4 Guidelines:
1. Project title and team members
2. Problem statement and objectives
3. Introduction and real-world applications
4. Dataset description
5. Data preprocessing and EDA
6. Feature engineering and methodology
7. Model architecture and algorithms
8. Performance evaluation and results
9. GUI screenshots and working demonstration
10. Conclusion and future scope
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Colors
C_DARK = RGBColor(26, 36, 43)
C_BLUE = RGBColor(33, 150, 243)
C_RED = RGBColor(231, 76, 60)
C_GREEN = RGBColor(46, 204, 113)
C_GRAY = RGBColor(100, 110, 120)

blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category="NLP CAPSTONE PROJECT 2"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(12)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_BLUE

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = C_DARK

# ----------------- SLIDE 1: Title -----------------
s1 = prs.slides.add_slide(blank_layout)
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.0))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "SENTINEL-SMS"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_BLUE

p = tf1.add_paragraph()
p.text = "Intelligent SMS Spam Detection System"
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = C_DARK

p = tf1.add_paragraph()
p.text = "Natural Language Processing Capstone Project"
p.font.size = Pt(18)
p.font.color.rgb = C_GRAY

p = tf1.add_paragraph()
p.text = "\nTeam Members: Ansh Jangid / Abhay Goyat & Group Members\nTechnology Stack: Python | NLTK | Scikit-Learn | Streamlit"
p.font.size = Pt(16)
p.font.color.rgb = C_DARK

# ----------------- SLIDE 2: Problem Statement & Objectives -----------------
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "1. Problem Statement & Objectives")
tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf2 = tb2.text_frame
tf2.word_wrap = True

p = tf2.paragraphs[0]
p.text = "Problem Statement:"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_RED

p = tf2.add_paragraph()
p.text = "• Short Message Service (SMS) remains a critical communication medium, but it is heavily targeted by fraud, phishing, lottery scams, and spam.\n• Unsolicited spam messages cause financial loss, security breaches, and degrade user trust.\n• Detecting spam in SMS is particularly challenging due to abbreviations, typos, informal slang, and character length limits."
p.font.size = Pt(16)

p = tf2.add_paragraph()
p.text = "\nKey Project Objectives:"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_BLUE

p = tf2.add_paragraph()
p.text = "• Develop an end-to-end automated NLP pipeline to classify incoming SMS as Ham (Legitimate) or Spam.\n• Minimize False Positives (prevent legitimate messages from being marked as spam).\n• Engineer domain-specific statistical and lexical text features combined with TF-IDF n-grams.\n• Evaluate multiple machine learning algorithms and build a production-grade Streamlit web GUI."
p.font.size = Pt(16)

# ----------------- SLIDE 3: Introduction & Real-World Applications -----------------
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "2. Introduction & Real-World Applications")
tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf3 = tb3.text_frame
tf3.word_wrap = True

p = tf3.paragraphs[0]
p.text = "Real-World Industry Applications:"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_DARK

apps = [
    ("Telecom Carrier Gateways:", "Filter malicious SMS traffic at telecom transit level before it reaches user handsets."),
    ("Mobile OS Integration:", "Native spam filtering in Android Messages and Apple iOS message filtering extensions."),
    ("Fintech & Banking Security:", "Protect customers from financial phishing, credential harvesting, and fraudulent OTP lures."),
    ("Enterprise Bulk Messaging:", "Validate outbound marketing campaigns against spam rules to protect sender reputation.")
]
for title, desc in apps:
    p = tf3.add_paragraph()
    p.text = f"• {title} {desc}"
    p.font.size = Pt(16)

p = tf3.add_paragraph()
p.text = "\nReal-World Challenges & Limitations:"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_RED
p = tf3.add_paragraph()
p.text = "• Evolving adversarial attacks (e.g., character substitution, homoglyphs like 'Fr€€').\n• High cost of false positives (missing a critical OTP or family SMS is far worse than seeing spam).\n• Low latency requirement for real-time mobile filtering."
p.font.size = Pt(15)

# ----------------- SLIDE 4: Dataset Description -----------------
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "3. Dataset Description (UCI SMS Spam Collection)")
tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
tf4 = tb4.text_frame
tf4.word_wrap = True

p = tf4.paragraphs[0]
p.text = "Dataset Characteristics:"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_DARK

stats = [
    ("Source:", "UCI Machine Learning Repository / Grumbletext"),
    ("Total Instances:", "5,572 mobile messages"),
    ("Legitimate (Ham):", "4,825 instances (86.6%)"),
    ("Spam:", "747 instances (13.4%)"),
    ("Imbalance Ratio:", "~6.5 : 1 class imbalance"),
    ("Format:", "Tab-separated values (Label, SMS Text)"),
    ("Splitting Strategy:", "80% Training, 20% Test (Stratified Split)")
]
for label, val in stats:
    p = tf4.add_paragraph()
    p.text = f"• {label} {val}"
    p.font.size = Pt(16)

class_dist_img = os.path.join(REPORT_DIR, "class_distribution.png")
if os.path.exists(class_dist_img):
    s4.shapes.add_picture(class_dist_img, Inches(7.0), Inches(1.8), width=Inches(5.5))

# ----------------- SLIDE 5: Data Preprocessing & EDA -----------------
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "4. Data Preprocessing & Exploratory Data Analysis")
tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
tf5 = tb5.text_frame
tf5.word_wrap = True

p = tf5.paragraphs[0]
p.text = "Multi-Stage NLP Preprocessing Pipeline:"
p.font.size = Pt(18)
p.font.bold = True

steps = [
    ("Normalization:", "Case folding to lower-case for uniformity."),
    ("Entity Tokenization:", "Regex substitution of URLs ('url'), phones ('phone'), and currencies ('money')."),
    ("Noise Removal:", "Punctuation and non-alphabetic token stripping."),
    ("Stopword Filtering:", "NLTK English stopwords exclusion."),
    ("Lemmatization:", "WordNet Lemmatization to reduce words to core lemma.")
]
for s, d in steps:
    p = tf5.add_paragraph()
    p.text = f"• {s} {d}"
    p.font.size = Pt(15)

length_img = os.path.join(REPORT_DIR, "length_distribution.png")
if os.path.exists(length_img):
    s5.shapes.add_picture(length_img, Inches(7.0), Inches(1.8), width=Inches(5.5))

# ----------------- SLIDE 6: Feature Engineering Methodology -----------------
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "5. Feature Engineering & Methodology")
tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
tf6 = tb6.text_frame
tf6.word_wrap = True

p = tf6.paragraphs[0]
p.text = "Hybrid Feature Representation:"
p.font.size = Pt(18)
p.font.bold = True

p = tf6.add_paragraph()
p.text = "1. N-Gram TF-IDF Vectorization:\n   • Unigrams & Bigrams (ngram_range=(1,2))\n   • Sublinear term frequency scaling\n   • Vocabulary capped at 8,000 informative terms"
p.font.size = Pt(15)

p = tf6.add_paragraph()
p.text = "\n2. Domain-Specific Metadata Signals:\n   • Message length (characters)\n   • Word & token count\n   • Digit frequency count\n   • Uppercase character count (shouting)\n   • Presence flags for URLs, currency symbols (£, $, €)\n   • Exclamation mark frequency"
p.font.size = Pt(15)

corr_img = os.path.join(REPORT_DIR, "correlation_heatmap.png")
if os.path.exists(corr_img):
    s6.shapes.add_picture(corr_img, Inches(7.0), Inches(1.8), width=Inches(5.5))

# ----------------- SLIDE 7: Model Architecture & Algorithms -----------------
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "6. Model Architecture & Algorithms")
tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
tf7 = tb7.text_frame
tf7.word_wrap = True

p = tf7.paragraphs[0]
p.text = "Comparative Model Benchmarking:"
p.font.size = Pt(18)
p.font.bold = True

models = [
    ("Multinomial Naive Bayes:", "Probabilistic baseline ideal for sparse text features; alpha=0.1."),
    ("Logistic Regression:", "L2-regularized linear classifier with sigmoid log-odds output; C=5.0."),
    ("Linear Support Vector Machine:", "Maximum-margin hyperplane classifier (LinearSVC)."),
    ("Random Forest Classifier:", "Ensemble of 200 decision trees mitigating overfitting on hybrid feature spaces.")
]
for m, d in models:
    p = tf7.add_paragraph()
    p.text = f"• {m} {d}"
    p.font.size = Pt(15)

p = tf7.add_paragraph()
p.text = "\nValidation Strategy: 5-Fold Stratified Cross-Validation on training data to ensure unbiased metric assessment."
p.font.size = Pt(14)
p.font.bold = True

comp_img = os.path.join(REPORT_DIR, "model_comparison.png")
if os.path.exists(comp_img):
    s7.shapes.add_picture(comp_img, Inches(7.0), Inches(1.8), width=Inches(5.5))

# ----------------- SLIDE 8: Performance Evaluation & Results -----------------
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "7. Performance Evaluation & Test Results")
tb8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.0))
tf8 = tb8.text_frame
tf8.word_wrap = True

p = tf8.paragraphs[0]
p.text = "Held-Out Test Set Metrics (1,115 SMS):"
p.font.size = Pt(18)
p.font.bold = True

results = [
    ("Overall Accuracy:", "98.48%"),
    ("ROC-AUC Score:", "0.9915"),
    ("Ham Precision:", "98% (Recall: 100%)"),
    ("Spam Precision:", "99% (Near-zero false alarms)"),
    ("Spam Recall:", "89%"),
    ("Spam F1-Score:", "0.94"),
    ("Champion Model:", "Random Forest Ensemble")
]
for r, v in results:
    p = tf8.add_paragraph()
    p.text = f"• {r} {v}"
    p.font.size = Pt(16)

cm_img = os.path.join(REPORT_DIR, "confusion_matrix.png")
roc_img = os.path.join(REPORT_DIR, "roc_curve.png")
if os.path.exists(cm_img):
    s8.shapes.add_picture(cm_img, Inches(6.8), Inches(1.8), width=Inches(3.1))
if os.path.exists(roc_img):
    s8.shapes.add_picture(roc_img, Inches(10.0), Inches(1.8), width=Inches(3.1))

# ----------------- SLIDE 9: GUI Demonstration & Features -----------------
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "8. GUI Development (Streamlit Application)")
tb9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
tf9 = tb9.text_frame
tf9.word_wrap = True

p = tf9.paragraphs[0]
p.text = "Key Graphical User Interface Features:"
p.font.size = Pt(18)
p.font.bold = True

features = [
    ("Live Single Message Detector:", "Real-time SMS classification with probability confidence meter and instant danger badges."),
    ("Feature Extraction Inspection:", "Visual inspection of computed features (length, uppercase letters, digit counts, URLs)."),
    ("Batch File Processing:", "CSV upload module enabling batch processing of thousands of SMS messages with instant download."),
    ("Interactive EDA Dashboard:", "Embedded visualization tabs showing label distributions, histograms, and correlation heatmaps."),
    ("Model Performance Viewer:", "Dynamic viewing of confusion matrices, ROC curves, and cross-validation comparisons.")
]
for f, d in features:
    p = tf9.add_paragraph()
    p.text = f"• {f} {d}"
    p.font.size = Pt(14)

gui_img = os.path.join(REPORT_DIR, "gui_screenshot.png")
if os.path.exists(gui_img):
    s9.shapes.add_picture(gui_img, Inches(7.0), Inches(1.8), width=Inches(5.5))

# ----------------- SLIDE 10: Conclusion & Future Scope -----------------
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "9. Conclusion & Future Scope")
tb10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf10 = tb10.text_frame
tf10.word_wrap = True

p = tf10.paragraphs[0]
p.text = "Summary of Accomplishments:"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_GREEN

p = tf10.add_paragraph()
p.text = "• Successfully built an end-to-end NLP system achieving 98.48% test accuracy and 0.9915 ROC-AUC.\n• Effectively addressed text brevity challenges through custom feature engineering alongside TF-IDF n-grams.\n• Delivered a user-friendly, responsive Streamlit web application satisfying all capstone criteria."
p.font.size = Pt(16)

p = tf10.add_paragraph()
p.text = "\nFuture Roadmap:"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = C_BLUE

p = tf10.add_paragraph()
p.text = "• Multilingual & Hinglish SMS detection using multilingual BERT / IndicBERT.\n• Adversarial robustness fine-tuning against obfuscated leetspeak and invisible Unicode attacks.\n• Edge deployment using ONNX runtime / TensorFlow Lite for on-device mobile inference without privacy leaks."
p.font.size = Pt(16)

ppt_path = os.path.join(BASE_DIR, "SMS_Spam_Detection_Presentation.pptx")
prs.save(ppt_path)
print(f"Presentation saved successfully to: {ppt_path}")
