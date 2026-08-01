import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re
from io import StringIO, BytesIO
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ── API key ───────────────────────────────────────────────────────────────────
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

# Update this constant if you need to swap models.
MODEL = "gemini-2.5-flash"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Echo — Data Intelligence Assistant",
    page_icon="🔊",
    layout="wide",
)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "messages": [],        # list of {"role": "user"|"assistant", "content": str, "figure": fig|None}
    "summary": None,       # executive summary text
    "df": None,            # current dataframe
    "data_context": None,  # rich string profile of the dataframe
    "file_name": None,     # name of the uploaded file
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_client():
    """Return a Gemini client, stopping the app with a friendly message if no key is set."""
    if not api_key:
        st.error(
            "⚠️ **No API key found.** Add `GEMINI_API_KEY` to your `.env` file or Streamlit secrets."
        )
        st.stop()
    return genai.Client(api_key=api_key)


def build_data_context(df: pd.DataFrame) -> str:
    """Build a rich data context string to give the LLM full situational awareness."""
    buf = StringIO()
    buf.write(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n\n")

    buf.write("Column names and dtypes:\n")
    buf.write(df.dtypes.to_string())
    buf.write("\n\n")

    buf.write("Descriptive statistics (all columns):\n")
    buf.write(df.describe(include="all").to_string())
    buf.write("\n\n")

    buf.write("Missing values per column:\n")
    null_counts = df.isnull().sum()
    buf.write(null_counts[null_counts > 0].to_string() if null_counts.any() else "None")
    buf.write("\n\n")

    # Value counts for low-cardinality categoricals (helpful for the LLM)
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols[:5]:
        if df[col].nunique() <= 30:
            buf.write(f"Value counts — '{col}':\n")
            buf.write(df[col].value_counts().head(10).to_string())
            buf.write("\n\n")

    buf.write("First 50 rows (sample):\n")
    buf.write(df.head(50).to_string(index=False))
    return buf.getvalue()


def build_api_history(messages: list) -> list:
    """Convert session messages into the Gemini multi-turn history format."""
    history = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": m["content"]}]})
    return history


CHART_RE = re.compile(
    r"\b(chart|plot|graph|visuali[sz]e?|histogram|bar chart|bar graph|line chart|"
    r"scatter|pie chart|heatmap|trend|distribution|show me|draw|display)\b",
    re.IGNORECASE,
)

def is_chart_request(text: str) -> bool:
    return bool(CHART_RE.search(text))


def extract_python_code(text: str) -> str | None:
    """Pull the first ```python ... ``` block out of an LLM response."""
    match = re.search(r"```python\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def render_chart_from_code(code: str, df: pd.DataFrame):
    """Execute LLM-generated Plotly code and return the figure, or None on failure."""
    local_ns: dict = {"px": px, "go": go, "df": df, "pd": pd}
    try:
        exec(code, local_ns)  # noqa: S102
        return local_ns.get("fig")
    except Exception as e:
        st.warning(f"⚠️ Chart rendering failed: {e}")
        return None


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔊 Echo")
    st.caption("Data Intelligence Assistant")
    st.divider()
    st.markdown(f"**Model:** `{MODEL}`")
    st.markdown("**Supported files:** CSV, XLSX")
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🔄 Upload New File", use_container_width=True):
        for key in ["messages", "summary", "df", "data_context", "file_name"]:
            st.session_state[key] = defaults[key]
        st.rerun()
    st.divider()
    st.caption(
        "Echo remembers your entire conversation. Ask follow-up questions freely. "
        "Request charts by saying *'show me a chart of…'* or *'plot the distribution of…'*."
    )


# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🔊 Echo — Data Intelligence Assistant")
st.caption("Listen to what your data is telling you.")


# ── File upload ────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file to begin",
    type=["csv", "xlsx"],
    help="Supports .csv and .xlsx files up to Streamlit's default limit.",
)

if uploaded_file:
    # Only re-parse when a new file arrives
    if uploaded_file.name != st.session_state.file_name:
        try:
            with st.spinner("Reading file…"):
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.session_state.data_context = build_data_context(df)
            st.session_state.file_name = uploaded_file.name
            # Clear previous session when switching files
            st.session_state.messages = []
            st.session_state.summary = None
            st.success(f"✅ Loaded **{uploaded_file.name}** — {df.shape[0]:,} rows × {df.shape[1]} columns")
        except Exception as e:
            st.error(f"Failed to read file: {e}")
            st.stop()

    df: pd.DataFrame = st.session_state.df

    # ── Dataset preview ────────────────────────────────────────────────────────
    with st.expander("📋 Dataset Preview", expanded=True):
        st.dataframe(df.head(20), use_container_width=True)

    # ── Profile metrics ────────────────────────────────────────────────────────
    st.subheader("📊 Data Profile")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))
    c4.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))

    # ── Auto-EDA charts ────────────────────────────────────────────────────────
    with st.expander("📈 Automatic EDA Charts", expanded=False):
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        if numeric_cols:
            st.markdown("**Numeric Distributions**")
            chunk_size = 3
            for chunk in [numeric_cols[i:i+chunk_size] for i in range(0, len(numeric_cols), chunk_size)]:
                grid = st.columns(len(chunk))
                for col_widget, col_name in zip(grid, chunk):
                    fig = px.histogram(
                        df, x=col_name, nbins=30, title=col_name,
                        color_discrete_sequence=["#6366f1"],
                    )
                    fig.update_layout(
                        margin=dict(l=10, r=10, t=35, b=10),
                        height=230,
                        showlegend=False,
                        title_font_size=13,
                    )
                    col_widget.plotly_chart(fig, use_container_width=True)

            if len(numeric_cols) > 1:
                st.markdown("**Correlation Heatmap**")
                corr = df[numeric_cols].corr()
                fig_corr = px.imshow(
                    corr,
                    text_auto=".2f",
                    color_continuous_scale="RdBu_r",
                    title="Pearson Correlation",
                    aspect="auto",
                )
                fig_corr.update_layout(height=400)
                st.plotly_chart(fig_corr, use_container_width=True)

        if cat_cols:
            st.markdown("**Categorical Value Counts (top 10)**")
            chunk_size = 2
            for chunk in [cat_cols[i:i+chunk_size] for i in range(0, len(cat_cols), chunk_size)]:
                grid = st.columns(len(chunk))
                for col_widget, col_name in zip(grid, chunk):
                    top = df[col_name].value_counts().head(10).reset_index()
                    top.columns = [col_name, "count"]
                    fig = px.bar(
                        top, x=col_name, y="count", title=col_name,
                        color_discrete_sequence=["#a78bfa"],
                    )
                    fig.update_layout(
                        margin=dict(l=10, r=10, t=35, b=10),
                        height=230,
                        title_font_size=13,
                    )
                    col_widget.plotly_chart(fig, use_container_width=True)

        if not numeric_cols and not cat_cols:
            st.info("No plottable columns found.")

    st.divider()

    # ── Executive summary ──────────────────────────────────────────────────────
    st.subheader("📝 Executive Summary")

    if st.button("✨ Generate Executive Summary", type="primary"):
        client = get_client()
        prompt = f"""You are a senior data analyst reviewing the following dataset.

{st.session_state.data_context}

Write a concise, professional executive summary using markdown. Cover:

## Key Patterns & Trends
## Data Quality & Risks
## Opportunities & Insights
## Recommendations
"""
        with st.spinner("Generating summary…"):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                )
                st.session_state.summary = response.text
            except Exception as e:
                st.error(f"Summary generation failed: {e}")

    if st.session_state.summary:
        with st.container(border=True):
            st.markdown(st.session_state.summary)

    st.divider()

    # ── Chat assistant ─────────────────────────────────────────────────────────
    st.subheader("💬 Ask Echo")

    # Render existing conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("figure") is not None:
                st.plotly_chart(msg["figure"], use_container_width=True)

    # Accept new input via the dedicated chat input widget
    if question := st.chat_input("Ask Echo about your data…"):

        # ── Show user bubble immediately
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        client = get_client()
        chart_requested = is_chart_request(question)

        # ── System instruction sent with every turn
        chart_guidance = (
            "- If the user asks for a chart or visualisation, include your text analysis "
            "AND a single ```python code block. The code must create a Plotly figure stored "
            "in a variable named `fig`. Import `plotly.express as px` or "
            "`plotly.graph_objects as go` inside the block. The dataframe is available as `df`. "
            "Do NOT call `fig.show()`."
        ) if chart_requested else (
            "- Do NOT include Python code blocks unless explicitly asked for a chart."
        )

        system_instruction = f"""You are Echo, an expert data analyst assistant.
The user has uploaded a dataset. Here is its full profile:

{st.session_state.data_context}

Guidelines:
- Answer questions precisely using the data profile above.
- Use markdown formatting (bold, bullets, tables) for clarity.
- Reference specific column names, statistics, and values when relevant.
- Remember and reference prior messages in the conversation for follow-up questions.
{chart_guidance}
"""
        # Build history excluding the message we just appended (that becomes the new turn)
        prior_history = build_api_history(st.session_state.messages[:-1])

        # ── Call Gemini with full conversation history
        try:
            chat = client.chats.create(
                model=MODEL,
                history=prior_history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                ),
            )

            with st.chat_message("assistant"):
                with st.spinner("Echo is thinking…"):
                    response = chat.send_message(question)
                    answer_text = response.text

                st.markdown(answer_text)

                # ── Attempt to render a chart if one was requested
                fig = None
                if chart_requested:
                    code = extract_python_code(answer_text)
                    if code:
                        fig = render_chart_from_code(code, df)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info(
                            "Echo didn't produce chart code this time. "
                            "Try being more specific, e.g. *'plot a bar chart of X vs Y'*."
                        )

            st.session_state.messages.append(
                {"role": "assistant", "content": answer_text, "figure": fig}
            )

        except Exception as e:
            st.error(f"Echo encountered an error: {e}")

    st.divider()

    # ── Export report ──────────────────────────────────────────────────────────
    st.subheader("📥 Export Report")

    report_lines = [
        "Echo Data Intelligence Report",
        "=" * 50,
        f"File: {st.session_state.file_name}",
        f"Rows: {df.shape[0]:,}",
        f"Columns: {df.shape[1]}",
        f"Column names: {list(df.columns)}",
    ]

    if st.session_state.summary:
        report_lines += ["", "EXECUTIVE SUMMARY", "-" * 30, st.session_state.summary]

    if st.session_state.messages:
        report_lines += ["", "CHAT HISTORY", "-" * 30]
        for m in st.session_state.messages:
            label = "You" if m["role"] == "user" else "Echo"
            report_lines.append(f"\n[{label}]\n{m['content']}\n{'─' * 20}")

    report_bytes = BytesIO("\n".join(report_lines).encode("utf-8"))

    st.download_button(
        label="⬇️ Download Report (.txt)",
        data=report_bytes,
        file_name="Echo_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )

else:
    # ── Landing state when no file is uploaded ─────────────────────────────────
    st.info("👆 Upload a CSV or Excel file above to get started.")
    st.markdown(
        """
        **What Echo can do:**
        - 📊 Instantly profile your dataset (rows, columns, missing values)
        - 📈 Generate automatic EDA charts (histograms, correlation heatmap, value counts)
        - 📝 Write an AI-powered executive summary
        - 💬 Answer questions about your data with full conversation memory
        - 🎨 Generate custom Plotly charts on request
        - 📥 Export your full session as a report
        """
    )
