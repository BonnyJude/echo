import streamlit as st
import pandas as pd
import os
from google import genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# App config
st.set_page_config(
    page_title="Echo — Data Intelligence Assistant",
    layout="wide"
)

st.title("Echo — Data Intelligence Assistant")

# Initialize session state for persistence
if "summary" not in st.session_state:
    st.session_state.summary = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Data profile
    st.subheader("Data Profile")

    col1, col2 = st.columns(2)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.write("Columns:", list(df.columns))

    # Executive summary
    if st.button("Generate Executive Summary"):

        preview = df.head(50).to_string()

        prompt = f"""
        You are a senior data analyst.

        Dataset preview:
        {preview}

        Write an executive summary covering:

        - Key patterns
        - Risks
        - Opportunities
        - Data quality
        - Recommendations
        """

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        st.session_state.summary = response.text

    if st.session_state.summary:
        st.subheader("Executive Summary")
        st.write(st.session_state.summary)

    # Chat assistant
    st.subheader("Ask Echo")
    question = st.text_input("Ask Echo about your data")

    if question:

        preview = df.head(50).to_string()

        prompt = f"""
        Dataset preview:
        {preview}

        Question:
        {question}
        """

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        st.session_state.chat_history.append((question, response.text))

    if st.session_state.chat_history:
        for q, r in st.session_state.chat_history:
            st.write(f"**Question:** {q}")
            st.write(f"**Echo:** {r}")
            st.divider()

    # Export report
    if st.button("Export Report"):

        report = f"""
Echo Data Report

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Columns:
{list(df.columns)}
"""
        if st.session_state.summary:
            report += f"\n\nExecutive Summary:\n{st.session_state.summary}"

        if st.session_state.chat_history:
            report += "\n\nChat History:\n"
            for q, r in st.session_state.chat_history:
                report += f"\nQuestion: {q}\nEcho: {r}\n{'-'*20}\n"

        with open("Echo_Report.txt", "w", encoding="utf-8") as f:
            f.write(report)

        st.success("Report exported to Echo_Report.txt")
