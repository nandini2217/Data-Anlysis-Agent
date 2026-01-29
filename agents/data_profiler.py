import pandas as pd

def profile_data(df: pd.DataFrame):
    profile = {}

    for col in df.columns:
        profile[col] = {
            "data_type": str(df[col].dtype),
            "missing_percentage": round(df[col].isnull().mean() * 100, 2),
            "unique_values": int(df[col].nunique())
        }

    return profile
