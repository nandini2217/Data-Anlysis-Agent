import pandas as pd

def clean_data(df: pd.DataFrame):
    df = df.copy()

    for col in df.columns:
        # If column is numeric → fill missing with median
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())

        # If column is text/categorical → fill missing with 'Unknown'
        else:
            df[col] = df[col].fillna("Unknown")

    return df

