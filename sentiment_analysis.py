import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/cleaned_reviews.csv"
OUTPUT_FILE = "data/sentiment_reviews.csv"
SUMMARY_FILE = "data/product_sentiment_summary.csv"


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

print("=" * 80)
print("MULTI-PRODUCT CUSTOMER SENTIMENT ANALYSIS")
print("=" * 80)

df = pd.read_csv(INPUT_FILE)

print("\nReviews loaded:", len(df))

print(
    "Products:",
    df["product_name"].nunique()
)


# ============================================================
# 2. CREATE SENTIMENT ANALYZER
# ============================================================

analyzer = SentimentIntensityAnalyzer()


# ============================================================
# 3. CALCULATE SENTIMENT SCORES
# ============================================================

def calculate_sentiment_score(text):

    scores = analyzer.polarity_scores(
        str(text)
    )

    return scores["compound"]


df["sentiment_score"] = (
    df["review_text"]
    .apply(calculate_sentiment_score)
)


# ============================================================
# 4. CLASSIFY SENTIMENT
# ============================================================

def classify_sentiment(score):

    if score >= 0.05:

        return "Positive"

    elif score <= -0.05:

        return "Negative"

    else:

        return "Neutral"


df["sentiment"] = (
    df["sentiment_score"]
    .apply(classify_sentiment)
)


# ============================================================
# 5. DISPLAY INDIVIDUAL REVIEWS
# ============================================================

print("\n" + "=" * 80)
print("INDIVIDUAL REVIEW SENTIMENT")
print("=" * 80)


for index, row in df.iterrows():

    print("\n" + "-" * 80)

    print(
        f"Review {index + 1}"
    )

    print(
        "Product:",
        row["product_name"]
    )

    print(
        "Customer:",
        row["customer_name"]
    )

    print(
        "Rating:",
        row["rating"]
    )

    print(
        "Review:",
        row["review_text"]
    )

    print(
        "Sentiment Score:",
        round(
            row["sentiment_score"],
            4
        )
    )

    print(
        "Sentiment:",
        row["sentiment"]
    )


# ============================================================
# 6. OVERALL SENTIMENT SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("OVERALL SENTIMENT")
print("=" * 80)


sentiment_counts = (
    df["sentiment"]
    .value_counts()
)


print(
    sentiment_counts
)


# ============================================================
# 7. OVERALL SENTIMENT PERCENTAGE
# ============================================================

print("\n" + "=" * 80)
print("OVERALL SENTIMENT PERCENTAGE")
print("=" * 80)


sentiment_percentage = (
    df["sentiment"]
    .value_counts(
        normalize=True
    )
    * 100
)


for sentiment, percentage in (
    sentiment_percentage.items()
):

    print(
        f"{sentiment}: "
        f"{percentage:.2f}%"
    )


# ============================================================
# 8. PRODUCT-LEVEL SENTIMENT ANALYSIS
# ============================================================

product_summary = (
    df.groupby("product_name")
    .agg(

        review_count=(
            "review_text",
            "count"
        ),

        average_rating=(
            "rating",
            "mean"
        ),

        average_sentiment=(
            "sentiment_score",
            "mean"
        ),

        total_helpful_votes=(
            "helpful_votes",
            "sum"
        )

    )
    .reset_index()
)


# ============================================================
# 9. SENTIMENT COUNTS PER PRODUCT
# ============================================================

sentiment_counts_by_product = (
    pd.crosstab(
        df["product_name"],
        df["sentiment"]
    )
    .reset_index()
)


# Make sure all columns exist
for sentiment in [
    "Positive",
    "Neutral",
    "Negative"
]:

    if sentiment not in (
        sentiment_counts_by_product.columns
    ):

        sentiment_counts_by_product[
            sentiment
        ] = 0


# ============================================================
# 10. MERGE PRODUCT SUMMARIES
# ============================================================

product_summary = product_summary.merge(
    sentiment_counts_by_product,
    on="product_name",
    how="left"
)


# ============================================================
# 11. CALCULATE SENTIMENT PERCENTAGES
# ============================================================

product_summary["positive_percentage"] = (
    product_summary["Positive"]
    / product_summary["review_count"]
    * 100
)


product_summary["neutral_percentage"] = (
    product_summary["Neutral"]
    / product_summary["review_count"]
    * 100
)


product_summary["negative_percentage"] = (
    product_summary["Negative"]
    / product_summary["review_count"]
    * 100
)


# ============================================================
# 12. ROUND VALUES
# ============================================================

product_summary[
    "average_rating"
] = product_summary[
    "average_rating"
].round(2)


product_summary[
    "average_sentiment"
] = product_summary[
    "average_sentiment"
].round(4)


product_summary[
    "positive_percentage"
] = product_summary[
    "positive_percentage"
].round(2)


product_summary[
    "neutral_percentage"
] = product_summary[
    "neutral_percentage"
].round(2)


product_summary[
    "negative_percentage"
] = product_summary[
    "negative_percentage"
].round(2)


# ============================================================
# 13. DISPLAY PRODUCT SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("PRODUCT SENTIMENT SUMMARY")
print("=" * 80)


print(
    product_summary.to_string(
        index=False
    )
)


# ============================================================
# 14. MOST POSITIVE REVIEW
# ============================================================

most_positive = df.loc[
    df["sentiment_score"].idxmax()
]


print("\n" + "=" * 80)
print("MOST POSITIVE REVIEW")
print("=" * 80)


print(
    "Product:",
    most_positive["product_name"]
)

print(
    "Customer:",
    most_positive["customer_name"]
)

print(
    "Rating:",
    most_positive["rating"]
)

print(
    "Sentiment Score:",
    round(
        most_positive["sentiment_score"],
        4
    )
)

print(
    "Review:",
    most_positive["review_text"]
)


# ============================================================
# 15. MOST NEGATIVE REVIEW
# ============================================================

most_negative = df.loc[
    df["sentiment_score"].idxmin()
]


print("\n" + "=" * 80)
print("MOST NEGATIVE REVIEW")
print("=" * 80)


print(
    "Product:",
    most_negative["product_name"]
)

print(
    "Customer:",
    most_negative["customer_name"]
)

print(
    "Rating:",
    most_negative["rating"]
)

print(
    "Sentiment Score:",
    round(
        most_negative["sentiment_score"],
        4
    )
)

print(
    "Review:",
    most_negative["review_text"]
)


# ============================================================
# 16. MOST HELPFUL REVIEW
# ============================================================

most_helpful = df.loc[
    df["helpful_votes"].idxmax()
]


print("\n" + "=" * 80)
print("MOST HELPFUL REVIEW")
print("=" * 80)


print(
    "Product:",
    most_helpful["product_name"]
)

print(
    "Customer:",
    most_helpful["customer_name"]
)

print(
    "Helpful Votes:",
    most_helpful["helpful_votes"]
)

print(
    "Review:",
    most_helpful["review_text"]
)


# ============================================================
# 17. SAVE REVIEW-LEVEL SENTIMENT
# ============================================================

os.makedirs(
    "data",
    exist_ok=True
)


df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 18. SAVE PRODUCT SUMMARY
# ============================================================

product_summary.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 19. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 80)
print("SENTIMENT ANALYSIS COMPLETED")
print("=" * 80)

print(
    "Review-level results:",
    OUTPUT_FILE
)

print(
    "Product-level summary:",
    SUMMARY_FILE
)