import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Setup the Page (This makes the website look professional)
st.set_page_config(page_title="Grant Assistant", layout="centered")
st.title("📑 Grant Guideline Chatbot")
st.markdown("Use this tool to ask questions about current grant funding rules and eligibility.")

# 2. Load the Data
# This part tells the app to look for your 'guidelines.csv' file
@st.cache_data
def load_data():
    try:
        return pd.read_csv("guidelines.csv")
    except FileNotFoundError:
        st.error("Error: The file 'guidelines.csv' was not found on GitHub. Please check the filename.")
        return None

df = load_data()

# 3. Connect to the AI Brain
# It looks for the GOOGLE_API_KEY you saved in the 'Secrets' section
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets[AIzaSyALKjQPFAvOFEf6cqpvJ9XfDEu4KifFM5c])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Error: API Key missing. Please add GOOGLE_API_KEY to your Streamlit Secrets.")

# 4. The Chat Interface
if df is not None:
    query = st.text_input("Ask a question about the grants (e.g., 'What are the travel rules for ARC?'):")

    if query:
        # We turn your spreadsheet into text so the AI can read it
        context = df.to_string()
        
        # This hidden prompt tells the AI how to behave
        prompt = f"""
        You are a helpful Grant Administration Assistant. 
        Answer the user's question using ONLY the information provided in the guidelines below.
        If the information is not in the data, politely say that the specific guideline isn't available.
        Use bullet points to make the answer easy for researchers to read.

        GUIDELINES DATA:
        {context}
        
        USER QUESTION:
        {query}
        """
        
        with st.spinner('Checking guidelines...'):
            try:
                response = model.generate_content(prompt)
                st.write("### Answer:")
                st.info(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")