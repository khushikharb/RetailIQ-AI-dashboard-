# pandas is used for data analysis and table manipulation

import pandas as pd

# os helps work with file paths and folders
import os

# Path of raw Excel dataset inside project folder
RAW_FILE_PATH = "data/raw/Sample - Superstore.xls"

#Create Load Function
def load_data(filepath):
    """
    Reads Excel file and returns pandas DataFrame.

    Input:
        filepath -> location of Excel file

    Output:
        df -> loaded dataset
    """

    print("Loading raw dataset...")

    df = pd.read_excel(filepath)

    print("Dataset loaded successfully.")

    return df

#Create inspection Function
def inspect_data(df):
    """
    Displays important information about dataset.
    Helps us understand raw data before cleaning.
    """

    print("\n--- DATASET SHAPE ---")
    print(df.shape)

    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())
 
#Standardize Column Names
def standardize_columns(df):
    """
    Cleans column names by:
    - converting to lowercase
    - replacing spaces with underscores
    - removing special characters
    """

    print("\nStandardizing column names...")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
        .str.replace("-", "_")
    )

    print("Column standardization complete.")

    return df
#save cleaned file
def save_cleaned_file(df):
    """
    Saves cleaned dataset as CSV.
    """

    output_path = "data/cleaned/cleaned_superstore.csv"

    # Save DataFrame to CSV
    df.to_csv(output_path, index=False)

    print(f"\nCleaned dataset saved at: {output_path}")
#Main Function
def main():
    """
    Main ETL orchestration function.
    Runs entire ingestion pipeline.
    """

    # Step 1: Load raw dataset
    df = load_data(RAW_FILE_PATH)

    # Step 2: Inspect raw data
    inspect_data(df)

    # Step 3: Standardize columns
    df = standardize_columns(df)

    print("\nUpdated Columns:")
    print(df.columns.tolist())

    # Step 4: Save cleaned raw data
    save_cleaned_file(df)

if __name__ == "__main__":
    main()