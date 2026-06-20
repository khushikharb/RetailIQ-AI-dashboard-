# Library for data analysis
import pandas as pd

# Used for file/folder operations
import os
# Path of cleaned CSV dataset inside project folder
INPUT_PATH = "data/cleaned/cleaned_superstore.csv"
def load_data(filepath):
    """
    Loads cleaned CSV file from ingestion phase.
    """

    print("Loading cleaned dataset...")

    df = pd.read_csv(filepath)

    print("Dataset loaded successfully.")

    return df
#check duplicates
def check_duplicates(df):
    """
    Checks duplicate rows in dataset.
    """

    duplicate_count = df.duplicated().sum()

    print("\nDuplicate Rows Found:", duplicate_count)

    return duplicate_count

#remove duplicates
def remove_duplicates(df):
    """
    Removes duplicate rows.
    """

    before_rows = len(df)

    df = df.drop_duplicates()

    after_rows = len(df)

    removed = before_rows - after_rows

    print("Duplicates Removed:", removed)

    return df
# validate sales
def validate_sales(df):
    """
    Finds invalid sales records.
    """

    invalid_sales = df[df["sales"] <= 0]

    print("\nInvalid Sales Records:", len(invalid_sales))
# validate quantity
def validate_quantity(df):
    """
    Checks invalid quantity.
    """

    invalid_qty = df[df["quantity"] <= 0]

    print("Invalid Quantity Records:", len(invalid_qty))
# validate discount
def validate_discount(df):
    """
    Checks invalid discount values.
    """

    invalid_discount = df[
        (df["discount"] < 0) |
        (df["discount"] > 1)
    ]

    print("Invalid Discount Records:", len(invalid_discount))

#validate shipping dates
def validate_shipping_dates(df):
    """
    Validates shipping dates.
    """

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    invalid_shipping = df[
        df["ship_date"] < df["order_date"]
    ]

    print("Invalid Shipping Records:", len(invalid_shipping))

#negative profit analysis
def analyze_negative_profit(df):
    """
    Counts loss-making transactions.
    """

    loss_orders = df[df["profit"] < 0]

    print("Loss-Making Orders:", len(loss_orders))

#detect sales outliers using IQR
def detect_sales_outliers(df):
    """
    Detects sales outliers using IQR.
    """

    Q1 = df["sales"].quantile(0.25)
    Q3 = df["sales"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df["sales"] < lower) |
        (df["sales"] > upper)
    ]

    print("Sales Outliers:", len(outliers))

#final cleaned dataset
def save_clean_data(df):
    """
    Saves final cleaned dataset.
    """

    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        "processed_superstore.csv"
    )

    df.to_csv(output_path, index=False)

    print("\nProcessed dataset saved successfully.")

# Main function to run all cleaning steps
def main():
    df = load_data(INPUT_PATH)

    check_duplicates(df)
    df = remove_duplicates(df)

    validate_sales(df)
    validate_quantity(df)
    validate_discount(df)
    validate_shipping_dates(df)

    analyze_negative_profit(df)
    detect_sales_outliers(df)

    save_clean_data(df)
if __name__ == "__main__":
    main()