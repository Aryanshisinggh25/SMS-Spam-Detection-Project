"""
SMS Spam Detection - Data Preprocessing Module
"""

import os
import re
import string
import pandas as pd
import nltk

# ── Point NLTK to the local copy inside the project folder ───────────────────
_BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
_NLTK_DATA  = os.path.join(_BASE_DIR, "nltk_data")
_MPLCFG     = os.path.join(_BASE_DIR, ".mplconfig")
os.makedirs(_MPLCFG, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", _MPLCFG)

if _NLTK_DATA not in nltk.data.path:
    nltk.data.path.insert(0, _NLTK_DATA)

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words("english"))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_data(path: str) -> pd.DataFrame:
    """
    Load the SMS Spam Collection dataset.

    Parameters
    ----------
    path : str
        Path to the tab-separated SMS Spam Collection file.

    Returns
    -------
    pd.DataFrame with columns ['label', 'message']
    """
    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="latin-1",
    )
    # Drop any extra columns that may appear in some versions
    df = df[["label", "message"]].dropna()
    df["label"] = df["label"].str.strip().str.lower()
    return df


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

def clean_text(text: str, use_stemming: bool = False) -> str:
    """
    Clean and normalise a single SMS message.

    Steps:
      1. Lowercase
      2. Remove URLs
      3. Remove phone numbers
      4. Remove currency symbols → 'money'
      5. Remove punctuation & numbers
      6. Tokenise
      7. Remove stopwords
      8. Stem OR lemmatize (default: lemmatize)

    Parameters
    ----------
    text        : raw SMS text
    use_stemming: use PorterStemmer if True, else WordNetLemmatizer

    Returns
    -------
    Cleaned string
    """
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " url ", text)
    # Replace phone numbers
    text = re.sub(r"\b\d{10,}\b|\b\d[\d\s\-]{7,}\d\b", " phone ", text)
    # Replace currency amounts
    text = re.sub(r"[£$€]\s?\d+(\.\d+)?", " money ", text)
    # Remove remaining punctuation & digits
    text = re.sub(r"[^a-z\s]", " ", text)
    # Tokenise
    tokens = word_tokenize(text)
    # Remove stopwords & short tokens
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    # Stem / lemmatize
    if use_stemming:
        tokens = [stemmer.stem(t) for t in tokens]
    else:
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add handcrafted features that signal spam:
      - msg_length    : character count
      - word_count    : token count
      - num_digits    : digit count
      - num_uppercase : uppercase char count
      - has_url       : contains a URL
      - has_currency  : contains £ $ €
      - num_excl      : exclamation marks
    """
    df = df.copy()
    df["msg_length"]    = df["message"].str.len()
    df["word_count"]    = df["message"].str.split().str.len()
    df["num_digits"]    = df["message"].str.count(r"\d")
    df["num_uppercase"] = df["message"].apply(lambda x: sum(1 for c in x if c.isupper()))
    df["has_url"]       = df["message"].str.contains(r"http|www", case=False, regex=True).astype(int)
    df["has_currency"]  = df["message"].str.contains(r"[£$€]", regex=True).astype(int)
    df["num_excl"]      = df["message"].str.count(r"!")
    return df


def preprocess(df: pd.DataFrame, use_stemming: bool = False) -> pd.DataFrame:
    """Full preprocessing pipeline: feature engineering + text cleaning."""
    df = add_features(df)
    df["clean_text"] = df["message"].apply(lambda x: clean_text(x, use_stemming))
    df["label_num"]  = (df["label"] == "spam").astype(int)
    return df
