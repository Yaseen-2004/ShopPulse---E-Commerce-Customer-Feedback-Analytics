import pandas as pd


# ============================================================
# LOAD DATA
# ============================================================

reviews = pd.read_csv(
    "data/sentiment_reviews.csv"
)

summary = pd.read_csv(
    "data/product_sentiment_summary.csv"
)

features = pd.read_csv(
    "data/feature_feedback.csv"
)


# ============================================================
# REPORT HEADER
# ============================================================

print("\n")
print("=" * 100)
print("E-COMMERCE CUSTOMER FEEDBACK REPORT")
print("=" * 100)


# ============================================================
# OVERALL STATISTICS
# ============================================================

print("\nOVERALL STATISTICS")
print("-" * 100)

print(
    "Products analyzed:",
    reviews["product_name"].nunique()
)

print(
    "Total reviews:",
    len(reviews)
)

print(
    "Average rating:",
    round(
        reviews["rating"].mean(),
        2
    )
)

print(
    "Average sentiment:",
    round(
        reviews["sentiment_score"].mean(),
        4
    )
)


# ============================================================
# SENTIMENT
# ============================================================

print("\nSENTIMENT DISTRIBUTION")
print("-" * 100)

sentiment_counts = (
    reviews["sentiment"]
    .value_counts()
)


for sentiment, count in sentiment_counts.items():

    percentage = (
        count / len(reviews) * 100
    )

    print(
        f"{sentiment}: "
        f"{count} reviews "
        f"({percentage:.2f}%)"
    )


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

print("\nPRODUCT ANALYSIS")
print("-" * 100)


for _, product in summary.iterrows():

    print("\n" + product["product_name"])

    print(
        "Reviews:",
        int(product["review_count"])
    )

    print(
        "Average Rating:",
        product["average_rating"]
    )

    print(
        "Average Sentiment:",
        product["average_sentiment"]
    )

    print(
        "Positive:",
        f"{product['positive_percentage']:.2f}%"
    )

    print(
        "Neutral:",
        f"{product['neutral_percentage']:.2f}%"
    )

    print(
        "Negative:",
        f"{product['negative_percentage']:.2f}%"
    )


# ============================================================
# MOST HELPFUL REVIEWS
# ============================================================

print("\nMOST HELPFUL REVIEWS")
print("-" * 100)


top_reviews = (
    reviews
    .sort_values(
        "helpful_votes",
        ascending=False
    )
    .head(5)
)


for _, review in top_reviews.iterrows():

    print(
        f"\n{review['customer_name']} "
        f"— {review['helpful_votes']} helpful votes"
    )

    print(
        review["review_title"]
    )

    print(
        review["review_text"]
    )


# ============================================================
# NEGATIVE FEEDBACK
# ============================================================

print("\nNEGATIVE CUSTOMER FEEDBACK")
print("-" * 100)


negative_reviews = reviews[
    reviews["sentiment"] == "Negative"
]


if len(negative_reviews) == 0:

    print(
        "No negative reviews detected."
    )

else:

    for _, review in negative_reviews.iterrows():

        print(
            f"\nProduct: "
            f"{review['product_name']}"
        )

        print(
            f"Customer: "
            f"{review['customer_name']}"
        )

        print(
            f"Rating: "
            f"{review['rating']}"
        )

        print(
            f"Review: "
            f"{review['review_text']}"
        )


# ============================================================
# FEATURE FEEDBACK
# ============================================================

print("\nFEATURE-LEVEL CUSTOMER FEEDBACK")
print("-" * 100)


for product in features[
    "product_name"
].unique():

    print("\nProduct:")
    print(product)


    product_features = features[
        features["product_name"] == product
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


    for _, feature in (
        product_features.iterrows()
    ):

        print(
            f"{feature['feature']}: "
            f"{int(feature['mentions'])} mentions"
        )


# ============================================================
# END
# ============================================================

print("\n")
print("=" * 100)
print("REPORT GENERATION COMPLETED")
print("=" * 100)