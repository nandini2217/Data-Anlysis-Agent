import pandas as pd

def route_question(question: str):
    q = question.lower()

    if any(k in q for k in ["average", "mean", "sum", "max", "min", "count"]):
        return "aggregation"

    if any(k in q for k in ["category", "categories", "unique", "distinct"]):
        return "categories"

    if any(k in q for k in ["plot", "chart", "graph"]):
        return "visual"

    if any(k in q for k in ["what is this file", "describe", "summary", "about"]):
        return "summary"

    return "document"


def answer_question(question, df: pd.DataFrame, document_text: str):
    intent = route_question(question)

    # ---------------- CATEGORY ----------------
    if intent == "categories":
        for col in df.columns:
            if col.lower() in question.lower():
                return df[col].dropna().unique().tolist()

        return "No categorical column found in your question."

    # ---------------- AGGREGATION ----------------
    if intent == "aggregation":
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in question.lower():
                if "average" in question or "mean" in question:
                    return round(df[col].mean(), 2)
                if "max" in question:
                    return df[col].max()
                if "min" in question:
                    return df[col].min()
                if "sum" in question:
                    return df[col].sum()
                if "count" in question:
                    return df[col].count()

        return "Numeric column not found for aggregation."

    # ---------------- SUMMARY ----------------
    if intent == "summary":
        return f"""
This dataset contains **{len(df)} records** and **{len(df.columns)} columns**.

Columns:
{', '.join(df.columns)}

Document Context:
{document_text[:600]}...
"""

    # ---------------- DOCUMENT Q&A ----------------
    if intent == "document":
        if document_text.strip():
            return f"Based on uploaded document:\n\n{document_text[:700]}..."
        else:
            return "No document uploaded to answer this question."

    return "I couldn't understand the question."
