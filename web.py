import streamlit as st


st.set_page_config(page_title="Billionaires Statistics 2023", page_icon="💰", layout="wide")


from homepage import show as show_homepage
from facts import show as show_facts
from dataset import show as show_dataset
from code_page import show as show_code
from starts import show as show_starts


pages = {
    "homepage": "🏠 Homepage",
    "facts": "👋 Billionaires and key facts",
    "dataset": "📚 Learn about our dataset",
    "code": "🧑‍💻 Explore our analysis code",
    "starts": "💰 Global billionaire statistics"
}


if "current_page" not in st.session_state:
    st.session_state.current_page = "homepage"


with st.sidebar:
    st.header("Navigation")
    is_home_selected = st.session_state.current_page == "homepage"
    

    if st.button("🏠 Homepage", use_container_width=True):
        st.session_state.current_page = "homepage"
    
    st.markdown("---")  
    
    for key, title in pages.items():
        if key != "homepage":  
            if st.button(title, use_container_width=True):
                st.session_state.current_page = key

page = st.session_state.current_page
if page == "homepage":
    show_homepage()
elif page == "facts":
    show_facts()
elif page == "dataset":
    show_dataset()
elif page == "code":
    show_code()
elif page == "starts":
    show_starts()





