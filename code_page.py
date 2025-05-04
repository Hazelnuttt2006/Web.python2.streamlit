import streamlit as st
import os

def show():
    st.subheader("Explore Our App Page Code 🧑‍💻")
    st.write("Select a page below to view its source code:")

    PAGE_FILES = {
        "🏠 Homepage": "homepage.py",
        "👋 Billionaires and key facts": "facts.py",
        "📚 Learn about our dataset": "dataset.py",
        "🧑‍💻 Explore our analysis code": "code_page.py",
        "💰 Global billionaire statistics": "starts.py",
    }

    page_choice = st.selectbox(
        "Which page code would you like to view?", 
        options=list(PAGE_FILES.keys()),
        index= list(PAGE_FILES.keys()).index("🏠 Homepage")
    )

    file_path = PAGE_FILES[page_choice]
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        st.code(code, language="python")
    else:
        st.error(f"File '{file_path}' not found. Ensure it exists in the app directory.")

