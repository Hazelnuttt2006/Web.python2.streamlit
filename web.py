import streamlit as st

# Import content files
from homepage import show as show_homepage
from facts import show as show_facts
from dataset import show as show_dataset
from code_page import show as show_code
from starts import show as show_starts

# Mapping page keys
pages = {
    "facts": "👋 Billionaires and key facts",
    "dataset": "📚 Learn about our dataset",
    "code": "🧑‍💻 Explore our analysis code",
    "starts": "💰 Global billionaire statistics"
}

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "homepage"

# Sidebar layout
with st.sidebar:
    # Homepage - kiểu như tiêu đề lớn
    is_home_selected = st.session_state.current_page == "homepage"
    home_bg = "#fff9c4" if is_home_selected else "transparent"

    if st.button("🏠 Homepage", use_container_width=True):
        st.session_state.current_page = "homepage"

    st.markdown("---")  # phân cách

    # Các mục còn lại
    for key, title in pages.items():
        is_selected = st.session_state.current_page == key
        bg_color = "#fff9c4" if is_selected else "transparent"

        # Custom styled clickable block
        if st.button(title, use_container_width=True):
            st.session_state.current_page = key

# Hiển thị nội dung phù hợp
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



