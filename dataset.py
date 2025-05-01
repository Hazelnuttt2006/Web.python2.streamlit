import streamlit as st

def show():
    st.title("📚 Learn About Our Dataset")
    st.write("Our dataset includes information on global billionaires in 2023, such as:")
    st.markdown("""
    - **Name**
    - **Net Worth**
    - **Country**
    - **Industry**
    - **Source of Wealth**
    """)
    st.info("Source: Forbes 2023 Billionaires List")
