def generate_summary(df):
    summary = []
    summary.append(f"The dataset contains {len(df)} records.")

    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) > 0:
        col = num_cols[0]
        summary.append(
            f"The average {col} is {round(df[col].mean(), 2)}, "
            f"with a maximum of {round(df[col].max(), 2)}."
        )

    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(cat_cols) > 0:
        top = df[cat_cols[0]].value_counts().idxmax()
        summary.append(f"The most frequent category is '{top}'.")

    return " ".join(summary)
