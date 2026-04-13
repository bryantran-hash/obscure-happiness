import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Setup the Page
st.set_page_config(page_title="Grant Assistant")
st.title("📑 Grant Guideline Chatbot")
st.markdown("Use this tool to ask questions about current grant funding rules and eligibility.")

# 2. Load the Data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("guidelines.csv")
    except Exception:
        st.error("Error: The file 'guidelines.csv' was not found on GitHub. Please check the filename.")
        return None

df = load_data()

# 3. Connect to the AI Brain
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
else:
    st.error("Secret Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")

# 4. The Chat Interface
if df is not None:
    query = st.text_input("Ask a question about the grants:")

    if query:
        context = df.to_string()
        prompt = f"Guidelines: {context}\n\nQuestion: {query}"
        
        with st.spinner('Thinking...'):
            response = model.generate_content(prompt)
            st.write("### Answer:")
            st.info(response.text)
