import streamlit as st
import pandas as pd

def show():
    st.title("💰 Global Billionaire Statistics")
    st.write("Here is a small sample of statistics from our dataset.")

    # Sample data for demo
    data = {
        "Country": ["USA", "China", "India", "Germany"],
        "Number of Billionaires": [735, 495, 169, 134]
    }
    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("Country"))
