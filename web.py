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

# Sidebar
with st.sidebar:
    st.title("📊 Billionaires 2023")
    st.caption("Use the menu below to explore insights, data, and analysis.")

    st.markdown("### 📌 Navigation")

    
    if st.button("🏠 Homepage", use_container_width=True):
        st.session_state.current_page = "homepage"

   
    st.markdown("---")

   
    for key, title in pages.items():
        if st.button(title, use_container_width=True):
            st.session_state.current_page = key

page = st.session_state.current_page

if page != "homepage":
    st.markdown(f"## {pages.get(page, '')}")


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








