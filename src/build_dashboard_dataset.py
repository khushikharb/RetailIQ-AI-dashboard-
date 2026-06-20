import pandas as pd
import os

# ===============================
# File Paths
# ===============================
FACT_PATH = "data/warehouse/fact_sales.csv"
CUSTOMER_PATH = "data/warehouse/dim_customer.csv"
PRODUCT_PATH = "data/warehouse/dim_product.csv"
REGION_PATH = "data/warehouse/dim_region.csv"
DATE_PATH = "data/warehouse/dim_date.csv"

OUTPUT_DIR = "data/dashboard"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===============================
# Load all tables
# ===============================
def load_tables():
    print("Loading warehouse tables...")

    fact = pd.read_csv(FACT_PATH)
    customer = pd.read_csv(CUSTOMER_PATH)
    product = pd.read_csv(PRODUCT_PATH)
    region = pd.read_csv(REGION_PATH)
    date = pd.read_csv(DATE_PATH)

    print("All tables loaded.")

    return fact, customer, product, region, date


# ===============================
# Build Semantic Layer
# ===============================
def build_dashboard_dataset():

    fact, customer, product, region, date = load_tables()

    print("\nInitial fact rows:", len(fact))

    # Merge Customer
    dashboard_df = fact.merge(
        customer,
        on="customer_key",
        how="left"
    )

    print("After customer merge:", len(dashboard_df))

    # Merge Product
    dashboard_df = dashboard_df.merge(
        product,
        on="product_key",
        how="left"
    )

    print("After product merge:", len(dashboard_df))

    # Merge Region
    dashboard_df = dashboard_df.merge(
        region,
        on="region_key",
        how="left"
    )

    print("After region merge:", len(dashboard_df))

    # Merge Date
    dashboard_df = dashboard_df.merge(
        date,
        on="date_key",
        how="left"
    )

    print("After date merge:", len(dashboard_df))

    return dashboard_df


# ===============================
# Save Dataset
# ===============================
def save_dataset(df):

    output_path = f"{OUTPUT_DIR}/dashboard_dataset.csv"

    df.to_csv(output_path, index=False)

    print("\nDashboard dataset saved:")
    print(output_path)
    print("Shape:", df.shape)


# ===============================
# Main
# ===============================
def main():

    dashboard_df = build_dashboard_dataset()

    save_dataset(dashboard_df)


if __name__ == "__main__":
    main()