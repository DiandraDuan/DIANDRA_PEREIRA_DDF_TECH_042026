import numpy as np
import pandas as pd
from src.utils import classify_price_band


def infer_product_type(title: str) -> str:
    if pd.isna(title):
        return "unknown"

    text = title.lower()

    rules = {
        "luggage": ["luggage", "suitcase", "spinner", "carry-on", "carry on", "checked"],
        "backpack": ["backpack"],
        "bag": ["bag", "handbag", "tote"],
        "shoe": ["shoe", "sneaker", "boot", "sandal"],
        "watch": ["watch"],
        "phone_accessory": ["case", "charger", "screen protector", "headphone", "earbuds"],
        "kitchen": ["pan", "pot", "knife", "cookware", "blender"],
        "beauty": ["cream", "serum", "shampoo", "conditioner", "makeup"],
    }

    for product_type, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return product_type

    return "other"


def infer_color(title: str) -> str:
    if pd.isna(title):
        return "unknown"

    colors = [
        "black", "white", "blue", "red", "green", "yellow", "pink", "purple",
        "gray", "grey", "brown", "navy", "silver", "gold", "beige", "orange"
    ]

    text = title.lower()
    found = [color for color in colors if color in text]
    return ", ".join(found) if found else "unknown"


def infer_material(title: str) -> str:
    if pd.isna(title):
        return "unknown"

    materials = ["leather", "pu", "abs", "pc", "plastic", "wood", "metal", "steel", "cotton", "polyester"]
    text = title.lower()
    found = [material for material in materials if material in text]
    return ", ".join(found) if found else "unknown"


def build_products_enriched(products: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    df = products.merge(categories, on="category_id", how="left")

    df["discount_value"] = np.where(
        df["list_price"].notna(),
        df["list_price"] - df["price"],
        np.nan
    )

    df["discount_pct"] = np.where(
        (df["list_price"].notna()) & (df["list_price"] > 0),
        (df["list_price"] - df["price"]) / df["list_price"],
        np.nan
    )

    df["price_band"] = df["price"].apply(classify_price_band)

    df["review_density"] = np.where(
        df["price"].notna() & (df["price"] > 0),
        df["reviews"] / df["price"],
        np.nan
    )

    df["popularity_score"] = (
        (df["stars"].fillna(0) * np.log1p(df["reviews"].fillna(0))) +
        (df["bought_in_last_month"].fillna(0) / 1000.0) +
        np.where(df["is_best_seller"], 2, 0)
    )

    df["title_product_type"] = df["title"].apply(infer_product_type)
    df["title_color"] = df["title"].apply(infer_color)
    df["title_material"] = df["title"].apply(infer_material)

    df["has_discount"] = df["discount_value"].fillna(0) > 0
    df["is_premium"] = df["price_band"] == "premium"
    df["high_rating_flag"] = df["stars"].fillna(0) >= 4.5
    df["high_traction_flag"] = df["bought_in_last_month"].fillna(0) >= 1000

    return df