from src.config import SILVER_DIR, GOLD_DIR
from src.ingest import load_raw_data, save_bronze
from src.clean import clean_products, clean_categories
from src.enrich import build_products_enriched
from src.quality import generate_quality_report


def run_pipeline():
    print("1. Lendo dados raw...")
    products_raw, categories_raw = load_raw_data()

    print("2. Salvando bronze...")
    save_bronze(products_raw, categories_raw)

    print("3. Limpando dados...")
    products_clean = clean_products(products_raw)
    categories_clean = clean_categories(categories_raw)

    print("4. Gerando relatório de qualidade...")
    quality_report = generate_quality_report(products_clean, categories_clean)

    print("5. Enriquecendo dados...")
    products_enriched = build_products_enriched(products_clean, categories_clean)

    print("6. Criando camada silver...")
    products_clean.to_csv(SILVER_DIR / "products_clean.csv", index=False)
    categories_clean.to_csv(SILVER_DIR / "categories_clean.csv", index=False)
    products_enriched.to_csv(SILVER_DIR / "products_enriched.csv", index=False)

    print("7. Criando camada gold...")
    gold_category = (
        products_enriched
        .groupby("category_name", dropna=False)
        .agg(
            total_products=("asin", "count"),
            avg_price=("price", "mean"),
            avg_stars=("stars", "mean"),
            total_reviews=("reviews", "sum"),
            total_bought_last_month=("bought_in_last_month", "sum"),
            avg_popularity_score=("popularity_score", "mean"),
            best_seller_count=("is_best_seller", "sum"),
        )
        .reset_index()
        .sort_values("total_products", ascending=False)
    )

    gold_price_band = (
        products_enriched
        .groupby("price_band", dropna=False)
        .agg(
            total_products=("asin", "count"),
            avg_price=("price", "mean"),
            avg_stars=("stars", "mean"),
            total_reviews=("reviews", "sum"),
            total_bought_last_month=("bought_in_last_month", "sum"),
        )
        .reset_index()
    )

    gold_bestseller = (
        products_enriched
        .groupby("is_best_seller", dropna=False)
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

    gold_category.to_csv(GOLD_DIR / "gold_category_analytics.csv", index=False)
    gold_price_band.to_csv(GOLD_DIR / "gold_price_band_analytics.csv", index=False)
    gold_bestseller.to_csv(GOLD_DIR / "gold_bestseller_analytics.csv", index=False)

    print("Pipeline finalizado com sucesso.")
    print("\nResumo:")
    print(f"Products raw: {products_raw.shape}")
    print(f"Products clean: {products_clean.shape}")
    print(f"Products enriched: {products_enriched.shape}")
    print(f"Gold category: {gold_category.shape}")
    print(f"Gold price band: {gold_price_band.shape}")
    print(f"Gold bestseller: {gold_bestseller.shape}")

    return {
        "products_raw": products_raw,
        "categories_raw": categories_raw,
        "products_clean": products_clean,
        "categories_clean": categories_clean,
        "products_enriched": products_enriched,
        "gold_category": gold_category,
        "gold_price_band": gold_price_band,
        "gold_bestseller": gold_bestseller,
        "quality_report": quality_report,
    }