import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Amazon Catalog Analytics", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent

products_file = BASE_DIR / "data" / "silver" / "products_enriched.csv"
gold_category_file = BASE_DIR / "data" / "gold" / "gold_category_analytics.csv"
gold_price_band_file = BASE_DIR / "data" / "gold" / "gold_price_band_analytics.csv"
gold_bestseller_file = BASE_DIR / "data" / "gold" / "gold_bestseller_analytics.csv"

@st.cache_data
def load_data():
    products = pd.read_csv(products_file)
    gold_category = pd.read_csv(gold_category_file)
    gold_price_band = pd.read_csv(gold_price_band_file)
    gold_bestseller = pd.read_csv(gold_bestseller_file)
    return products, gold_category, gold_price_band, gold_bestseller

products, gold_category, gold_price_band, gold_bestseller = load_data()

st.title("Amazon Product Catalog Analytics")
st.markdown("POC de catálogo analítico inteligente para descoberta e priorização de produtos.")

# filtros
st.sidebar.header("Filtros")

category_options = sorted([c for c in products["category_name"].dropna().unique()])
selected_categories = st.sidebar.multiselect("Categoria", category_options)

price_band_options = sorted([p for p in products["price_band"].dropna().unique()])
selected_price_bands = st.sidebar.multiselect("Faixa de preço", price_band_options)

best_seller_filter = st.sidebar.selectbox(
    "Best Seller",
    ["Todos", "Somente Best Seller", "Somente Não Best Seller"]
)

filtered = products.copy()

if selected_categories:
    filtered = filtered[filtered["category_name"].isin(selected_categories)]

if selected_price_bands:
    filtered = filtered[filtered["price_band"].isin(selected_price_bands)]

if best_seller_filter == "Somente Best Seller":
    filtered = filtered[filtered["is_best_seller"] == True]
elif best_seller_filter == "Somente Não Best Seller":
    filtered = filtered[filtered["is_best_seller"] == False]

# KPIs
total_products = len(filtered)
avg_price = filtered["price"].mean()
avg_stars = filtered["stars"].mean()
total_reviews = filtered["reviews"].sum()
total_bought = filtered["bought_in_last_month"].sum()
best_seller_rate = filtered["is_best_seller"].mean() * 100 if len(filtered) > 0 else 0

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("Total de produtos", f"{total_products:,}")
col2.metric("Preço médio", f"${avg_price:,.2f}" if pd.notna(avg_price) else "-")
col3.metric("Rating médio", f"{avg_stars:.2f}" if pd.notna(avg_stars) else "-")
col4.metric("Total de reviews", f"{int(total_reviews):,}")
col5.metric("Comprados no último mês", f"{int(total_bought):,}")
col6.metric("% Best Seller", f"{best_seller_rate:.2f}%")

st.divider()

# top categorias
st.subheader("Top 10 categorias por volume de produtos")
top_categories = (
    filtered.groupby("category_name", dropna=False)["asin"]
    .count()
    .reset_index(name="total_products")
    .sort_values("total_products", ascending=False)
    .head(10)
)
st.bar_chart(top_categories.set_index("category_name"))

# preço médio por categoria
st.subheader("Preço médio por categoria")
avg_price_cat = (
    filtered.groupby("category_name", dropna=False)["price"]
    .mean()
    .reset_index()
    .sort_values("price", ascending=False)
    .head(10)
)
st.bar_chart(avg_price_cat.set_index("category_name"))

# rating médio por categoria
st.subheader("Rating médio por categoria")
avg_rating_cat = (
    filtered.groupby("category_name", dropna=False)["stars"]
    .mean()
    .reset_index()
    .sort_values("stars", ascending=False)
    .head(10)
)
st.bar_chart(avg_rating_cat.set_index("category_name"))

# faixa de preço
st.subheader("Distribuição por faixa de preço")
price_band_dist = (
    filtered.groupby("price_band", dropna=False)["asin"]
    .count()
    .reset_index(name="total_products")
)
st.bar_chart(price_band_dist.set_index("price_band"))

# best seller x não best seller
st.subheader("Best Seller vs Não Best Seller")
bestseller_summary = (
    filtered.groupby("is_best_seller", dropna=False)
    .agg(
        total_products=("asin", "count"),
        avg_price=("price", "mean"),
        avg_stars=("stars", "mean"),
        avg_reviews=("reviews", "mean"),
        avg_bought_last_month=("bought_in_last_month", "mean"),
        avg_popularity_score=("popularity_score", "mean"),
    )
    .reset_index()
)
st.dataframe(bestseller_summary, use_container_width=True)

# top produtos
st.subheader("Top 20 produtos por popularity_score")
top_products = (
    filtered[[
        "asin", "title", "category_name", "price", "stars", "reviews",
        "bought_in_last_month", "popularity_score", "price_band", "is_best_seller"
    ]]
    .sort_values("popularity_score", ascending=False)
    .head(20)
)
st.dataframe(top_products, use_container_width=True)

# amostra enriquecida
st.subheader("Amostra da base enriquecida")
sample_cols = [
    "asin", "title", "category_name", "price", "list_price", "discount_pct",
    "stars", "reviews", "bought_in_last_month", "price_band",
    "title_product_type", "title_color", "title_material"
]
sample_cols = [c for c in sample_cols if c in filtered.columns]
st.dataframe(filtered[sample_cols].head(50), use_container_width=True)