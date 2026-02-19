import sqlite3
import os
import json
import re
from datetime import datetime
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt

# =====================================================
# Rule-Based Sentiment Keywords
# =====================================================
POS_KEYWORDS = ["good", "great", "excellent", "happy", "love", "best", "awesome", "perfect", "amazing"]
NEG_KEYWORDS = ["bad", "poor", "terrible", "worst", "hate", "disappointing", "awful", "broken"]

# =====================================================
# Text Cleaning
# =====================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# =====================================================
# Calculate Score
# =====================================================
def calculate_score(text):
    score = 0
    words = clean_text(text).split()

    for word in words:
        if word in POS_KEYWORDS:
            score += 1
        elif word in NEG_KEYWORDS:
            score -= 1

    return score

# =====================================================
# Get Sentiment from Score
# =====================================================
def get_sentiment(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# =====================================================
# Convert Rating to Sentiment (Ground Truth)
# =====================================================
def rating_to_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating <= 2:
        return "Negative"
    else:
        return "Neutral"

# =====================================================
# Process Single Review (for multiprocessing)
# =====================================================
def process_review(data):
    text = data.get("reviewText", "")
    rating = data.get("overall", 3)

    if not text.strip():
        return None

    score = calculate_score(text)
    predicted = get_sentiment(score)
    actual = rating_to_sentiment(rating)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (text, score, predicted, actual, timestamp)

# =====================================================
# Create Database
# =====================================================
def create_database():
    conn = sqlite3.connect("amazon_sentiment.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT,
            score INTEGER,
            predicted_sentiment TEXT,
            actual_sentiment TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

# =====================================================
# Main Processing Function (Multiprocessing)
# =====================================================
def process_file(json_file):

    if not os.path.exists(json_file):
        print("File not found!")
        return

    print("Reading JSON file...")

    data_list = []
    with open(json_file, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data_list.append(json.loads(line))
            except:
                continue

    print(f"Total Reviews Loaded: {len(data_list)}")
    print(f"Using {cpu_count()} CPU cores...\n")

    with Pool(cpu_count()) as pool:
        results = pool.map(process_review, data_list)

    # Remove None values
    results = [r for r in results if r is not None]

    # Store in DB
    conn = sqlite3.connect("amazon_sentiment.db")
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO sentiment_results 
        (review, score, predicted_sentiment, actual_sentiment, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, results)

    conn.commit()
    conn.close()

    print(f"Successfully processed {len(results)} reviews!")

# =====================================================
# Accuracy Calculation
# =====================================================
def calculate_accuracy():
    conn = sqlite3.connect("amazon_sentiment.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM sentiment_results
        WHERE predicted_sentiment = actual_sentiment
    """)
    correct = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sentiment_results")
    total = cursor.fetchone()[0]

    accuracy = (correct / total) * 100

    print(f"\nModel Accuracy: {accuracy:.2f}%")

    conn.close()

# =====================================================
# Visualization
# =====================================================
def visualize_results():
    conn = sqlite3.connect("amazon_sentiment.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT predicted_sentiment, COUNT(*)
        FROM sentiment_results
        GROUP BY predicted_sentiment
    """)

    data = cursor.fetchall()
    conn.close()

    sentiments = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure()
    plt.bar(sentiments, counts)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.savefig("sentiment_chart.png")
    plt.show()

    print("Chart saved as sentiment_chart.png")

# =====================================================
# Main
# =====================================================
if __name__ == "__main__":
    print("Starting Advanced Sentiment Analysis...\n")

    create_database()
    process_file("Cell_Phones_and_Accessories_5.json")
    calculate_accuracy()
    visualize_results()

    print("\nProject Completed Successfully 🚀")
