"""
Jupyter Notebook-style EDA and Model Analysis Script
Run with: python eda_analysis.py
Outputs charts to reports/ folder
"""

import os
import pandas as pd
import numpy as np

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MPLCONFIGDIR", os.path.join(_BASE_DIR, ".mplconfig"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "data", "SMSSpamCollection")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

from preprocessing import load_data, preprocess

print("Loading data…")
df = load_data(DATA_PATH)
df = preprocess(df)
print(f"Loaded {len(df):,} messages — {df['label_num'].mean()*100:.1f}% spam")

# ── 1. Class distribution ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
counts = df["label"].value_counts()
axes[0].pie(counts, labels=counts.index, autopct="%1.1f%%",
            colors=["#2ecc71", "#e74c3c"], startangle=90)
axes[0].set_title("Label Distribution")
sns.countplot(x="label", data=df,
              palette={"ham": "#2ecc71", "spam": "#e74c3c"}, ax=axes[1])
axes[1].set_title("Count by Label")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "class_distribution.png"), dpi=150)
plt.close()
print("Saved class_distribution.png")

# ── 2. Length distributions ───────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for label, color in [("ham", "#2ecc71"), ("spam", "#e74c3c")]:
    subset = df[df["label"] == label]
    axes[0].hist(subset["msg_length"], bins=50, alpha=0.6, label=label, color=color)
    axes[1].hist(subset["word_count"], bins=40, alpha=0.6, label=label, color=color)
for ax, title, xlabel in zip(
    axes,
    ["Character Length Distribution", "Word Count Distribution"],
    ["Characters", "Words"],
):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "length_distribution.png"), dpi=150)
plt.close()
print("Saved length_distribution.png")

# ── 3. Top words ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for idx, (label, color) in enumerate([("ham", "#2ecc71"), ("spam", "#e74c3c")]):
    words = " ".join(df[df["label"] == label]["clean_text"]).split()
    top   = Counter(words).most_common(20)
    words_list, counts_list = zip(*top)
    axes[idx].barh(words_list[::-1], counts_list[::-1], color=color)
    axes[idx].set_title(f"Top 20 Words – {label.upper()}")
    axes[idx].set_xlabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "top_words.png"), dpi=150)
plt.close()
print("Saved top_words.png")

# ── 4. Feature correlation ────────────────────────────────────────────────────
num_feats = ["msg_length", "word_count", "num_digits",
             "num_uppercase", "has_url", "has_currency", "num_excl", "label_num"]
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(df[num_feats].corr(), annot=True, fmt=".2f",
            cmap="coolwarm", center=0, square=True, ax=ax)
ax.set_title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "correlation_heatmap.png"), dpi=150)
plt.close()
print("Saved correlation_heatmap.png")

print("\nAll EDA charts saved to reports/")
