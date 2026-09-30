# ShopPluse - E-Commerce Customer Feedback Analytics

An end-to-end web scraping and customer feedback analytics project that collects product reviews from an e-commerce demo website, cleans the scraped data, performs sentiment analysis, extracts customer insights, and presents the results through an interactive Streamlit dashboard.

## Project Overview

This project demonstrates a complete data analytics pipeline:

Web Scraping → Data Cleaning → Sentiment Analysis → Customer Insights → Visualization → Interactive Dashboard

The project uses an e-commerce playground website containing product information and customer reviews.

## Features

- Web scraping of product information
- Customer review extraction
- Customer name extraction
- Review title extraction
- Review text extraction
- Star rating extraction
- Verified purchase information
- Review date extraction
- Helpful vote extraction
- Data cleaning and preprocessing
- VADER-based sentiment analysis
- Positive, Neutral and Negative sentiment classification
- Average customer rating calculation
- Product-level sentiment analysis
- Feature-level customer feedback analysis
- Customer review visualization
- Interactive Streamlit dashboard
- Product filtering
- Review sorting
- Structured data exploration
- CSV export

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- NumPy
- VADER Sentiment
- Matplotlib
- Streamlit

## Project Structure

```text
ShopPluse-E-Commerce-Customer-Feedback-Analytics/
│
├── app.py
├── scraper.py
├── data_cleaning.py
├── sentiment_analysis.py
├── customer_insights.py
├── visualization.py
├── generate_report.py
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── cleaned_reviews.csv
│   ├── sentiment_reviews.csv
│   ├── product_sentiment_summary.csv
│   └── feature_feedback.csv
│
└── output/