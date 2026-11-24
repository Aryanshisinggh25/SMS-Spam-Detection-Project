"""
SMS Spam Detection - Model Training Module

Trains multiple classifiers, selects the best, and saves:
  - models/vectorizer.pkl
  - models/model.pkl
  - models/label_encoder.pkl (unused but kept for completeness)
  - reports/classification_report.txt
  - reports/confusion_matrix.png
  - reports/roc_curve.png
  - reports/feature_importance.png
"""

import os
import sys

# ── Set writable paths before importing matplotlib / nltk ────────────────────
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MPLCONFIGDIR", os.path.join(_BASE_DIR, ".mplconfig"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    accuracy_score,
)
from scipy.sparse import hstack
from preprocessing import load_data, preprocess

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(BASE_DIR, "data", "SMSSpamCollection")
MODEL_DIR   = os.path.join(BASE_DIR, "models")
REPORT_DIR  = os.path.join(BASE_DIR, "reports")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ------------------------------------------------------------------
# Feature matrix construction
# ------------------------------------------------------------------

def build_feature_matrix(df: pd.DataFrame, vectorizer=None, fit: bool = True):
    """
    Combine TF-IDF features with handcrafted numeric features.

    Returns (X_sparse, vectorizer)
    """
    tfidf_cols = df["clean_text"]
    num_cols   = df[["msg_length", "word_count", "num_digits",
                      "num_uppercase", "has_url", "has_currency", "num_excl"]].values

    from scipy.sparse import csr_matrix
    if fit:
        vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2,
        )
        tfidf_matrix = vectorizer.fit_transform(tfidf_cols)
    else:
        tfidf_matrix = vectorizer.transform(tfidf_cols)

    X = hstack([tfidf_matrix, csr_matrix(num_cols)])
    return X, vectorizer


# ------------------------------------------------------------------
# Training
# ------------------------------------------------------------------

def train(data_path: str = DATA_PATH):
    print("=" * 60)
    print("SMS Spam Detection – Training Pipeline")
    print("=" * 60)

    # 1. Load & preprocess
    print("\n[1/6] Loading and preprocessing data...")
    df = load_data(data_path)
    df = preprocess(df)
    print(f"      Dataset size : {len(df):,} messages")
    print(f"      Spam count   : {df['label_num'].sum():,} ({df['label_num'].mean()*100:.1f}%)")

    # 2. Split
    X_train_df, X_test_df, y_train, y_test = train_test_split(
        df, df["label_num"], test_size=0.2, random_state=42, stratify=df["label_num"]
    )

    # 3. Features
    print("\n[2/6] Building feature matrices...")
    X_train, vectorizer = build_feature_matrix(X_train_df, fit=True)
    X_test, _           = build_feature_matrix(X_test_df, vectorizer=vectorizer, fit=False)

    # 4. Compare classifiers
    print("\n[3/6] Comparing classifiers (5-fold CV)...")
    classifiers = {
        "Naive Bayes (MNB)"        : MultinomialNB(alpha=0.1),
        "Logistic Regression"      : LogisticRegression(C=5, max_iter=1000, solver="lbfgs"),
        "Linear SVM"               : LinearSVC(C=1.0, max_iter=2000),
        "Random Forest"            : RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = {}
    for name, clf in classifiers.items():
        scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)
        results[name] = scores.mean()
        print(f"      {name:<30} F1 = {scores.mean():.4f} ± {scores.std():.4f}")

    best_name = max(results, key=results.get)
    best_clf  = classifiers[best_name]
    print(f"\n      ✔ Best model: {best_name} (F1={results[best_name]:.4f})")

    # 5. Final training on full train set
    print("\n[4/6] Training best model on full training set...")
    best_clf.fit(X_train, y_train)

    # 6. Evaluation
    print("\n[5/6] Evaluating on held-out test set...")
    y_pred = best_clf.predict(X_test)

    # Probabilities (SVM uses decision function)
    if hasattr(best_clf, "predict_proba"):
        y_prob = best_clf.predict_proba(X_test)[:, 1]
    else:
        y_prob = best_clf.decision_function(X_test)

    acc  = accuracy_score(y_test, y_pred)
    auc  = roc_auc_score(y_test, y_prob)
    report = classification_report(y_test, y_pred, target_names=["Ham", "Spam"])
    print(f"\n      Accuracy : {acc:.4f}")
    print(f"      ROC-AUC  : {auc:.4f}")
    print(f"\n{report}")

    # Save text report
    with open(os.path.join(REPORT_DIR, "classification_report.txt"), "w") as f:
        f.write(f"Best Model: {best_name}\n")
        f.write(f"Accuracy : {acc:.4f}\n")
        f.write(f"ROC-AUC  : {auc:.4f}\n\n")
        f.write(report)

    # --- Confusion Matrix ---
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Ham", "Spam"], yticklabels=["Ham", "Spam"], ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix – {best_name}")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "confusion_matrix.png"), dpi=150)
    plt.close()

    # --- ROC Curve ---
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(fpr, tpr, lw=2, label=f"AUC = {auc:.4f}")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "roc_curve.png"), dpi=150)
    plt.close()

    # --- CV Comparison Bar Chart ---
    fig, ax = plt.subplots(figsize=(8, 4))
    names   = list(results.keys())
    scores  = [results[n] for n in names]
    colors  = ["#2ecc71" if n == best_name else "#3498db" for n in names]
    bars    = ax.bar(names, scores, color=colors, edgecolor="white")
    ax.set_ylim(min(scores) - 0.02, 1.0)
    ax.set_ylabel("Mean F1 Score (5-fold CV)")
    ax.set_title("Model Comparison")
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                f"{score:.4f}", ha="center", va="bottom", fontsize=9)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "model_comparison.png"), dpi=150)
    plt.close()

    # 7. Save artefacts
    print("\n[6/6] Saving model artefacts...")
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))
    joblib.dump(best_clf,   os.path.join(MODEL_DIR, "model.pkl"))
    # Also save model name for the app
    joblib.dump(best_name,  os.path.join(MODEL_DIR, "model_name.pkl"))
    print(f"      Saved to {MODEL_DIR}/")
    print("\n✅ Training complete!\n")

    return best_clf, vectorizer


if __name__ == "__main__":
    train()
