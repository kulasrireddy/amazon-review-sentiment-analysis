# 📊 Amazon Review Sentiment Analysis

A Python-based sentiment analysis pipeline that processes Amazon product reviews using a rule-based Natural Language Processing (NLP) approach. The system stores results in a SQLite database, evaluates prediction accuracy, and visualizes sentiment distribution.

---

## 🚀 Project Overview

This project performs sentiment analysis on Amazon product reviews by:

- Cleaning and preprocessing review text
- Applying a rule-based keyword sentiment scoring system
- Comparing predicted sentiment with rating-based ground truth
- Storing processed results in a SQLite database
- Calculating model accuracy
- Generating sentiment distribution visualization

The system is optimized using multiprocessing to efficiently handle large datasets.

---

## 🛠 Tech Stack

- Python 3
- SQLite (Database Storage)
- Matplotlib (Data Visualization)
- Multiprocessing (Parallel Processing)

---

## 📂 Features

- ✅ Rule-based sentiment classification (Positive / Neutral / Negative)
- ✅ Ground truth comparison using product ratings
- ✅ Model accuracy calculation
- ✅ Parallel processing using multiple CPU cores
- ✅ Automatic chart generation (`sentiment_chart.png`)
- ✅ Persistent storage using SQLite database

---

## 🧠 Sentiment Classification Logic

### 🔹 Predicted Sentiment
Calculated using keyword scoring:

- Positive keywords → +1 score
- Negative keywords → -1 score
- Final score determines sentiment:
  - Score > 0 → Positive
  - Score < 0 → Negative
  - Score = 0 → Neutral

### 🔹 Actual Sentiment (Ground Truth)
Derived from product rating:

- Rating ≥ 4 → Positive
- Rating ≤ 2 → Negative
- Rating = 3 → Neutral

---

## 📊 Output

After execution, the program:

- Stores processed data in `amazon_sentiment.db`
- Displays model accuracy percentage
- Generates and saves a visualization chart: sentiment_chart.png

1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
  
  
