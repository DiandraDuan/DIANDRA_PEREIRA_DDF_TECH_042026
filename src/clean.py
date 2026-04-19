import numpy as np
import pandas as pd
from src.utils import normalize_text


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()

    df = df.rename(
        columns={
            "imgUrl": "img_url",
            "productURL": "product_url",
            "listPrice": "list_price",
            "isBestSeller": "is_best_seller",
            "boughtInLastMonth": "bought_in_last_month",
        }
    )

    text_cols = ["asin", "title", "img_url", "product_url"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)

    numeric_cols = [
        "stars",
        "reviews",
        "price",
        "list_price",
        "category_id",
        "bought_in_last_month",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "is_best_seller" in df.columns:
        df["is_best_seller"] = df["is_best_seller"].fillna(False).astype(bool)

    df = df.drop_duplicates(subset=["asin"]).copy()

    df = df[df["asin"].notna()].copy()
    df = df[df["title"].notna()].copy()
    df = df[df["category_id"].notna()].copy()

    df.loc[df["price"] < 0, "price"] = np.nan
    df.loc[df["list_price"] < 0, "list_price"] = np.nan
    df.loc[df["reviews"] < 0, "reviews"] = np.nan
    df.loc[df["bought_in_last_month"] < 0, "bought_in_last_month"] = np.nan

    df.loc[(df["stars"] < 0) | (df["stars"] > 5), "stars"] = np.nan

    df.loc[df["list_price"] == 0, "list_price"] = np.nan
    df.loc[df["list_price"] < df["price"], "list_price"] = np.nan

    df["reviews"] = df["reviews"].fillna(0)
    df["bought_in_last_month"] = df["bought_in_last_month"].fillna(0)

    return df


def clean_categories(categories: pd.DataFrame) -> pd.DataFrame:
    df = categories.copy()

    df = df.rename(columns={"id": "category_id"})
    df["category_id"] = pd.to_numeric(df["category_id"], errors="coerce")

    if "category_name" in df.columns:
        df["category_name"] = df["category_name"].apply(normalize_text)

    df = df.drop_duplicates(subset=["category_id"]).copy()
    df = df[df["category_id"].notna()].copy()

    return df