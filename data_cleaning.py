import pandas as pd
import os


# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/raw_reviews.csv"
OUTPUT_FILE = "data/cleaned_reviews.csv"


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

print("=" * 80)
print("CUSTOMER REVIEW DATA CLEANING")
print("=" * 80)

df = pd.read_csv(INPUT_FILE)

print("\nRaw reviews loaded:", len(df))


# ============================================================
# 2. DISPLAY RAW DATA INFORMATION
# ============================================================

print("\n" + "=" * 80)
print("DATASET INFORMATION")
print("=" * 80)

print(df.info())


# ============================================================
# 3. CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 80)
print("MISSING VALUES")
print("=" * 80)

print(df.isnull().sum())


# ============================================================
# 4. REMOVE DUPLICATE REVIEWS
# ============================================================

before_duplicates = len(df)


# First use review ID when available
if "review_id" in df.columns:

    df = df.drop_duplicates(
        subset=["review_id"],
        keep="first"
    )


# Additional duplicate protection
df = df.drop_duplicates(
    subset=[
        "product_name",
        "customer_name",
        "review_text"
    ],
    keep="first"
)


after_duplicates = len(df)

print(
    "\nDuplicate reviews removed:",
    before_duplicates - after_duplicates
)


# ============================================================
# 5. CLEAN PRODUCT NAMES
# ============================================================

df["product_name"] = (
    df["product_name"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 6. CLEAN CUSTOMER NAMES
# ============================================================

df["customer_name"] = (
    df["customer_name"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 7. CLEAN REVIEW TITLES
# ============================================================

df["review_title"] = (
    df["review_title"]
    .fillna("No title")
    .astype(str)
    .str.strip()
)


# ============================================================
# 8. CLEAN REVIEW TEXT
# ============================================================

df["review_text"] = (
    df["review_text"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# 9. CONVERT RATING TO NUMERIC
# ============================================================

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)


# ============================================================
# 10. VALIDATE RATING
# ============================================================

df.loc[
    ~df["rating"].between(1, 5),
    "rating"
] = pd.NA


# ============================================================
# 11. CONVERT HELPFUL VOTES TO NUMERIC
# ============================================================

df["helpful_votes"] = pd.to_numeric(
    df["helpful_votes"],
    errors="coerce"
)


df["helpful_votes"] = (
    df["helpful_votes"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# 12. CONVERT VERIFIED PURCHASE
# ============================================================

df["verified_purchase"] = (
    df["verified_purchase"]
    .astype(str)
    .str.lower()
    .map({
        "true": True,
        "false": False
    })
)


df["verified_purchase"] = (
    df["verified_purchase"]
    .fillna(False)
)


# ============================================================
# 13. CONVERT REVIEW DATE
# ============================================================

df["review_date"] = pd.to_datetime(
    df["review_date"],
    errors="coerce"
)


# ============================================================
# 14. REMOVE REVIEWS WITHOUT TEXT
# ============================================================

before_empty = len(df)

df = df[
    df["review_text"].str.strip() != ""
]

after_empty = len(df)

print(
    "Empty reviews removed:",
    before_empty - after_empty
)


# ============================================================
# 15. REMOVE REVIEWS WITH INVALID RATINGS
# ============================================================

before_rating = len(df)

df = df[
    df["rating"].notna()
]

after_rating = len(df)

print(
    "Invalid-rating reviews removed:",
    before_rating - after_rating
)


# ============================================================
# 16. CONVERT RATING TO INTEGER
# ============================================================

df["rating"] = df["rating"].astype(int)


# ============================================================
# 17. SORT DATA
# ============================================================

df = df.sort_values(
    by=[
        "product_name",
        "review_date"
    ],
    ascending=[
        True,
        False
    ]
)


# ============================================================
# 18. RESET INDEX
# ============================================================

df = df.reset_index(drop=True)


# ============================================================
# 19. SAVE CLEANED DATA
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
# 20. PRODUCT SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("PRODUCT SUMMARY")
print("=" * 80)

product_summary = (
    df.groupby("product_name")
    .agg(
        review_count=("review_text", "count"),
        average_rating=("rating", "mean"),
        total_helpful_votes=("helpful_votes", "sum")
    )
    .reset_index()
)


product_summary["average_rating"] = (
    product_summary["average_rating"]
    .round(2)
)


print(
    product_summary.to_string(
        index=False
    )
)


# ============================================================
# 21. VERIFIED PURCHASE SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("VERIFIED PURCHASE SUMMARY")
print("=" * 80)

print(
    df["verified_purchase"]
    .value_counts()
)


# ============================================================
# 22. FINAL DATASET
# ============================================================

print("\n" + "=" * 80)
print("CLEANED DATASET")
print("=" * 80)

print(
    df.to_string(
        index=False
    )
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 80)
print("DATA CLEANING COMPLETED")
print("=" * 80)

print(
    "Final number of reviews:",
    len(df)
)

print(
    "Number of products:",
    df["product_name"].nunique()
)

print(
    "Saved to:",
    OUTPUT_FILE
)