# Data analysis library
import pandas as pd

# Folder operations
import os
# Path of schema CSV dataset inside project folder
INPUT_PATH = "data/final/feature_engineered_superstore.csv"
#load data
def load_data(filepath):
    """
    Loads final feature-engineered dataset.
    """

    print("Loading final dataset...")

    df = pd.read_csv(filepath)

    print("Dataset loaded successfully.")
    print("Shape:", df.shape)

    return df
# create output directory
OUTPUT_DIR = "data/warehouse"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# create  dimension tables build dim_customer
def build_dim_customer(df):
    """
    Creates customer dimension table.
    """

    dim_customer = df[
        ["customer_id", "customer_name", "segment"]
    ].drop_duplicates().reset_index(drop=True)

    # Generate surrogate keys
    dim_customer.insert(
        0,
        "customer_key",
        range(1, len(dim_customer) + 1)
    )

    output_path = f"{OUTPUT_DIR}/dim_customer.csv"
    dim_customer.to_csv(output_path, index=False)

    print("dim_customer created:", dim_customer.shape)

    print("\nChecking duplicate keys...")
    print(
    dim_customer.duplicated(
        subset=["customer_id"]
    ).sum()
)
    return dim_customer


    #create dimension tables build dim_product
def build_dim_product(df):
    """
    Creates Product Dimension Table.

    Purpose:
    - Extract unique products from transaction dataset
    - Clean hidden text issues (spaces, formatting)
    - Generate surrogate key (product_key)
    - Save dimension table as CSV

    Why needed?
    In star schema, product information should be stored once
    in dimension table instead of repeating in every sales row.
    """

    print("\nBuilding Product Dimension...")

    # ---------------------------------------------------
    # Step 1: Select only product-related columns
    # ---------------------------------------------------
    product_df = df[
        [
            "product_id",
            "product_name",
            "category",
            "sub_category"
        ]
    ].copy()

    # ---------------------------------------------------
    # Step 2: Clean text columns
    #
    # Problems this solves:
    # - trailing spaces
    # - leading spaces
    # - double spaces
    # - datatype inconsistency
    # ---------------------------------------------------
    text_cols = [
        "product_id",
        "product_name",
        "category",
        "sub_category"
    ]

    for col in text_cols:
        product_df[col] = (
            product_df[col]
            .astype(str)                     # Ensure string type
            .str.strip()                    # Remove leading/trailing spaces
            .str.replace(r"\s+", " ", regex=True)  # Replace multiple spaces with single space
        )

    # ---------------------------------------------------
    # Step 3: Debug duplicate product IDs BEFORE removal
    # ---------------------------------------------------
    duplicate_products = product_df[
        product_df.duplicated(
            subset=["product_id"],
            keep=False
        )
    ]

    print("\nDuplicate Product Records BEFORE Cleaning:")
    print(duplicate_products.shape)

    if len(duplicate_products) > 0:
        print(
            duplicate_products
            .sort_values("product_id")
            .head(20)
        )

    # ---------------------------------------------------
    # Step 4: Remove duplicate product IDs
    #
    # Keep first occurrence for each product_id
    # ---------------------------------------------------
    dim_product = (
        product_df
        .drop_duplicates(subset=["product_id"], keep="first")
        .reset_index(drop=True)
    )

    # ---------------------------------------------------
    # Step 5: Create surrogate key
    #
    # product_key becomes warehouse primary key
    # ---------------------------------------------------
    dim_product.insert(
        0,
        "product_key",
        range(1, len(dim_product) + 1)
    )

    # ---------------------------------------------------
    # Step 6: Verify duplicates removed
    # ---------------------------------------------------
    duplicate_count = dim_product.duplicated(
        subset=["product_id"]
    ).sum()

    print("\nProduct duplicate keys AFTER cleaning:", duplicate_count)

    # ---------------------------------------------------
    # Step 7: Save CSV
    # ---------------------------------------------------
    output_path = f"{OUTPUT_DIR}/dim_product.csv"
    dim_product.to_csv(output_path, index=False)

    print("dim_product created:", dim_product.shape)

    return dim_product
    

