import re
import numpy as np
import pandas as pd


def normalize_text(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value if value else None


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def safe_divide(numerator, denominator):
    if denominator in [0, None] or pd.isna(denominator):
        return np.nan
    return numerator / denominator


def classify_price_band(price: float) -> str:
    if pd.isna(price):
        return "unknown"
    if price < 25:
        return "low"
    if price < 100:
        return "mid"
    if price < 300:
        return "high"
    return "premium"