# Library for data analysis
import pandas as pd

# Used for folders and saving files
import os
# Path of engineered CSV dataset inside project folder
INPUT_PATH = "data/processed/processed_superstore.csv"
def load_data(filepath):
    """
    Loads processed dataset from cleaning phase.
    """

    print("Loading processed dataset...")

    df = pd.read_csv(filepath)

    print("Dataset loaded successfully.")

    return df
# convert date columns
def convert_dates(df):
    """
    Converts date columns to datetime format.
    """

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    return df

# create time features 
# helps analyse weekly sales patterns,seasonal sale 

def create_time_features(df):
    """
    Creates year, month, quarter, weekday.
    """

    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_quarter"] = df["order_date"].dt.quarter
    df["weekday"] = df["order_date"].dt.day_name()

    return df
 #delivery days
def create_delivery_features(df):
    """
    Calculates delivery duration.
    """

    df["delivery_days"] = (
        df["ship_date"] - df["order_date"]
    ).dt.days

    return df

#shipping speed category
def classify_shipping_speed(df):
    """
    Creates shipping speed category.
    """

    def speed(days):
        if days <= 2:
            return "Fast"
        elif days <= 5:
            return "Medium"
        else:
            return "Slow"

    df["shipping_speed"] = df["delivery_days"].apply(speed)

    return df
# create profit margin
def create_profit_margin(df):
    """
    Creates profit margin percentage.
    """

    df["profit_margin_pct"] = (
        df["profit"] / df["sales"]
    ) * 100

    return df
#create estimated cost= sales - profit
def estimate_cost(df):
    """
    Estimates cost using sales and profit.
    """

    df["estimated_cost"] = df["sales"] - df["profit"]

    return df
#discount bucket
def create_discount_bucket(df):
    """
    Categorizes discount levels.
    """

    def bucket(discount):
        if discount == 0:
            return "No Discount"
        elif discount <= 0.2:
            return "Low"
        elif discount <= 0.5:
            return "Medium"
        else:
            return "High"

    df["discount_bucket"] = df["discount"].apply(bucket)

    return df
#loss flag
def create_loss_flag(df):
    """
    Flags loss-making orders.
    """

    df["loss_flag"] = df["profit"].apply(
        lambda x: 1 if x < 0 else 0
    )

    return df
#feature dataset
def save_feature_data(df):
    """
    Saves final feature-engineered dataset.
    """

    output_dir = "data/final"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        "feature_engineered_superstore.csv"
    )

    df.to_csv(output_path, index=False)

    print("\nFeature engineered dataset saved.")

# Main function to run all feature engineering steps
def main():
    df = load_data(INPUT_PATH)

    df = convert_dates(df)
    df = create_time_features(df)
    df = create_delivery_features(df)
    df = classify_shipping_speed(df)
    df = create_profit_margin(df)
    df = estimate_cost(df)
    df = create_discount_bucket(df)
    df = create_loss_flag(df)

    print("\nFinal Shape:")
    print(df.shape)

    print("\nNew Columns Added:")
    print([
        "order_year",
        "order_month",
        "order_quarter",
        "weekday",
        "delivery_days",
        "shipping_speed",
        "profit_margin_pct",
        "estimated_cost",
        "discount_bucket",
        "loss_flag"
    ])

    save_feature_data(df)

if __name__ == "__main__":
    main()
