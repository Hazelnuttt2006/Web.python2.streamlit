import streamlit as st
import os

def show():
    st.title("🔍 Explore Our App Code")

    st.markdown("""
    Welcome to the **Code Explorer** section!  
    Here you can view the source code behind each page of our app.  
    Use the dropdown menu below to select a specific page and see how it was built.
    """)

    # Dictionary of page labels and corresponding file names
    PAGE_FILES = {
        "🏠 Homepage": "homepage.py",
        "📊 Billionaires and Key Facts": "facts.py",
        "📚 Learn About Our Dataset": "dataset.py",
        "🧑‍💻 Explore Our Analysis Code": "code_page.py",
        "💰 Global Billionaire Statistics": "starts.py",
    }

    # Dropdown to select which page's code to view
    page_choice = st.selectbox(
        "👇 Select a page to view its source code:",
        options=list(PAGE_FILES.keys()),
        index=0
    )

    file_path = PAGE_FILES[page_choice]

    # Display code content or error if not found
    with st.container():
        if os.path.exists(file_path):
            st.success(f"📄 Showing source code from: `{file_path}`")
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            with st.expander("🔐 Click to show/hide the code", expanded=True):
                st.code(code, language="python")
        else:
            st.error(f"⚠️ File '{file_path}' not found. Please check if it exists.")


