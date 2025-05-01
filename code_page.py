import streamlit as st

def show():
    st.title("🧑‍💻 Explore Our Analysis Code")
    st.write("We used Python and libraries such as Pandas, Matplotlib, and Streamlit to visualize and analyze the dataset.")
    code = '''
import pandas as pd
df = pd.read_csv("billionaires.csv")
df.head()
    '''
    st.code(code, language='python')
