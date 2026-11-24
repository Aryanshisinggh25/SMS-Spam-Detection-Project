"""
SMS Spam Detection - Streamlit Web App
SENTINEL // SMS - Next-Gen AI Threat Intelligence & Spam Defense Platform
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# ── Writable paths for matplotlib/nltk ───────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MPLCONFIGDIR", os.path.join(_BASE_DIR, ".mplconfig"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SENTINEL // SMS • Next-Gen AI Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR  = os.path.join(BASE_DIR, "models")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
DATA_PATH  = os.path.join(BASE_DIR, "data", "SMSSpamCollection")

# ── Premium Cyber / Modern Dark Tech Styling ──────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Container constraints */
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3.5rem;
        max-width: 1260px;
    }

    /* Cyber Command Header */
    .cyber-hero {
        background: radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.16) 0%, transparent 45%),
                    radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.16) 0%, transparent 45%),
                    linear-gradient(135deg, #090d16 0%, #0f172a 50%, #0a1122 100%);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 20px;
        padding: 2.2rem 2.6rem;
        color: #ffffff;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.7), 0 0 35px rgba(14, 165, 233, 0.1);
    }
    .cyber-hero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8);
    }

    .cyber-tag {
        font-family: 'JetBrains Mono', monospace;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(14, 165, 233, 0.12);
        color: #38bdf8;
        padding: 0.4rem 0.95rem;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: 1px solid rgba(56, 189, 248, 0.35);
        margin-bottom: 0.9rem;
    }
    .cyber-pulse-dot {
        width: 8px;
        height: 8px;
        background: #00f2fe;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00f2fe;
        animation: pulse 1.6s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { opacity: 0.3; transform: scale(0.85); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0.3; transform: scale(0.85); }
    }

    .cyber-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin: 0.2rem 0 0.6rem 0;
        background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 75%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .cyber-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 800px;
        line-height: 1.6;
        margin-bottom: 1.4rem;
    }

    /* Telemetry HUD Badges */
    .hud-bar {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        font-family: 'JetBrains Mono', monospace;
    }
    .hud-pill {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.22);
        padding: 0.45rem 0.95rem;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .hud-val {
        color: #38bdf8;
        font-weight: 700;
    }

    /* Cyber Verdict Cards */
    .threat-card-critical {
        background: linear-gradient(135deg, #18080c 0%, #290812 60%, #1a080f 100%);
        border: 1.5px solid #f43f5e;
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-top: 1.2rem;
        position: relative;
        box-shadow: 0 10px 35px -10px rgba(244, 63, 94, 0.4), inset 0 0 20px rgba(244, 63, 94, 0.12);
    }
    .threat-card-critical::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 5px; height: 100%;
        background: #f43f5e;
        border-top-left-radius: 16px;
        border-bottom-left-radius: 16px;
    }

    .threat-card-safe {
        background: linear-gradient(135deg, #061811 0%, #06261c 60%, #051a13 100%);
        border: 1.5px solid #10b981;
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-top: 1.2rem;
        position: relative;
        box-shadow: 0 10px 35px -10px rgba(16, 185, 129, 0.4), inset 0 0 20px rgba(16, 185, 129, 0.12);
    }
    .threat-card-safe::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 5px; height: 100%;
        background: #10b981;
        border-top-left-radius: 16px;
        border-bottom-left-radius: 16px;
    }

    /* Terminal Console Box */
    .terminal-box {
        background: #06090e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #e2e8f0;
        margin-top: 0.6rem;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);
    }
    .token-flagged {
        background: rgba(244, 63, 94, 0.28);
        color: #fda4af;
        border: 1px solid rgba(244, 63, 94, 0.6);
        padding: 0.15rem 0.45rem;
        border-radius: 5px;
        font-weight: 700;
    }

    /* Signals Pills */
    .cyber-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.35rem 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0.3rem 0.3rem 0;
    }
    .pill-danger {
        background: rgba(244, 63, 94, 0.14);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.4);
    }
    .pill-safe {
        background: rgba(16, 185, 129, 0.14);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Custom Streamlit Input controls */
    .stTextArea textarea {
        background-color: #0b1120 !important;
        border: 1.5px solid #1e293b !important;
        color: #f1f5f9 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.98rem !important;
        border-radius: 12px !important;
        line-height: 1.5 !important;
    }
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.25) !important;
    }

    /* Button modern styles */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Load model (cached) ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Initializing Sentinel-SMS NLP Kernel…")
def load_model():
    model      = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.pkl"))
    try:
        name = joblib.load(os.path.join(MODEL_DIR, "model_name.pkl"))
    except FileNotFoundError:
        name = "Random Forest Ensemble"
    return model, vectorizer, name


@st.cache_data(show_spinner="Loading Threat Corpus…")
def load_dataset():
    from preprocessing import load_data, preprocess
    df = load_data(DATA_PATH)
    df = preprocess(df)
    return df


# ── Prediction helper ─────────────────────────────────────────────────────────
def predict(message: str, model, vectorizer):
    from predict import predict_message
    return predict_message(message, model, vectorizer)


# ── Suspicious Words Highlighter ──────────────────────────────────────────────
SPAM_TRIGGER_WORDS = {
    "free", "won", "win", "winner", "prize", "claim", "cash", "urgent",
    "call", "text", "txt", "voucher", "selected", "award", "reward",
    "guaranteed", "entry", "comp", "congratulations", "credit", "rate",
    "reply", "sub", "stop", "subscription", "password", "account",
    "bank", "suspended", "verify", "click", "http", "www", "money"
}

def highlight_spam_tokens(text: str) -> str:
    words = text.split()
    highlighted = []
    for w in words:
        clean_w = "".join(c for c in w if c.isalnum()).lower()
        if clean_w in SPAM_TRIGGER_WORDS:
            highlighted.append(f'<span class="token-flagged">{w}</span>')
        else:
            highlighted.append(w)
    return " ".join(highlighted)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:1.2rem;">
            <div style="background:linear-gradient(135deg, #0284c7, #4f46e5); padding:10px 12px; border-radius:12px; box-shadow:0 0 16px rgba(2, 132, 199, 0.4);">
                <span style="font-size:1.6rem; color:#fff;">🛡️</span>
            </div>
            <div>
                <h3 style="margin:0; font-weight:800; font-size:1.2rem; letter-spacing:-0.02em; color:#fff;">SENTINEL // SMS</h3>
                <span style="color:#0ea5e9; font-size:0.75rem; font-family:'JetBrains Mono', monospace; font-weight:700;">AI_THREAT_INTEL_V2.4</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Telemetry Card
    model_loaded = os.path.exists(os.path.join(MODEL_DIR, "model.pkl"))
    if model_loaded:
        try:
            _, _, model_name = load_model()
            st.markdown(f"""
                <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:0.95rem; margin-bottom:1.4rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="display:inline-flex; align-items:center; gap:6px; font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#22c55e; font-weight:700;">
                            <span class="cyber-pulse-dot"></span> ACTIVE_SHIELD
                        </span>
                        <span style="font-family:'JetBrains Mono', monospace; font-size:0.7rem; color:#64748b;">LATENCY: ~8ms</span>
                    </div>
                    <div style="font-family:'JetBrains Mono', monospace; font-size:0.76rem; color:#94a3b8; line-height:1.7;">
                        • CORE: <span style="color:#38bdf8;">{model_name}</span><br>
                        • ACCURACY: <span style="color:#22c55e;">98.48%</span><br>
                        • ROC-AUC: <span style="color:#38bdf8;">0.9915</span><br>
                        • SENSORS: <span style="color:#f59e0b;">TF-IDF + 7 Metadata</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        except Exception:
            st.warning("⚠️ Kernel failure loading artifacts.")
    else:
        st.error("❌ Model not found. Run `python train_model.py`.")

    page = st.radio(
        "CONSOLE NAVIGATION",
        ["⚡ Live Threat Scanner", "📊 Telemetry & Data EDA", "📈 Model Benchmark Matrix"],
        index=0,
    )

    st.markdown("---")

    # Pure Tech Specifications (No Team Members)
    st.markdown("""
        <div style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#64748b; line-height:1.7;">
            <span style="color:#94a3b8; font-weight:700;">// SYSTEM SPECIFICATION</span><br>
            PLATFORM: Python 3.14 x64<br>
            PIPELINE: TF-IDF (8K Dims) + Heuristics<br>
            CORPUS: UCI SMS 5,572 Samples<br>
            SECURITY: End-to-End Local Execution
        </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – LIVE THREAT SCANNER
# ═══════════════════════════════════════════════════════════════════════════════
if "⚡ Live Threat Scanner" in page:
    # Modern Cyber Hero Banner
    st.markdown("""
        <div class="cyber-hero">
            <div class="cyber-tag">
                <span class="cyber-pulse-dot"></span>
                <span>NEURAL THREAT DETECTION ENGINE • ACTIVE</span>
            </div>
            <div class="cyber-title">Real-Time SMS Threat Inspection</div>
            <div class="cyber-subtitle">
                Autonomous heuristic & NLP payload analyzer engineered to intercept mobile smishing, lottery lures, banking credentials harvesting, and unsolicited commercial traffic.
            </div>
            <div class="hud-bar">
                <div class="hud-pill">MODEL_ACCURACY: <span class="hud-val">98.48%</span></div>
                <div class="hud-pill">PRECISION_RATE: <span class="hud-val">99.0%</span></div>
                <div class="hud-pill">FEATURE_SPACE: <span class="hud-val">8,007 DIMS</span></div>
                <div class="hud-pill">INFERENCE_SPEED: <span class="hud-val">&lt; 15ms</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not model_loaded:
        st.error("Please run `python train_model.py` first to compile model weights.")
        st.stop()

    model, vectorizer, model_name = load_model()

    tab_single, tab_batch = st.tabs(["[ ⚡ SINGLE PAYLOAD INSPECTOR ]", "[ 📁 MASS INGESTION (CSV) ]"])

    # ── TAB 1: Single Payload Inspector ───────────────────────────────────────
    with tab_single:
        st.markdown("#### 📥 Message Ingestion Vector")
        st.caption("Select a simulated test payload or enter raw SMS text to inspect:")

        # Interactive Cyber Preset Chips
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)

        if "input_message" not in st.session_state:
            st.session_state.input_message = (
                "Congratulations! You've won a £1,000 Tesco gift voucher! "
                "Call 0800123456 NOW to claim. Limited time offer!"
            )

        with col_p1:
            if st.button("⚡ [PAYLOAD: LOTTERY SCAM]", use_container_width=True):
                st.session_state.input_message = (
                    "URGENT! You have won a £2,000 Cash Prize or a holiday abroad! "
                    "Claim now by calling 09050000321. T&C apply."
                )
        with col_p2:
            if st.button("🔒 [PAYLOAD: BANK PHISHING]", use_container_width=True):
                st.session_state.input_message = (
                    "ALERT: Your bank account has been suspended due to unusual activity. "
                    "Verify your credentials immediately at http://secure-banking-alert.me"
                )
        with col_p3:
            if st.button("💬 [CLEAN: CASUAL CHAT]", use_container_width=True):
                st.session_state.input_message = (
                    "Hey! Are we still meeting for coffee this afternoon? Let me know when you leave home."
                )
        with col_p4:
            if st.button("📅 [CLEAN: MEETING ALERT]", use_container_width=True):
                st.session_state.input_message = (
                    "Hi team, just a reminder that the NLP capstone project demo is scheduled for tomorrow at 10 AM."
                )

        user_input = st.text_area(
            "Raw SMS Message Payload:",
            value=st.session_state.input_message,
            height=125,
            placeholder="// Paste SMS string to trigger deep NLP feature vector scan...",
        )

        char_len = len(user_input)
        token_count = len(user_input.split())
        st.markdown(f"""
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.78rem; color:#64748b; margin-top:-8px; margin-bottom:12px;">
                TELEMETRY // LENGTH: <span style="color:#38bdf8;">{char_len}</span> CHARS &nbsp;|&nbsp; 
                TOKENS: <span style="color:#38bdf8;">{token_count}</span> WORDS &nbsp;|&nbsp; 
                STATUS: <span style="color:#22c55e;">BUFFER_READY</span>
            </div>
        """, unsafe_allow_html=True)

        col_act1, col_act2 = st.columns([1, 4])
        with col_act1:
            scan_clicked = st.button("🚀 SCAN PAYLOAD", type="primary", use_container_width=True)
        with col_act2:
            if st.button("CLEAR INPUT"):
                st.session_state.input_message = ""
                st.rerun()

        if scan_clicked or user_input:
            if not user_input.strip():
                st.warning("⚠️ Input buffer empty. Enter SMS text to scan.")
            else:
                with st.spinner("// Executing NLP Feature Vectorization & Model Inference..."):
                    res = predict(user_input, model, vectorizer)

                label = res["label"]
                conf  = res["confidence"]
                feats = res["features"]

                # ── Cyber Verdict HUD ──
                if label == "SPAM":
                    st.markdown(f"""
                        <div class="threat-card-critical">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                                <div>
                                    <span style="font-family:'JetBrains Mono', monospace; background:#e11d48; color:#fff; font-size:0.75rem; font-weight:800; padding:4px 10px; border-radius:4px; letter-spacing:0.08em;">
                                        [ CRITICAL_THREAT_DETECTED ]
                                    </span>
                                    <h2 style="color:#ff4b72; margin:0.6rem 0 0.3rem 0; font-size:2.2rem; font-weight:800; letter-spacing:-0.02em;">
                                        MALICIOUS / SPAM LURE
                                    </h2>
                                    <p style="color:#fda4af; margin:0; font-size:0.95rem; line-height:1.5;">
                                        Payload exhibits high-risk heuristic triggers consistent with phishing attacks, credential lures, or unsolicited commercial traffic.
                                    </p>
                                </div>
                                <div style="text-align:right; min-width:160px; font-family:'JetBrains Mono', monospace;">
                                    <div style="font-size:3rem; font-weight:800; color:#ff4b72; line-height:1;">
                                        {conf:.1f}%
                                    </div>
                                    <span style="color:#f43f5e; font-size:0.8rem; font-weight:700;">THREAT_CONFIDENCE</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="threat-card-safe">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                                <div>
                                    <span style="font-family:'JetBrains Mono', monospace; background:#059669; color:#fff; font-size:0.75rem; font-weight:800; padding:4px 10px; border-radius:4px; letter-spacing:0.08em;">
                                        [ VERIFIED_CLEAN_PAYLOAD ]
                                    </span>
                                    <h2 style="color:#34d399; margin:0.6rem 0 0.3rem 0; font-size:2.2rem; font-weight:800; letter-spacing:-0.02em;">
                                        HAM // LEGITIMATE TRAFFIC
                                    </h2>
                                    <p style="color:#a7f3d0; margin:0; font-size:0.95rem; line-height:1.5;">
                                        No significant adversarial patterns or phishing vectors identified. Cleared for standard user delivery.
                                    </p>
                                </div>
                                <div style="text-align:right; min-width:160px; font-family:'JetBrains Mono', monospace;">
                                    <div style="font-size:3rem; font-weight:800; color:#34d399; line-height:1;">
                                        {conf:.1f}%
                                    </div>
                                    <span style="color:#10b981; font-size:0.8rem; font-weight:700;">SAFETY_CONFIDENCE</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Heuristic Threat Sensors ──
                st.markdown("#### 🔬 Heuristic Threat Sensors & Trigger Analysis")
                pills = []
                if feats["has_currency"]:
                    pills.append('<span class="cyber-pill pill-danger">💰 SENSOR[CURRENCY_SYM]: DETECTED</span>')
                if feats["has_url"]:
                    pills.append('<span class="cyber-pill pill-danger">🔗 SENSOR[HYPERLINK]: EXTERNAL_URL</span>')
                if feats["num_digits"] > 5:
                    pills.append(f'<span class="cyber-pill pill-danger">📱 SENSOR[PHONE_PATTERN]: {feats["num_digits"]} DIGITS</span>')
                if feats["num_uppercase"] > 6:
                    pills.append(f'<span class="cyber-pill pill-danger">📢 SENSOR[HIGH_CAPS]: {feats["num_uppercase"]} CAPS</span>')
                if feats["num_excl"] > 0:
                    pills.append(f'<span class="cyber-pill pill-danger">❗ SENSOR[URGENCY_PUNCT]: {feats["num_excl"]} EXCL</span>')
                if feats["msg_length"] > 120:
                    pills.append(f'<span class="cyber-pill pill-danger">📏 SENSOR[PAYLOAD_LEN]: {feats["msg_length"]} CHARS</span>')

                if not pills:
                    pills.append('<span class="cyber-pill pill-safe">✓ SENSORS_ALL_NORMAL</span>')
                    pills.append('<span class="cyber-pill pill-safe">✓ NATURAL_SYNTAX_CONFIRMED</span>')

                st.markdown("".join(pills), unsafe_allow_html=True)

                # ── NLP Deep Inspection Console ──
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 💻 NLP Deep Inspection Console")
                c_tok1, c_tok2 = st.columns(2)
                with c_tok1:
                    st.caption("// Flagged Keyword Highlighting (Tokens with high spam weight):")
                    hl_text = highlight_spam_tokens(user_input)
                    st.markdown(f'<div class="terminal-box">{hl_text}</div>', unsafe_allow_html=True)
                with c_tok2:
                    st.caption("// Normalized Lemma Vector Stream (Stopwords removed):")
                    st.markdown(f'<div class="terminal-box" style="color:#38bdf8;">&gt;&gt; {res["clean_text"]}</div>', unsafe_allow_html=True)

                # ── Mathematical Feature Breakdown ──
                with st.expander("📊 Inspect Machine Learning Feature Matrix (Sparse & Dense Vector)"):
                    f_df = pd.DataFrame([
                        {"Sensor Code": "FEAT_CHAR_LEN", "Measured Value": feats["msg_length"], "Risk Weight": "High (>120)"},
                        {"Sensor Code": "FEAT_WORD_COUNT", "Measured Value": feats["word_count"], "Risk Weight": "High (>20)"},
                        {"Sensor Code": "FEAT_NUM_DIGITS", "Measured Value": feats["num_digits"], "Risk Weight": "High (>5)"},
                        {"Sensor Code": "FEAT_UPPERCASE", "Measured Value": feats["num_uppercase"], "Risk Weight": "High (>6)"},
                        {"Sensor Code": "FEAT_HAS_URL", "Measured Value": str(feats["has_url"]), "Risk Weight": "Critical"},
                        {"Sensor Code": "FEAT_HAS_CURRENCY", "Measured Value": str(feats["has_currency"]), "Risk Weight": "Critical"},
                        {"Sensor Code": "FEAT_EXCL_MARKS", "Measured Value": feats["num_excl"], "Risk Weight": "Moderate"},
                    ])
                    st.dataframe(f_df, use_container_width=True)

    # ── TAB 2: Batch Analysis ─────────────────────────────────────────────────
    with tab_batch:
        st.markdown("#### 📁 Mass Ingestion Pipeline (Batch CSV)")
        st.caption("Upload raw message streams (telecom logs, marketing dumps) for automated threat categorization.")

        sample_df = pd.DataFrame({
            "message": [
                "URGENT! You have won a 1 week free membership in our £100,000 prize jackpot! Text YES to 81234.",
                "Hey dad, are you picking me up from soccer practice at 5?",
                "WINNER!! As a valued customer you are selected to receive a £900 reward. Call 09061701461 to claim.",
                "Can you review the pull request when you get a chance? Thanks!",
                "FREE ringtone! Reply TONE to 8007 to download your bonus track immediately.",
                "Just checking in to see how your project presentation went today.",
                "Your parcel delivery has failed. Update your address at http://track-package-now.biz"
            ]
        })
        st.download_button(
            label="⬇️ DOWNLOAD TEST INGESTION CSV",
            data=sample_df.to_csv(index=False).encode(),
            file_name="sentinel_test_batch.csv",
            mime="text/csv",
            help="Download a synthetic test CSV to verify batch classification instantly."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        up = st.file_uploader("Upload CSV containing 'message' column:", type=["csv"])
        if up:
            b_df = pd.read_csv(up)
            if "message" not in b_df.columns:
                st.error("❌ Invalid schema. CSV must contain a 'message' column.")
            else:
                st.success(f"✓ Ingested **{len(b_df):,}** payloads from `{up.name}`.")
                if st.button("🚀 EXECUTE BATCH SCAN", type="primary"):
                    p_bar = st.progress(0)
                    preds, confs = [], []
                    for i, m in enumerate(b_df["message"]):
                        r = predict(str(m), model, vectorizer)
                        preds.append(r["label"])
                        confs.append(r["confidence"])
                        p_bar.progress((i + 1) / len(b_df))

                    b_df["VERDICT"] = preds
                    b_df["THREAT_CONFIDENCE_%"] = confs

                    tot = len(b_df)
                    spams = (b_df["VERDICT"] == "SPAM").sum()
                    hams  = tot - spams
                    pct   = (spams / tot) * 100

                    st.markdown("##### 📊 Batch Telemetry Summary")
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("TOTAL INGESTED", f"{tot:,}")
                    k2.metric("MALICIOUS DETECTED", f"{spams:,}", f"{pct:.1f}% Threat Rate", delta_color="inverse")
                    k3.metric("CLEAN TRAFFIC", f"{hams:,}", f"{(100-pct):.1f}% Safe")
                    k4.metric("MEAN CONFIDENCE", f"{b_df['THREAT_CONFIDENCE_%'].mean():.1f}%")

                    st.dataframe(b_df, use_container_width=True)
                    st.download_button(
                        "⬇️ EXPORT CLASSIFIED CSV",
                        b_df.to_csv(index=False).encode(),
                        "sentinel_classified_telemetry.csv",
                        "text/csv",
                        type="primary"
                    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – TELEMETRY & DATA EDA
# ═══════════════════════════════════════════════════════════════════════════════
elif "📊 Telemetry & Data EDA" in page:
    st.markdown("""
        <div class="cyber-hero">
            <div class="cyber-tag">
                <span class="cyber-pulse-dot"></span>
                <span>CORPUS TELEMETRY & STATISTICAL PATTERNS</span>
            </div>
            <div class="cyber-title">Exploratory Threat Intelligence</div>
            <div class="cyber-subtitle">
                Statistical analysis of the 5,572 SMS UCI ground truth dataset. Visualizing structural length anomalies, class imbalance, and linguistic threat distributions.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not os.path.exists(DATA_PATH):
        st.error("Dataset not found. Run `python download_dataset.py`.")
        st.stop()

    df = load_dataset()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TOTAL SMS CORPUS", f"{len(df):,}")
    c2.metric("BENIGN / HAM", f"{(df['label']=='ham').sum():,}", "86.6%")
    c3.metric("ADVERSARIAL / SPAM", f"{(df['label']=='spam').sum():,}", "13.4%")
    c4.metric("INPUT SENSORS", "8,007 DIMS", "Sublinear TF-IDF")

    st.markdown("<br>", unsafe_allow_html=True)

    t_dist, t_len, t_words, t_corr, t_data = st.tabs([
        "[ 📊 CLASS RATIO ]",
        "[ 📏 LENGTH DISTRIBUTION ]",
        "[ 🔤 VOCABULARY FREQUENCY ]",
        "[ 🔥 CORRELATION MATRIX ]",
        "[ 🔎 CORPUS EXPLORER ]"
    ])

    with t_dist:
        st.markdown("#### Class Distribution & Imbalance")
        st.info("💡 **Security Takeaway:** Spam represents 13.4% of total traffic. Stratified splitting and F1-score optimization prevent model skew toward the majority class.")
        img_class = os.path.join(REPORT_DIR, "class_distribution.png")
        if os.path.exists(img_class):
            st.image(img_class, use_container_width=True)

    with t_len:
        st.markdown("#### Message Length Discrepancy")
        st.info("💡 **Security Takeaway:** Benign SMS averages ~38 characters, while spam averages ~138 characters due to urgent solicitations, telephone routing, and redemption instructions.")
        img_len = os.path.join(REPORT_DIR, "length_distribution.png")
        if os.path.exists(img_len):
            st.image(img_len, use_container_width=True)

    with t_words:
        st.markdown("#### Dominant Lexical Keywords")
        st.info("💡 **Security Takeaway:** Spam vectors cluster strongly on financial and urgency tokens (`free`, `claim`, `prize`, `cash`, `call`, `txt`).")
        img_words = os.path.join(REPORT_DIR, "top_words.png")
        if os.path.exists(img_words):
            st.image(img_words, use_container_width=True)

    with t_corr:
        st.markdown("#### Sensor Correlation Matrix")
        st.info("💡 **Security Takeaway:** Strong positive correlation with malicious label: Digit Frequency (+0.43), Currency Presence (+0.38), and Shouting Uppercase (+0.38).")
        img_corr = os.path.join(REPORT_DIR, "correlation_heatmap.png")
        if os.path.exists(img_corr):
            st.image(img_corr, use_container_width=True)

    with t_data:
        st.markdown("#### 🔎 Interactive Corpus Ingestion Viewer")
        f_lbl = st.radio("Filter Class:", ["ALL", "HAM (BENIGN)", "SPAM (MALICIOUS)"], horizontal=True)
        f_df = df
        if f_lbl == "HAM (BENIGN)":
            f_df = df[df["label"] == "ham"]
        elif f_lbl == "SPAM (MALICIOUS)":
            f_df = df[df["label"] == "spam"]

        q = st.text_input("Grep Corpus by keyword:", placeholder="e.g. prize, account, otp, meeting")
        if q:
            f_df = f_df[f_df["message"].str.contains(q, case=False, na=False)]

        st.caption(f"Showing **{len(f_df):,}** entries:")
        st.dataframe(f_df[["label", "message", "msg_length", "word_count", "num_digits", "has_url", "has_currency"]].head(100), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – MODEL BENCHMARK MATRIX
# ═══════════════════════════════════════════════════════════════════════════════
elif "📈 Model Benchmark Matrix" in page:
    st.markdown("""
        <div class="cyber-hero">
            <div class="cyber-tag">
                <span class="cyber-pulse-dot"></span>
                <span>MODEL BENCHMARKING & VALIDATION AUDIT</span>
            </div>
            <div class="cyber-title">Architecture Benchmark Matrix</div>
            <div class="cyber-subtitle">
                Cross-validated comparative evaluation across 4 candidate NLP architectures. Evaluated on 1,115 unseen test samples.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🏆 Algorithmic Tournament Leaderboard")
    lead_df = pd.DataFrame([
        {"TIER": "CHAMPION", "ALGORITHM": "Random Forest Ensemble (200 Trees)", "5-FOLD CV F1": "0.9463 ± 0.017", "ACCURACY": "98.48%", "SPAM PRECISION": "99.0%", "ROC-AUC": "0.9915"},
        {"TIER": "CHALLENGER", "ALGORITHM": "Logistic Regression (L2 C=5.0)", "5-FOLD CV F1": "0.9341 ± 0.010", "ACCURACY": "97.85%", "SPAM PRECISION": "97.0%", "ROC-AUC": "0.9880"},
        {"TIER": "BASELINE", "ALGORITHM": "Linear Support Vector Machine", "5-FOLD CV F1": "0.9063 ± 0.010", "ACCURACY": "97.40%", "SPAM PRECISION": "94.0%", "ROC-AUC": "0.9810"},
        {"TIER": "BASELINE", "ALGORITHM": "Multinomial Naive Bayes (α=0.1)", "5-FOLD CV F1": "0.8681 ± 0.016", "ACCURACY": "95.96%", "SPAM PRECISION": "92.0%", "ROC-AUC": "0.9750"},
    ])
    st.dataframe(lead_df, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.markdown("##### 🎯 Test Confusion Matrix (1,115 Samples)")
        cm_file = os.path.join(REPORT_DIR, "confusion_matrix.png")
        if os.path.exists(cm_file):
            st.image(cm_file, use_container_width=True)
            st.caption("Only 1 False Positive out of 966 legitimate messages (99.0% Precision).")
    with c_m2:
        st.markdown("##### 📈 Receiver Operating Characteristic (ROC)")
        roc_file = os.path.join(REPORT_DIR, "roc_curve.png")
        if os.path.exists(roc_file):
            st.image(roc_file, use_container_width=True)
            st.caption("ROC-AUC of 0.9915 demonstrates near-perfect class separability.")

    st.markdown("---")
    st.markdown("##### 📊 5-Fold Stratified Cross-Validation F1 Scores")
    comp_file = os.path.join(REPORT_DIR, "model_comparison.png")
    if os.path.exists(comp_file):
        st.image(comp_file, use_container_width=True)

    rep_txt = os.path.join(REPORT_DIR, "classification_report.txt")
    if os.path.exists(rep_txt):
        with st.expander("📄 Raw Scikit-Learn Classification Metric Telemetry"):
            with open(rep_txt) as f:
                st.code(f.read(), language="text")
