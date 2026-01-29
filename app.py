import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from agents.data_profiler import profile_data
from agents.chat_agent import answer_question
from utils.document_reader import extract_text

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Data Agent", layout="wide")
st.title("🤖 AI Data Analysis Agent")

# ---------------- FILE UPLOAD ----------------
csv_file = st.file_uploader("📂 Upload CSV File", type=["csv"])
doc_files = st.file_uploader(
    "📄 Upload Supporting Documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

df = None
document_text = ""

if csv_file:
    df = pd.read_csv(csv_file)
    st.success("✅ CSV uploaded successfully")

if doc_files:
    document_text = extract_text(doc_files)
    st.success("✅ Documents processed")

# ==================================================
# ================= DASHBOARD ======================
# ==================================================
if df is not None:
    st.markdown("---")
    st.subheader("📊 Dashboard Controls")

    col1, col2, col3 = st.columns(3)

    with col1:
        dashboard_title = st.text_input("Dashboard Title", "Auto Data Dashboard")

    with col2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Line", "Pie", "Histogram"]
        )

    with col3:
        theme = st.selectbox(
            "Theme",
            ["default", "dark_background", "ggplot", "seaborn"]
        )

    color = st.color_picker("Pick Chart Color", "#4CAF50")

    selected_cols = st.multiselect(
        "Select Columns for Charts",
        df.columns.tolist()
    )

    summary = st.text_area(
        "Dashboard Summary",
        "This dashboard provides insights generated automatically from the uploaded dataset."
    )

    generate_dashboard = st.button("🚀 Generate Dashboard")

    if generate_dashboard and selected_cols:
        plt.style.use(theme)

        st.markdown("---")
        st.subheader(f"📌 {dashboard_title}")
        st.info(summary)

        # ---------- KPIs ----------
        k1, k2, k3 = st.columns(3)
        k1.metric("Rows", df.shape[0])
        k2.metric("Columns", df.shape[1])
        k3.metric("Missing %", round(df.isna().mean().mean() * 100, 2))

        # ---------- CHART AREA ----------
        st.markdown("### 📈 Visualizations")

        chart_cols = st.columns(2)

        for i, col in enumerate(selected_cols):
            with chart_cols[i % 2]:
                fig, ax = plt.subplots()

                if chart_type == "Histogram" and pd.api.types.is_numeric_dtype(df[col]):
                    df[col].dropna().hist(ax=ax)
                    ax.set_title(col)

                elif chart_type == "Bar":
                    df[col].value_counts().head(10).plot(
                        kind="bar", ax=ax
                    )
                    ax.set_title(col)

                elif chart_type == "Pie":
                    df[col].value_counts().head(5).plot(
                        kind="pie", ax=ax, autopct="%1.1f%%"
                    )
                    ax.set_ylabel("")
                    ax.set_title(col)

                elif chart_type == "Line" and pd.api.types.is_numeric_dtype(df[col]):
                    df[col].plot(ax=ax)
                    ax.set_title(col)

                ax.set_facecolor("white")
                st.pyplot(fig)

        # ---------- DOWNLOAD ----------
        st.markdown("---")
        st.download_button(
            "⬇ Download Dashboard Data",
            df.to_csv(index=False),
            "dashboard_data.csv",
            "text/csv"
        )

# ==================================================
# ================= DATA PROFILE ===================
# ==================================================
if df is not None:
    st.markdown("---")
    st.subheader("🧠 Data Understanding")
    profile = profile_data(df)
    st.json(profile)

# ==================================================
# ================= CHAT AGENT =====================
# ==================================================
st.markdown("---")
st.subheader("💬 Ask Your Data")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input(
    "Ask anything about your CSV or documents",
    placeholder="e.g. What are the different income groups?"
)

if st.button("Ask Question") and query:
    answer = answer_question(query, df, document_text)
    st.session_state.chat_history.append((query, answer))

for q, a in st.session_state.chat_history:
    st.markdown(f"**🧑 You:** {q}")

    if isinstance(a, list):
        st.dataframe(pd.DataFrame(a, columns=["Result"]))
    elif isinstance(a, (int, float, str)):
        st.success(a)
    else:
        st.dataframe(a)
