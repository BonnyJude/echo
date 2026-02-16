# Echo — Data Intelligence Assistant 🚀

## Executive Summary
Echo is a sophisticated, AI-driven data intelligence platform designed to transform raw datasets into actionable strategic insights. By leveraging state-of-the-art generative AI models, Echo provides senior-level data analysis at the click of a button. The application streamlines the entire data lifecycle—from initial ingestion and profiling to deep conversational exploration and comprehensive report generation. Designed for modern professionals who demand speed without sacrificing depth, Echo acts as a force multiplier for data-driven decision-making, ensuring that key patterns and opportunities are never overlooked.

---

## Overview
Welcome to **Echo**, your new partner in data exploration. In an era where data is plentiful but insight is rare, Echo bridges the gap. Built with a focus on simplicity and power, Echo allows you to upload complex datasets and immediately receive high-level executive summaries and conversational answers to your most pressing business questions.

## Key Features
- **Seamless Data Ingestion:** Effortlessly upload CSV or Excel files to begin your analysis.
- **Instant Data Profiling:** Get an immediate snapshot of your dataset’s scale, including row counts, column structures, and a polished preview.
- **AI-Powered Executive Summaries:** Utilising the latest Gemini models, Echo identifies key patterns, risks, and opportunities within your data, delivering a professional summary in seconds.
- **Conversational Intelligence:** Ask Echo anything about your data. Whether you're looking for specific trends or complex correlations, our chat assistant provides precise, context-aware answers.
- **Comprehensive Report Export:** Finalise your findings by exporting a full report that includes data profiles, the AI executive summary, and your entire chat history—perfect for sharing with stakeholders.

## Technology Stack
Echo is built using a modern, robust stack:
- **Streamlit:** For a sleek, responsive, and intuitive user interface.
- **Pandas & Openpyxl:** For high-performance data manipulation and spreadsheet support.
- **Google GenAI (Gemini):** Powering the core intelligence and natural language processing capabilities.
- **Python 3.12+:** The backbone of our logic and integration.

## Getting Started

### Prerequisites
- Python 3.12 or higher.
- A Google Gemini API Key.

### Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd echo
   ```

2. **Set up your virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application
Launch the Echo interface with Streamlit:
```bash
streamlit run app.py
```

## Usage
1. **Upload:** Drag and drop your CSV or Excel file into the uploader.
2. **Profile:** Review the dataset preview and basic metrics to ensure data integrity.
3. **Summarise:** Click "Generate Executive Summary" for a deep-dive analysis into the data's narrative.
4. **Enquire:** Use the "Ask Echo" field to probe deeper into specific metrics or hypotheses.
5. **Export:** Click "Export Report" to save your entire session into a clean, professional text file for your records.

---

## Professional Standards
Echo is built with a commitment to clean code and efficient performance. We prioritise UTF-8 encoding for global compatibility and utilise session state management to ensure your analysis remains persistent throughout your session.

*Echo — Listen to what your data is telling you.*
