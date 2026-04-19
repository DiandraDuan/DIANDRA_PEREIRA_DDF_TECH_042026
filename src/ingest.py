import pandas as pd
from src.config import PRODUCTS_FILE, CATEGORIES_FILE, BRONZE_DIR
from src.utils import clean_column_names


def load_raw_data():
    products = pd.read_csv(PRODUCTS_FILE)
    categories = pd.read_csv(CATEGORIES_FILE)

    products = clean_column_names(products)
    categories = clean_column_names(categories)

    return products, categories


def save_bronze(products: pd.DataFrame, categories: pd.DataFrame):
    products.to_csv(BRONZE_DIR / "products_raw.csv", index=False)
    categories.to_csv(BRONZE_DIR / "categories_raw.csv", index=False)