import pandas as pd
import matplotlib.pyplot as plt
import os


# --------------------------------------------------
# 1. LOAD SENTIMENT DATA
# --------------------------------------------------

input_file = "data/sentiment_reviews.csv"

df = pd.read_csv(input_file)

print("=" * 80)
print("CUSTOMER REVIEW VISUALIZATION")
print("=" * 80)

print("Number of reviews:", len(df))


# --------------------------------------------------
# 2. CREATE OUTPUT DIRECTORY
# --------------------------------------------------

os.makedirs("output", exist_ok=True)


# --------------------------------------------------
# 3. RATING DISTRIBUTION
# --------------------------------------------------

rating_counts = df["rating"].value_counts().sort_index()

plt.figure(figsize=(8, 5))

plt.bar(
    rating_counts.index.astype(str),
    rating_counts.values
)

plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.savefig(
    "output/rating_distribution.png",
    dpi=300
)

plt.show()

print("Created: output/rating_distribution.png")


# --------------------------------------------------
# 4. SENTIMENT DISTRIBUTION
# --------------------------------------------------

sentiment_counts = df["sentiment"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    sentiment_counts.index,
    sentiment_counts.values
)

plt.title("Customer Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.savefig(
    "output/sentiment_distribution.png",
    dpi=300
)

plt.show()

print("Created: output/sentiment_distribution.png")


# --------------------------------------------------
# 5. RATING VS SENTIMENT SCORE
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["rating"],
    df["sentiment_score"],
    s=100
)

plt.title("Rating vs Sentiment Score")
plt.xlabel("Customer Rating")
plt.ylabel("Sentiment Score")

plt.axhline(
    y=0,
    linestyle="--"
)

plt.tight_layout()

plt.savefig(
    "output/rating_vs_sentiment.png",
    dpi=300
)

plt.show()

print("Created: output/rating_vs_sentiment.png")


# --------------------------------------------------
# 6. HELPFUL VOTES
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["customer_name"],
    df["helpful_votes"]
)

plt.title("Helpful Votes by Customer Review")
plt.xlabel("Customer")
plt.ylabel("Helpful Votes")

plt.tight_layout()

plt.savefig(
    "output/helpful_votes.png",
    dpi=300
)

plt.show()

print("Created: output/helpful_votes.png")


# --------------------------------------------------
# 7. REVIEW SENTIMENT BY RATING
# --------------------------------------------------

sentiment_by_rating = (
    df.groupby("rating")["sentiment_score"]
    .mean()
)

plt.figure(figsize=(8, 5))

plt.plot(
    sentiment_by_rating.index,
    sentiment_by_rating.values,
    marker="o"
)

plt.title("Average Sentiment Score by Rating")
plt.xlabel("Rating")
plt.ylabel("Average Sentiment Score")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/sentiment_by_rating.png",
    dpi=300
)

plt.show()

print("Created: output/sentiment_by_rating.png")


# --------------------------------------------------
# 8. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 80)
print("VISUALIZATION COMPLETED")
print("=" * 80)

print("All charts have been saved inside the output folder.")