import pandas as pd
from src.config import QUALITY_DIR


def generate_quality_report(products: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    checks = []

    checks.append({
        "check_name": "products_asin_not_null",
        "result": products["asin"].notna().all(),
        "details": f"nulos: {products['asin'].isna().sum()}",
    })

    checks.append({
        "check_name": "products_asin_unique",
        "result": products["asin"].is_unique,
        "details": f"duplicados: {products['asin'].duplicated().sum()}",
    })

    checks.append({
        "check_name": "products_title_not_null",
        "result": products["title"].notna().all(),
        "details": f"nulos: {products['title'].isna().sum()}",
    })

    checks.append({
        "check_name": "products_price_non_negative",
        "result": (products["price"].dropna() >= 0).all(),
        "details": f"valores inválidos: {(products['price'].dropna() < 0).sum()}",
    })

    stars_valid = products["stars"].dropna().between(0, 5)
    checks.append({
        "check_name": "products_stars_between_0_5",
        "result": stars_valid.all(),
        "details": f"fora da faixa: {(~stars_valid).sum()}",
    })

    checks.append({
        "check_name": "products_reviews_non_negative",
        "result": (products["reviews"].dropna() >= 0).all(),
        "details": f"valores inválidos: {(products['reviews'].dropna() < 0).sum()}",
    })

    checks.append({
        "check_name": "category_fk_valid",
        "result": products["category_id"].isin(categories["category_id"]).all(),
        "details": f"fora da dimensão: {(~products['category_id'].isin(categories['category_id'])).sum()}",
    })

    report = pd.DataFrame(checks)
    report.to_csv(QUALITY_DIR / "quality_report.csv", index=False)
    report.to_excel(QUALITY_DIR / "quality_report.xlsx", index=False)

    return report