import plotly.express as px
import pandas as pd

COLOR_MAP = {
    "Blue": px.colors.sequential.Blues,
    "Green": px.colors.sequential.Greens,
    "Orange": px.colors.sequential.Oranges,
    "Purple": px.colors.sequential.Purples,
    "Dark": px.colors.sequential.Greys
}

def generate_chart(df, chart_config, theme, color_theme):
    chart_type = chart_config["type"]
    x = chart_config["x"]
    y = chart_config.get("y")

    colors = COLOR_MAP.get(color_theme)

    if chart_type == "Bar":
        return px.bar(df, x=x, y=y, theme=theme, color_discrete_sequence=colors)

    if chart_type == "Line":
        return px.line(df, x=x, y=y, theme=theme)

    if chart_type == "Histogram":
        return px.histogram(df, x=x, theme=theme, color_discrete_sequence=colors)

    if chart_type == "Pie":
        return px.pie(df, names=x, theme=theme)

    if chart_type == "Donut":
        return px.pie(df, names=x, hole=0.5, theme=theme)

    return None


def generate_kpis(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing %": round(df.isna().mean().mean() * 100, 2)
    }


def generate_summary(df):
    return f"""
This dashboard analyzes a dataset with **{df.shape[0]} records**
and **{df.shape[1]} fields**.

You can customize charts, colors, and layouts dynamically
to explore insights interactively.
"""