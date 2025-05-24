import streamlit as st

st.set_page_config(page_title="Billionaires Statistics 2023", page_icon="💰", layout="wide")

from homepage import show as show_homepage
from facts import show as show_facts
from dataset import show as show_dataset
from code_page import show as show_code
from starts import show as show_starts

pages = {
    "facts": "👋 Billionaires and key facts",
    "dataset": "📚 Learn about our dataset",
    "code": "🧑‍💻 Explore our analysis code",
    "starts": "💰 Global billionaire statistics"
}

if "current_page" not in st.session_state:
    st.session_state.current_page = "homepage"

with st.sidebar:
    st.header("Navigation")

    # Nút Homepage riêng biệt
    is_home_selected = st.session_state.current_page == "homepage"
    home_bg = "#fff9c4" if is_home_selected else "transparent"
    if st.button("🏠 Homepage", use_container_width=True, key="btn_homepage"):
        st.session_state.current_page = "homepage"

    st.markdown("---")

    # Nút các trang còn lại (bỏ homepage)
    for i, (key, title) in enumerate(pages.items()):
        is_selected = st.session_state.current_page == key
        bg_color = "#fff9c4" if is_selected else "transparent"
        if st.button(title, use_container_width=True, key=f"btn_{key}_{i}"):
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







