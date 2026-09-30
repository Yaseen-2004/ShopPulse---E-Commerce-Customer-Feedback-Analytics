import os
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ShopPulse - Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("📊 ShopPulse")
st.subheader("E-Commerce Customer Feedback Analytics")

st.write(
    "Analyze customer reviews collected through web scraping "
    "using sentiment analysis, ratings and feature-level feedback."
)

st.divider()


# ============================================================
# DATA FILES
# ============================================================

REVIEWS_FILE = "data/sentiment_reviews.csv"
SUMMARY_FILE = "data/product_sentiment_summary.csv"
FEATURE_FILE = "data/feature_feedback.csv"


# ============================================================
# CHECK FILES
# ============================================================

required_files = [
    REVIEWS_FILE,
    SUMMARY_FILE,
    FEATURE_FILE
]

missing_files = [
    file for file in required_files
    if not os.path.exists(file)
]

if missing_files:

    st.error("Required data files are missing.")

    st.write("Missing files:")

    for file in missing_files:
        st.write(f"- {file}")

    st.info(
        "Run your scraping and analysis pipeline before starting "
        "the dashboard."
    )

    st.code(
        """
python scraper.py
python data_cleaning.py
python sentiment_analysis.py
python customer_insights.py
        """
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    reviews = pd.read_csv(
        REVIEWS_FILE
    )

    summary = pd.read_csv(
        SUMMARY_FILE
    )

    features = pd.read_csv(
        FEATURE_FILE
    )

    return reviews, summary, features


reviews, summary, features = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("ShopPulse")

    st.caption(
        "Customer Feedback Intelligence"
    )

    st.divider()

    st.subheader("Product Filter")

    products = sorted(
        reviews[
            "product_name"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_product = st.selectbox(
        "Choose a product",
        ["All Products"] + products
    )

    st.divider()

    st.subheader("Analytics Pipeline")

    st.write("🕷️ Web Scraping")
    st.write("🧹 Data Cleaning")
    st.write("🧠 Sentiment Analysis")
    st.write("📊 Customer Insights")
    st.write("📈 Visualization")

    st.divider()

    st.caption(
        "Built using Python, BeautifulSoup, Pandas, "
        "VADER and Streamlit."
    )


# ============================================================
# FILTER DATA
# ============================================================

if selected_product == "All Products":

    filtered_reviews = reviews.copy()

else:

    filtered_reviews = reviews[
        reviews["product_name"] == selected_product
    ].copy()


# ============================================================
# BASIC METRICS
# ============================================================

total_reviews = len(
    filtered_reviews
)

average_rating = (
    filtered_reviews["rating"].mean()
    if total_reviews > 0
    else 0
)

average_sentiment = (
    filtered_reviews["sentiment_score"].mean()
    if total_reviews > 0
    else 0
)

positive_reviews = len(
    filtered_reviews[
        filtered_reviews["sentiment"] == "Positive"
    ]
)

neutral_reviews = len(
    filtered_reviews[
        filtered_reviews["sentiment"] == "Neutral"
    ]
)

negative_reviews = len(
    filtered_reviews[
        filtered_reviews["sentiment"] == "Negative"
    ]
)

helpful_votes = int(
    filtered_reviews[
        "helpful_votes"
    ].sum()
)


# ============================================================
# OVERVIEW
# ============================================================

st.header("Overview")

st.caption(
    "Key indicators from customer feedback."
)

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.metric(
        "Total Reviews",
        total_reviews
    )

with m2:
    st.metric(
        "Average Rating",
        f"{average_rating:.2f} / 5"
    )

with m3:
    st.metric(
        "Positive Reviews",
        positive_reviews
    )

with m4:
    st.metric(
        "Negative Reviews",
        negative_reviews
    )

with m5:
    st.metric(
        "Helpful Votes",
        helpful_votes
    )


st.divider()


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

st.header("🧠 Sentiment Analysis")

st.caption(
    "Distribution of customer sentiment extracted from review text."
)

sentiment_counts = (
    filtered_reviews[
        "sentiment"
    ]
    .value_counts()
    .reindex(
        [
            "Positive",
            "Neutral",
            "Negative"
        ],
        fill_value=0
    )
)

left, right = st.columns(2)


with left:

    st.subheader(
        "Sentiment Distribution"
    )

    sentiment_chart = pd.DataFrame(
        {
            "Reviews": sentiment_counts
        }
    )

    st.bar_chart(
        sentiment_chart
    )


with right:

    st.subheader(
        "Sentiment Breakdown"
    )

    for sentiment in [
        "Positive",
        "Neutral",
        "Negative"
    ]:

        count = int(
            sentiment_counts[
                sentiment
            ]
        )

        percentage = (
            count / total_reviews * 100
            if total_reviews > 0
            else 0
        )

        st.write(
            f"**{sentiment}**"
        )

        st.progress(
            percentage / 100
        )

        st.caption(
            f"{count} reviews — "
            f"{percentage:.1f}%"
        )

    st.metric(
        "Average Sentiment Score",
        f"{average_sentiment:.4f}"
    )


st.divider()


# ============================================================
# PRODUCT COMPARISON
# ============================================================

if selected_product == "All Products":

    st.header("📦 Product Comparison")

    st.caption(
        "Compare customer ratings and sentiment across products."
    )

    comparison1, comparison2 = st.columns(2)

    with comparison1:

        st.subheader(
            "Average Rating"
        )

        rating_comparison = (
            summary[
                [
                    "product_name",
                    "average_rating"
                ]
            ]
            .set_index(
                "product_name"
            )
        )

        st.bar_chart(
            rating_comparison
        )

    with comparison2:

        st.subheader(
            "Average Sentiment"
        )

        sentiment_comparison = (
            summary[
                [
                    "product_name",
                    "average_sentiment"
                ]
            ]
            .set_index(
                "product_name"
            )
        )

        st.bar_chart(
            sentiment_comparison
        )

    st.subheader(
        "Product Summary"
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()


# ============================================================
# FEATURE ANALYSIS
# ============================================================

st.header("🔍 Customer Feature Insights")

st.caption(
    "Identify the product features customers mention in their reviews."
)


feature_filtered = features[
    features[
        "product_name"
    ].isin(
        filtered_reviews[
            "product_name"
        ].unique()
    )
].copy()


if not feature_filtered.empty:

    feature_summary = (
        feature_filtered
        .groupby("feature")
        .agg(
            mentions=(
                "mentions",
                "sum"
            ),
            positive_mentions=(
                "positive_mentions",
                "sum"
            ),
            negative_mentions=(
                "negative_mentions",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "mentions",
            ascending=False
        )
    )

    feature_left, feature_right = st.columns(2)

    with feature_left:

        st.subheader(
            "Most Mentioned Features"
        )

        feature_chart = (
            feature_summary[
                [
                    "feature",
                    "mentions"
                ]
            ]
            .set_index(
                "feature"
            )
        )

        st.bar_chart(
            feature_chart
        )

    with feature_right:

        st.subheader(
            "Feature Feedback"
        )

        st.dataframe(
            feature_summary,
            use_container_width=True,
            hide_index=True
        )

else:

    st.info(
        "No feature-level feedback available "
        "for the selected product."
    )


st.divider()


# ============================================================
# CUSTOMER REVIEWS
# ============================================================

st.header("💬 Customer Reviews")

st.caption(
    "Actual customer feedback collected from the e-commerce website."
)


sort_option = st.selectbox(
    "Sort reviews by",
    [
        "Most Helpful",
        "Highest Rating",
        "Lowest Rating"
    ]
)


if sort_option == "Most Helpful":

    display_reviews = (
        filtered_reviews
        .sort_values(
            "helpful_votes",
            ascending=False
        )
    )

elif sort_option == "Highest Rating":

    display_reviews = (
        filtered_reviews
        .sort_values(
            "rating",
            ascending=False
        )
    )

else:

    display_reviews = (
        filtered_reviews
        .sort_values(
            "rating",
            ascending=True
        )
    )


# ============================================================
# REVIEW DISPLAY
# ============================================================

for index, row in display_reviews.iterrows():

    rating = int(
        row["rating"]
    )

    stars = (
        "★" * rating
        +
        "☆" * (5 - rating)
    )

    sentiment = row[
        "sentiment"
    ]

    with st.container(
        border=True
    ):

        review_col1, review_col2 = st.columns(
            [4, 1]
        )

        with review_col1:

            st.subheader(
                row["review_title"]
            )

            st.write(
                f"**Customer:** "
                f"{row['customer_name']}"
            )

            st.caption(
                row["product_name"]
            )

        with review_col2:

            st.write(
                f"### {stars}"
            )

            if sentiment == "Positive":

                st.success(
                    "Positive"
                )

            elif sentiment == "Negative":

                st.error(
                    "Negative"
                )

            else:

                st.warning(
                    "Neutral"
                )

        st.write(
            row["review_text"]
        )

        meta_col1, meta_col2 = st.columns(2)

        with meta_col1:

            st.caption(
                f"Helpful votes: "
                f"{int(row['helpful_votes'])}"
            )

        with meta_col2:

            st.caption(
                f"Sentiment score: "
                f"{row['sentiment_score']:.4f}"
            )


st.divider()


# ============================================================
# DATA EXPLORER
# ============================================================

st.header("🗃️ Data Explorer")

st.caption(
    "View the structured dataset generated by the analysis pipeline."
)

tab1, tab2, tab3 = st.tabs(
    [
        "Reviews",
        "Product Summary",
        "Feature Feedback"
    ]
)


with tab1:

    st.dataframe(
        filtered_reviews,
        use_container_width=True,
        hide_index=True
    )


with tab2:

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


with tab3:

    st.dataframe(
        features,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DOWNLOAD
# ============================================================

st.header("⬇️ Export Data")

csv_data = filtered_reviews.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Filtered Reviews CSV",
    data=csv_data,
    file_name="customer_reviews.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ShopPulse Customer Analytics | "
    "Web Scraping → Data Cleaning → "
    "Sentiment Analysis → Customer Insights"
)