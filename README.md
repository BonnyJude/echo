# Echo — Data Intelligence Assistant 🚀

## Executive Summary

**Echo** is a state-of-the-art, AI-driven data intelligence platform designed to transform raw tabular datasets into actionable strategic insights. Powered by Google's latest **Gemini models** (`gemini-2.5-flash`), Echo provides senior-level data analysis, multi-turn conversational exploration, dynamic Plotly chart generation, automatic Exploratory Data Analysis (EDA), and seamless report exports.

Designed for modern analysts, managers, and decision-makers who demand speed without sacrificing depth, Echo acts as a force multiplier for data-driven teams.

---

## 🌟 Visual Preview & Key Features

### 1. Landing & Seamless Data Ingestion

Upload CSV or Excel (`.xlsx`) files up to standard Streamlit limits with automatic data profiling.

![Echo Landing Page](<files/Echo — Data Intelligence Assistant Homepage.png>)

### 2. Dataset Profiling & Executive Summaries

Instantly inspect row counts, column counts, missing value summaries, numeric column distributions, and detailed previews. Generate structured, C-suite ready executive summaries covering key patterns, risks, opportunities, and strategic recommendations at the click of a button.

![Data Profiling & Summary](<files/Echo — Data Intelligence Assistant Loan_data demo page.png>)

### 3. Automatic Exploratory Data Analysis (EDA)

Echo automatically renders high-level visualizations for uploaded datasets, including numeric distribution histograms, categorical value count bar charts, and interactive Pearson correlation heatmaps.

![Automatic EDA Charts](<files/Echo — Data Intelligence Assistant charts demo.png>)

### 4. Conversational Intelligence & Dynamic Chart Generation

Ask complex questions about your data with full **multi-turn conversation memory**. Ask follow-up questions freely (e.g., *"expand on that risk"*, *"what about high-income borrowers?"*). Request custom charts simply by asking (e.g., *"plot a bar chart of loan_amount by homeownership"* or *"show me a scatter plot"*), and Echo writes and executes interactive **Plotly** visualizations on the fly.

![Conversational Assistant & Follow-ups](<files/Echo — Data Intelligence Assistant conversation demo.png>)

### 5. Comprehensive Report Export & Easy Copy-Pasting

Export your entire session—including data profiles, the AI executive summary, and complete chat history—as a clean, structured `.txt` report directly in your browser.

> 💡 **Tip:** The exported `.txt` report is formatted using standard markdown headers, bullet points, and divider sections. You can easily copy and paste its contents directly into **Google Docs, Microsoft Word, Notion**, or any **Markdown (`.md`)** editor without needing any extra formatting!

---

## 🛠️ Technology Stack

- **UI Framework:** [Streamlit](https://streamlit.io/) 1.54+
- **Data Engine:** [Pandas](https://pandas.pydata.org/) & [Openpyxl](https://openpyxl.readthedocs.io/)
- **Visualizations:** [Plotly Express & Graph Objects](https://plotly.com/python/)
- **AI Core:** [Google GenAI SDK](https://github.com/googleapis/python-genai) (`google-genai` with Gemini models)
- **Language:** Python 3.12+

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher.
- A Google Gemini API Key (get one from [Google AI Studio](https://aistudio.google.com/)).

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd echo
   ```

2. **Set up virtual environment:**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key:**
   Create a `.env` file in the root directory:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   *Or configure `GEMINI_API_KEY` inside `.streamlit/secrets.toml`.*

### Running the Application

Launch the app with Streamlit:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📖 Usage Guide

1. **Upload Dataset:** Drag and drop your CSV or Excel file into the file uploader.
2. **Review Profile & EDA:** Expand **Automatic EDA Charts** to view data distributions and correlation heatmaps.
3. **Generate Summary:** Click **Generate Executive Summary** for an AI analysis of key trends, data quality risks, and opportunities.
4. **Chat & Follow-up:** Use the **Ask Echo** chat input to ask questions about your dataset. Ask follow-up questions naturally—Echo retains full conversation context.
5. **Request Custom Charts:** Ask Echo to plot specific variables (e.g., *"show me a distribution of debt_to_income"*), and view interactive Plotly charts directly in the chat.
6. **Download Report:** Click **Download Report (.txt)** to save your session output, ready to paste into documentation or executive slide decks.

---

*Echo — Listen to what your data is telling you.* 🔊
