"""
SMS Spam Detection - Predict Module
"""
import os
import joblib
import pandas as pd
from preprocessing import clean_text, add_features
from scipy.sparse import hstack, csr_matrix

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR  = os.path.join(BASE_DIR, "models")


def load_artifacts():
    """Load saved model and vectorizer."""
    model      = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.pkl"))
    try:
        model_name = joblib.load(os.path.join(MODEL_DIR, "model_name.pkl"))
    except FileNotFoundError:
        model_name = "Unknown"
    return model, vectorizer, model_name


def predict_message(message: str, model=None, vectorizer=None):
    """
    Predict whether a single SMS is spam or ham.

    Returns
    -------
    dict with keys: label, confidence, clean_text, features
    """
    if model is None or vectorizer is None:
        model, vectorizer, _ = load_artifacts()

    # Build a one-row dataframe (mirrors training pipeline)
    df = pd.DataFrame({"message": [message]})
    df = add_features(df)
    df["clean_text"] = df["message"].apply(clean_text)

    tfidf_vec = vectorizer.transform(df["clean_text"])
    num_vec   = csr_matrix(df[["msg_length", "word_count", "num_digits",
                                "num_uppercase", "has_url", "has_currency",
                                "num_excl"]].values)
    X = hstack([tfidf_vec, num_vec])

    label_num = model.predict(X)[0]
    label     = "SPAM" if label_num == 1 else "HAM"

    # Confidence
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0]
        confidence = prob[label_num]
    elif hasattr(model, "decision_function"):
        score      = model.decision_function(X)[0]
        # Sigmoid-like normalisation for display
        import math
        confidence = 1 / (1 + math.exp(-abs(score)))
    else:
        confidence = 1.0

    return {
        "label"      : label,
        "confidence" : round(float(confidence) * 100, 2),
        "clean_text" : df["clean_text"].iloc[0],
        "features"   : {
            "msg_length"    : int(df["msg_length"].iloc[0]),
            "word_count"    : int(df["word_count"].iloc[0]),
            "num_digits"    : int(df["num_digits"].iloc[0]),
            "num_uppercase" : int(df["num_uppercase"].iloc[0]),
            "has_url"       : bool(df["has_url"].iloc[0]),
            "has_currency"  : bool(df["has_currency"].iloc[0]),
            "num_excl"      : int(df["num_excl"].iloc[0]),
        },
    }


if __name__ == "__main__":
    test_messages = [
        "Congratulations! You've won a £1,000 prize! Call now: 0800123456",
        "Hey, are we still on for dinner tonight? Let me know!",
        "FREE entry in 2 a wkly comp to win FA Cup final tkts! Text FA to 87121",
        "I'll be late for the meeting, sorry.",
        "URGENT: Your account has been suspended. Click http://bit.ly/xxx to restore",
    ]

    model, vec, model_name = load_artifacts()
    print(f"Using model: {model_name}\n")
    for msg in test_messages:
        result = predict_message(msg, model, vec)
        icon   = "🚨" if result["label"] == "SPAM" else "✅"
        print(f"{icon} [{result['label']} | {result['confidence']:.1f}%] {msg[:60]}...")
