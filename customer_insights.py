import pandas as pd
import re
from collections import Counter
import os


# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/sentiment_reviews.csv"

OUTPUT_FILE = "data/customer_insights.csv"


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 80)
print("CUSTOMER FEEDBACK INSIGHTS")
print("=" * 80)

df = pd.read_csv(INPUT_FILE)

print("\nReviews loaded:", len(df))


# ============================================================
# 2. STOPWORDS
# ============================================================

stopwords = {
    "the", "and", "is", "are", "was", "were",
    "a", "an", "to", "of", "in", "on", "for",
    "with", "this", "that", "it", "my", "me",
    "i", "we", "you", "they", "he", "she",
    "have", "has", "had", "be", "been",
    "very", "but", "after", "before", "from",
    "as", "at", "or", "so", "up", "out",
    "into", "than", "too", "also", "still",
    "just", "first", "few", "more", "most",
    "its", "their", "our", "without", "same",
    "all", "can", "could", "would", "will",
    "not", "no", "do", "does", "did",
    "with", "about", "through", "during",
    "me", "myself"
}


# ============================================================
# 3. TEXT CLEANING FUNCTION
# ============================================================

def clean_text(text):

    text = str(text).lower()

    # Remove punctuation
    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# 4. EXTRACT WORDS
# ============================================================

def extract_words(text):

    text = clean_text(text)

    words = text.split()

    words = [
        word
        for word in words
        if word not in stopwords
        and len(word) > 2
    ]

    return words


# ============================================================
# 5. GLOBAL WORD FREQUENCY
# ============================================================

all_words = []

for review in df["review_text"]:

    all_words.extend(
        extract_words(review)
    )


word_counts = Counter(
    all_words
)


print("\n" + "=" * 80)
print("MOST COMMON CUSTOMER WORDS")
print("=" * 80)


for word, count in word_counts.most_common(20):

    print(
        f"{word}: {count}"
    )


# ============================================================
# 6. PRODUCT-LEVEL WORD FREQUENCY
# ============================================================

product_insights = []


for product in df["product_name"].unique():

    product_reviews = df[
        df["product_name"] == product
    ]


    words = []

    for review in product_reviews[
        "review_text"
    ]:

        words.extend(
            extract_words(review)
        )


    counts = Counter(words)


    for word, count in counts.most_common(15):

        product_insights.append({

            "product_name": product,

            "keyword": word,

            "frequency": count

        })


# ============================================================
# 7. CREATE DATAFRAME
# ============================================================

insights_df = pd.DataFrame(
    product_insights
)


# ============================================================
# 8. SAVE KEYWORD DATA
# ============================================================

insights_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 9. IDENTIFY POSITIVE REVIEW THEMES
# ============================================================

positive_reviews = df[
    df["sentiment"] == "Positive"
]


positive_words = []


for review in positive_reviews[
    "review_text"
]:

    positive_words.extend(
        extract_words(review)
    )


positive_counts = Counter(
    positive_words
)


print("\n" + "=" * 80)
print("COMMON WORDS IN POSITIVE REVIEWS")
print("=" * 80)


for word, count in (
    positive_counts.most_common(15)
):

    print(
        f"{word}: {count}"
    )


# ============================================================
# 10. IDENTIFY NEGATIVE REVIEW THEMES
# ============================================================

negative_reviews = df[
    df["sentiment"] == "Negative"
]


negative_words = []


for review in negative_reviews[
    "review_text"
]:

    negative_words.extend(
        extract_words(review)
    )


negative_counts = Counter(
    negative_words
)


print("\n" + "=" * 80)
print("COMMON WORDS IN NEGATIVE REVIEWS")
print("=" * 80)


for word, count in (
    negative_counts.most_common(15)
):

    print(
        f"{word}: {count}"
    )


# ============================================================
# 11. DEFINE PRODUCT FEATURES
# ============================================================

features = {

    "Battery": [
        "battery",
        "charge",
        "charging",
        "flight"
    ],

    "Audio": [
        "sound",
        "bass",
        "audio",
        "music",
        "anc"
    ],

    "Comfort": [
        "comfort",
        "comfortable",
        "cushions",
        "clamping"
    ],

    "Connectivity": [
        "connected",
        "connection",
        "pairing",
        "bluetooth",
        "multipoint"
    ],

    "Microphone": [
        "mic",
        "microphone",
        "zoom",
        "call",
        "calls"
    ],

    "App": [
        "app",
        "application",
        "eq",
        "presets"
    ],

    "Design": [
        "design",
        "fold",
        "foldable",
        "case"
    ]
}


# ============================================================
# 12. FEATURE MENTION ANALYSIS
# ============================================================

feature_results = []


for product in df["product_name"].unique():

    product_df = df[
        df["product_name"] == product
    ]


    for feature, keywords in features.items():

        mention_count = 0

        positive_count = 0

        negative_count = 0


        for _, row in product_df.iterrows():

            review_text = (
                str(row["review_text"])
                .lower()
            )


            found = any(
                keyword in review_text
                for keyword in keywords
            )


            if found:

                mention_count += 1


                if row["sentiment"] == "Positive":

                    positive_count += 1


                elif row["sentiment"] == "Negative":

                    negative_count += 1


        feature_results.append({

            "product_name": product,

            "feature": feature,

            "mentions": mention_count,

            "positive_mentions": positive_count,

            "negative_mentions": negative_count

        })


# ============================================================
# 13. FEATURE DATAFRAME
# ============================================================

feature_df = pd.DataFrame(
    feature_results
)


feature_output = (
    "data/feature_feedback.csv"
)


feature_df.to_csv(
    feature_output,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 14. PRINT FEATURE INSIGHTS
# ============================================================

print("\n" + "=" * 80)
print("CUSTOMER FEATURE FEEDBACK")
print("=" * 80)


for product in df["product_name"].unique():

    print("\nProduct:")
    print(product)


    product_features = feature_df[
        feature_df["product_name"] == product
    ]


    product_features = (
        product_features[
            product_features["mentions"] > 0
        ]
        .sort_values(
            "mentions",
            ascending=False
        )
    )


    for _, row in product_features.iterrows():

        print(
            f"{row['feature']}: "
            f"{int(row['mentions'])} mentions | "
            f"Positive: "
            f"{int(row['positive_mentions'])} | "
            f"Negative: "
            f"{int(row['negative_mentions'])}"
        )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 80)
print("CUSTOMER INSIGHT ANALYSIS COMPLETED")
print("=" * 80)

print(
    "Keyword data:",
    OUTPUT_FILE
)

print(
    "Feature feedback:",
    feature_output
)