#create dimension tables build dim_region
def build_dim_region(df):
    """
    Creates region dimension table.
    Stores unique geographic combinations.
    """

    dim_region = df[
        [
            "country_region",
            "city",
            "state_province",
            "postal_code",
            "region"
        ]
    ].drop_duplicates().reset_index(drop=True)

    # Create surrogate key
    dim_region.insert(
        0,
        "region_key",
        range(1, len(dim_region) + 1)
    )

    output_path = f"{OUTPUT_DIR}/dim_region.csv"
    dim_region.to_csv(output_path, index=False)

    print("dim_region created:", dim_region.shape)
    print(
    "Region duplicate keys:",
    dim_region.duplicated(
        subset=[
            "country_region",
            "city",
            "state_province",
            "postal_code",
            "region"
        ]
    ).sum()
)

    return dim_region
#create dimension tables build dim_date
def build_dim_date(df):
    """
    Creates date dimension table.
    Stores unique dates and time hierarchy.
    """

    dim_date = df[
        [
            "order_date",
            "order_year",
            "order_month",
            "order_quarter",
            "weekday"
        ]
    ].drop_duplicates().reset_index(drop=True)

    # Create surrogate key
    dim_date.insert(
        0,
        "date_key",
        range(1, len(dim_date) + 1)
    )

    output_path = f"{OUTPUT_DIR}/dim_date.csv"
    dim_date.to_csv(output_path, index=False)

    print("dim_date created:", dim_date.shape)
    print(
    "Date duplicate keys:",
    dim_date.duplicated(
        subset=["order_date"]
    ).sum()
)
    return dim_date
#create fact table build fact_sales
def build_fact_sales(
    df,
    dim_customer,
    dim_product,
    dim_region,
    dim_date
):
    """
    Creates fact_sales table by mapping surrogate keys.
    """
    print("\n--- FACT TABLE DEBUG ---")
    print("Initial rows:", len(df))
#merge with dim_customer to get customer_key 
    fact = df.merge(
    dim_customer[
        ["customer_key", "customer_id"]
    ],
    on="customer_id",
    how="left"
)

    print("After customer merge:", len(fact))

#merge with dim_product to get product_key
    fact = fact.merge(
        dim_product[
            ["product_key", "product_id"]
        ],
        on="product_id",
        how="left"
    )
    print("After product merge:", len(fact))
#merge with dim_region to get region_key
    fact = fact.merge(
        dim_region[
            [
                "region_key",
                "country_region",
                "city",
                "state_province",
                "postal_code",
                "region"
            ]
        ],
        on=[
            "country_region",
            "city",
            "state_province",
            "postal_code",
            "region"
        ],
        how="left"
    )
    print("After region merge:", len(fact))
#merge with dim_date to get date_key
    fact = fact.merge(
        dim_date[
            ["date_key", "order_date"]
        ],
        on="order_date",
        how="left"
    )
    print("After date merge:", len(fact))
#select relevant columns for fact table
    fact_sales = fact[
        [
            "customer_key",
            "product_key",
            "region_key",
            "date_key",
            "order_id",
            "ship_date",
            "ship_mode",
            "sales",
            "quantity",
            "discount",
            "profit",
            "delivery_days",
            "shipping_speed",
            "profit_margin_pct",
            "estimated_cost",
            "discount_bucket",
            "loss_flag"
        ]
    ].copy()

#add sales_key as surrogate key for fact table
    fact_sales.insert(
        0,
        "sales_key",
        range(1, len(fact_sales) + 1)
    )
#save fact_sales to CSV
    output_path = f"{OUTPUT_DIR}/fact_sales.csv"
    fact_sales.to_csv(output_path, index=False)

    print("fact_sales created:", fact_sales.shape)

    return fact_sales

# Main function to run all schema building steps
def main():
    df = load_data(INPUT_PATH)

    dim_customer = build_dim_customer(df)
    dim_product = build_dim_product(df)
    dim_region = build_dim_region(df)
    dim_date = build_dim_date(df)

    fact_sales = build_fact_sales(
        df,
        dim_customer,
        dim_product,
        dim_region,
        dim_date
    )
if __name__ == "__main__":
    main()
