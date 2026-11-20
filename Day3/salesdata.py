from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "messy_sales_data.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_sales_data.csv"


def clean_sales_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE)

    print(df.head())
    print(df.shape)
    df.info()
    print(df.describe())

    print(df.isna().sum())
    print(df.duplicated().sum())

    df = df.drop_duplicates()
    df = df.dropna(subset=["customer_name", "order_date"])

    df["quantity"] = df["quantity"].fillna(df["quantity"].median())
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].mean())
    df["rating"] = df["rating"].fillna(df["rating"].mean())
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["city"] = df["city"].fillna("Unknown")
    df["email"] = df["email"].fillna("not_provided")

    print(df.isna().sum())

    df["order_date"] = pd.to_datetime(
        df["order_date"], format="mixed", dayfirst=True
    )
    df["city"] = df["city"].str.strip().str.title()

    df.to_csv(OUTPUT_FILE, index=False)
    return df


if __name__ == "__main__":
    clean_sales_data()
