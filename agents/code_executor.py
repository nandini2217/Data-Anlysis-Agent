def execute_pandas(df, operation):
    try:
        return eval(operation)
    except Exception as e:
        return f"❌ Error: {e}"
