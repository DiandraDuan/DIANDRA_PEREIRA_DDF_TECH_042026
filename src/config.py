from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"

OUTPUTS_DIR = BASE_DIR / "outputs"
QUALITY_DIR = OUTPUTS_DIR / "quality_reports"
LOGS_DIR = OUTPUTS_DIR / "logs"

PRODUCTS_FILE = RAW_DIR / "amazon_products.csv"
CATEGORIES_FILE = RAW_DIR / "amazon_categories.csv"

for folder in [BRONZE_DIR, SILVER_DIR, GOLD_DIR, QUALITY_DIR, LOGS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)