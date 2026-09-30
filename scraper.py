
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin
import time


# ============================================================
# SETTINGS
# ============================================================

BASE_URL = "https://scrapifydatalabs.com"

MARKETPLACE_URL = (
    "https://scrapifydatalabs.com/playground/ecommerce/"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ============================================================
# FUNCTION: DOWNLOAD WEB PAGE
# ============================================================

def get_soup(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        print(f"Request: {url}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:

            return BeautifulSoup(
                response.text,
                "html.parser"
            )

        return None

    except requests.RequestException as error:

        print("Request failed:", error)

        return None


# ============================================================
# START SCRAPER
# ============================================================

print("=" * 80)
print("SCRAPIFY E-COMMERCE CUSTOMER REVIEW SCRAPER")
print("=" * 80)


# ============================================================
# STEP 1: OPEN MARKETPLACE
# ============================================================

marketplace_soup = get_soup(
    MARKETPLACE_URL
)

if marketplace_soup is None:

    print("\nCould not access marketplace.")
    exit()


# ============================================================
# STEP 2: DISCOVER UNIQUE PRODUCT URLS
# ============================================================

print("\n" + "=" * 80)
print("DISCOVERING PRODUCT PAGES")
print("=" * 80)


product_urls = set()


for link in marketplace_soup.find_all(
    "a",
    href=True
):

    href = link.get("href")

    # Only consider product detail URLs
    if "/product-" in href:

        # Convert relative URL to absolute URL
        full_url = urljoin(
            BASE_URL,
            href
        )

        # Remove #reviews or any other URL fragment
        full_url = full_url.split("#")[0]

        # Add to set to automatically remove duplicates
        product_urls.add(full_url)


# ============================================================
# DISPLAY DISCOVERED PRODUCTS
# ============================================================

print(
    "\nUnique product pages discovered:",
    len(product_urls)
)

for number, url in enumerate(
    sorted(product_urls),
    start=1
):

    print(
        f"{number}. {url}"
    )


# ============================================================
# CHECK FOR PRODUCTS
# ============================================================

if not product_urls:

    print(
        "\nNo product pages were found."
    )

    print(
        "Please inspect the marketplace HTML "
        "for the correct product-link structure."
    )

    exit()


# ============================================================
# STEP 3: SCRAPE PRODUCTS
# ============================================================

all_reviews = []


for product_number, product_url in enumerate(
    sorted(product_urls),
    start=1
):

    print("\n" + "=" * 80)

    print(
        f"SCRAPING PRODUCT "
        f"{product_number}/{len(product_urls)}"
    )

    print("=" * 80)


    # --------------------------------------------------------
    # Download product page
    # --------------------------------------------------------

    product_soup = get_soup(
        product_url
    )

    if product_soup is None:

        print(
            "Skipping this product."
        )

        continue


    # --------------------------------------------------------
    # Extract product name
    # --------------------------------------------------------

    product_element = product_soup.select_one(
        "#productTitle"
    )

    if product_element:

        product_name = (
            product_element
            .get_text(strip=True)
        )

    else:

        product_name = "Unknown Product"


    print("\nProduct:")
    print(product_name)


    # --------------------------------------------------------
    # Find customer reviews
    # --------------------------------------------------------

    reviews = product_soup.select(
        "#cm-cr-dp-review-list .sf-review"
    )

    print(
        "Reviews found:",
        len(reviews)
    )


    # ========================================================
    # STEP 4: EXTRACT EACH REVIEW
    # ========================================================

    for review_number, review in enumerate(
        reviews,
        start=1
    ):

        # ----------------------------------------------------
        # Customer Name
        # ----------------------------------------------------

        reviewer_element = review.select_one(
            ".reviewer"
        )

        if reviewer_element:

            customer_name = (
                reviewer_element
                .get_text(strip=True)
            )

        else:

            customer_name = "Unknown"


        # ----------------------------------------------------
        # Rating
        # ----------------------------------------------------

        rating = review.get(
            "data-rating",
            "0"
        )

        try:

            rating = int(rating)

        except ValueError:

            rating = 0


        # ----------------------------------------------------
        # Review Title
        # ----------------------------------------------------

        title_element = review.select_one(
            ".sf-review-title"
        )

        if title_element:

            review_title = (
                title_element
                .get_text(strip=True)
            )

        else:

            review_title = "No title"


        # ----------------------------------------------------
        # Verified Purchase
        # ----------------------------------------------------

        verified_element = review.select_one(
            ".sf-verified"
        )

        if verified_element:

            verified_value = (
                verified_element
                .get(
                    "data-verified",
                    "false"
                )
                .lower()
            )

            verified_purchase = (
                verified_value == "true"
            )

        else:

            verified_purchase = False


        # ----------------------------------------------------
        # Review Date
        # ----------------------------------------------------

        date_element = review.select_one(
            "time"
        )

        if date_element:

            review_date = date_element.get(
                "datetime",
                "Unknown"
            )

        else:

            review_date = "Unknown"


        # ----------------------------------------------------
        # Review Text
        # ----------------------------------------------------

        body_element = review.select_one(
            ".sf-review-body"
        )

        if body_element:

            review_text = (
                body_element
                .get_text(
                    " ",
                    strip=True
                )
            )

        else:

            review_text = ""


        # ----------------------------------------------------
        # Helpful Votes
        # ----------------------------------------------------

        helpful_element = review.select_one(
            ".sf-helpful"
        )

        if helpful_element:

            helpful_votes = helpful_element.get(
                "data-helpful-votes",
                "0"
            )

        else:

            helpful_votes = "0"


        try:

            helpful_votes = int(
                helpful_votes
            )

        except ValueError:

            helpful_votes = 0


        # ----------------------------------------------------
        # Review ID
        # ----------------------------------------------------

        review_id = review.get(
            "data-review-id",
            ""
        )


        # ----------------------------------------------------
        # Store Review
        # ----------------------------------------------------

        all_reviews.append({

            "product_name": product_name,

            "customer_name": customer_name,

            "rating": rating,

            "review_title": review_title,

            "verified_purchase": verified_purchase,

            "review_date": review_date,

            "review_text": review_text,

            "helpful_votes": helpful_votes,

            "review_id": review_id,

            "product_url": product_url

        })


    # --------------------------------------------------------
    # Delay between requests
    # --------------------------------------------------------

    time.sleep(1)


# ============================================================
# STEP 5: CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(
    all_reviews
)


# ============================================================
# STEP 6: REMOVE DUPLICATE REVIEWS
# ============================================================

if not df.empty:

    # Prefer review ID when available
    if "review_id" in df.columns:

        df = df.drop_duplicates(
            subset=["review_id"],
            keep="first"
        )

    # Additional protection against duplicates
    df = df.drop_duplicates(
        subset=[
            "product_name",
            "customer_name",
            "review_text"
        ],
        keep="first"
    )


# ============================================================
# STEP 7: CREATE DATA DIRECTORY
# ============================================================

os.makedirs(
    "data",
    exist_ok=True
)


# ============================================================
# STEP 8: SAVE RAW DATA
# ============================================================

output_file = (
    "data/raw_reviews.csv"
)

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# STEP 9: DISPLAY SCRAPING SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("SCRAPING SUMMARY")
print("=" * 80)


if not df.empty:

    unique_products = (
        df["product_name"]
        .nunique()
    )

    total_reviews = len(df)

    print(
        "Products scraped:",
        unique_products
    )

    print(
        "Total unique reviews:",
        total_reviews
    )


    # --------------------------------------------------------
    # Product-wise review count
    # --------------------------------------------------------

    print("\n" + "-" * 80)
    print("REVIEWS BY PRODUCT")
    print("-" * 80)

    product_counts = (
        df["product_name"]
        .value_counts()
    )

    for product, count in product_counts.items():

        print(
            f"{product}: {count} reviews"
        )


else:

    print(
        "No reviews were collected."
    )


# ============================================================
# STEP 10: DISPLAY SAMPLE DATA
# ============================================================

if not df.empty:

    print("\n" + "=" * 80)
    print("FIRST FIVE REVIEWS")
    print("=" * 80)

    display_columns = [
        "product_name",
        "customer_name",
        "rating",
        "review_title",
        "verified_purchase",
        "review_date",
        "review_text",
        "helpful_votes"
    ]

    print(
        df[display_columns]
        .head()
        .to_string(index=False)
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 80)
print("SCRAPING COMPLETED")
print("=" * 80)

print(
    "Raw data saved to:",
    output_file
)
