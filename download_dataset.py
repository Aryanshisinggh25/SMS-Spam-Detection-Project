"""
Download the SMS Spam Collection dataset.
Run this script once to get the data.
"""
import urllib.request
import zipfile
import os

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
DEST_DIR = os.path.join(os.path.dirname(__file__), "data")
ZIP_PATH = os.path.join(DEST_DIR, "smsspamcollection.zip")
DATA_PATH = os.path.join(DEST_DIR, "SMSSpamCollection")

os.makedirs(DEST_DIR, exist_ok=True)

if os.path.exists(DATA_PATH):
    print(f"Dataset already exists at {DATA_PATH}")
else:
    print("Downloading SMS Spam Collection dataset...")
    urllib.request.urlretrieve(URL, ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DEST_DIR)
    os.remove(ZIP_PATH)
    print(f"Dataset saved to {DATA_PATH}")
