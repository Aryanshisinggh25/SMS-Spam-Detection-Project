# SMS Spam Detection

> An end-to-end NLP project that detects spam SMS messages using classical machine learning, with a Streamlit web application for interactive predictions.

---

## 📂 Project Structure

```
Nlp project/
├── data/
│   └── SMSSpamCollection                 ← UCI dataset (tab-separated)
├── models/
│   ├── model.pkl                         ← Trained classifier (Random Forest)
│   ├── vectorizer.pkl                    ← Fitted TF-IDF vectorizer
│   └── model_name.pkl                    ← Name of champion model
├── reports/
│   ├── classification_report.txt         ← Precision, recall, F1 metrics
│   ├── confusion_matrix.png              ← Test confusion matrix
│   ├── roc_curve.png                     ← ROC curve (AUC = 0.9915)
│   ├── model_comparison.png              ← 5-fold CV comparison bar chart
│   ├── class_distribution.png            ← Class imbalance visualization
│   ├── length_distribution.png           ← Message length histograms
│   ├── top_words.png                     ← Top 20 terms for Ham vs Spam
│   └── correlation_heatmap.png           ← Feature correlation matrix
├── app.py                                ← 3-Page interactive Streamlit GUI
├── SMS_Spam_Detection.ipynb              ← Complete documented Jupyter Notebook
├── SMS_Spam_Detection_Presentation.pptx  ← 10-slide Capstone Presentation Deck
├── run_app.bat                           ← 1-click launcher for the Streamlit web app
├── preprocessing.py                      ← Text cleaning & feature engineering pipeline
├── train_model.py                        ← Model training with 5-fold CV
├── predict.py                            ← Command-line inference module
├── eda_analysis.py                       ← Standalone EDA chart generation
├── generate_ppt.py                       ← Automated slide deck generator
├── download_dataset.py                   ← Auto-downloads UCI dataset
├── requirements.txt                      ← Project dependencies
└── README.md                             ← Project documentation
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the dataset

```bash
python download_dataset.py
```

> The script downloads the **UCI SMS Spam Collection** dataset (~500 KB) automatically.

### 3. Train the model

```bash
python train_model.py
```

This will:
- Preprocess messages (cleaning, stemming/lemmatization, feature engineering)
- Compare Naive Bayes, Logistic Regression, Linear SVM, and Random Forest using 5-fold cross-validation
- Select the best model by F1 score
- Save model artefacts to `models/`
- Generate evaluation charts in `reports/`

### 4. Run the web app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🧠 ML Pipeline

### Text Preprocessing
| Step | Description |
|------|-------------|
| Lowercase | Normalize case |
| URL removal | Replace URLs with `url` token |
| Phone number removal | Replace phone numbers with `phone` token |
| Currency amounts | Replace £/$€ amounts with `money` token |
| Punctuation / digits | Removed |
| Tokenization | NLTK `word_tokenize` |
| Stopword removal | NLTK English stopwords |
| Lemmatization | WordNetLemmatizer (default) |

### Features
| Feature | Type | Description |
|---------|------|-------------|
| TF-IDF | Sparse (8,000 dims) | Unigrams + bigrams, sublinear TF |
| `msg_length` | Numeric | Character count |
| `word_count` | Numeric | Token count |
| `num_digits` | Numeric | Digit count |
| `num_uppercase` | Numeric | Uppercase char count |
| `has_url` | Binary | Contains a URL |
| `has_currency` | Binary | Contains £ $ € |
| `num_excl` | Numeric | Exclamation mark count |

### Models Evaluated
- Multinomial Naive Bayes
- Logistic Regression
- Linear SVM (LinearSVC)
- Random Forest

The best-performing model by 5-fold CV F1 score is automatically saved.

---

## 📊 Results (typical)

| Metric | Value |
|--------|-------|
| Accuracy | ~98–99% |
| F1 (Spam) | ~97–99% |
| ROC-AUC | ~99% |

---

## 🌐 Web App Features

| Page | Description |
|------|-------------|
| **🔍 Predict** | Single-message classification + batch CSV upload |
| **📊 EDA & Insights** | Class distribution, length analysis, feature correlations |
| **📈 Model Performance** | Classification report, confusion matrix, ROC curve |

---

## 📦 Dataset

**UCI SMS Spam Collection Dataset**  
- 5,572 SMS messages (4,825 ham, 747 spam)  
- Source: https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection

---

## 🛠 Tech Stack

- **Python 3.10+**
- **scikit-learn** – ML models, TF-IDF, evaluation
- **NLTK** – tokenization, stopwords, lemmatization
- **pandas / numpy** – data manipulation
- **matplotlib / seaborn** – visualisations
- **Streamlit** – web interface
- **joblib** – model serialisation
