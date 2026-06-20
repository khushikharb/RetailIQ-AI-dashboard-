# ==========================================
# RetailIQ AI - Load Warehouse CSVs to MySQL
# ==========================================

import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ==========================================
# MYSQL CONFIGURATION
# ==========================================
# Replace with your actual MySQL credentials

DB_USER = "root"
DB_PASSWORD = "kk1215@$"   # <-- Replace this
DB_HOST = "127.0.0.1"                # or "localhost"
DB_PORT = 3306
DB_NAME = "retailiq_ai"

# ==========================================
# ENCODE PASSWORD
# Needed if password contains:
# @, $, #, %, !, :, /
# ==========================================
encoded_password = quote_plus(DB_PASSWORD)

# ==========================================
# CREATE SQLALCHEMY ENGINE
# ==========================================
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================
# PATH OF WAREHOUSE CSV FILES
# ==========================================
WAREHOUSE_PATH = "data/warehouse"


def test_connection():
    """
    Tests MySQL connection before loading data.
    """
    try:
        with engine.connect() as conn:
            print("✅ MySQL connection successful!")
        return True

    except Exception as e:
        print("❌ Connection failed")
        print("Error:", e)
        return False


def load_csv_to_mysql(filename, table_name):
    """
    Reads CSV file and inserts data into MySQL table.

    Parameters:
        filename   -> CSV file name
        table_name -> MySQL table name
    """

    file_path = os.path.join(WAREHOUSE_PATH, filename)

    print(f"\nLoading file: {filename}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    # Read CSV
    df = pd.read_csv(file_path)

    print("Rows found:", len(df))

    try:
        # Insert rows into MySQL
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",   # append to existing table
            index=False
        )

        print(f"✅ Loaded into table: {table_name}")

    except Exception as e:
        print(f"❌ Failed loading table: {table_name}")
        print("Error:", e)


def main():
    """
    Loads all warehouse tables into MySQL
    in correct dependency order.
    """

    # Dimension tables first
    load_csv_to_mysql("dim_customer.csv", "dim_customer")
    load_csv_to_mysql("dim_product.csv", "dim_product")
    load_csv_to_mysql("dim_region.csv", "dim_region")
    load_csv_to_mysql("dim_date.csv", "dim_date")

    # Fact table last (because of foreign keys)
    load_csv_to_mysql("fact_sales.csv", "fact_sales")


# ==========================================
# PROGRAM START
# ==========================================
if __name__ == "__main__":

    connection_ok = test_connection()

    if connection_ok:
        main()
    else:
        print("\nFix MySQL connection first.")