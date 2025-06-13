import streamlit as st
from streamlit_extras.stoggle import stoggle
from streamlit_extras.let_it_rain import rain
import base64
import os  

def show():
    st.subheader("Group F415")
    st.title("👩‍💻PYTHON 2 - BUSINESS IT 2 😊:")
    st.write("""
    We are a group of business students passionate about understanding global economic dynamics.
    For our analysis, we focused on a dataset detailing the distribution of wealth among billionaires in 2023.
    Through this visualization, we aim to offer a comprehensive view of how the billionaire landscape has evolved this year,
    shedding light on notable trends and shifts in wealth accumulation.
    """)

    stoggle(
        "Group information",
        """
    1. Au Hong An - 106240010

    2. Le Ho Thu Giang - 106240409

    3. Luu Ngoc Phuong Khanh - 106240260

    4. Nguyen Ngoc Thao An - 103240210
        """,
    )

    st.write("[Accessing our dataset >](https://docs.google.com/spreadsheets/d/1STYDa2xArV1B6D1R9hZSHRp4lSp1o8welEsCN62zfVk/edit?usp=sharing)")

    rain(emoji="🪙", font_size=54, falling_speed=5, animation_length="3")

    st.markdown("""
    <div style="margin-top: 30px;">
        <div style="height: 8px; background-color: #FFC200; width: 100%; border-radius: 4px;"></div>
        <h3 style="margin-top: 10px;">👧 Group members introduction</h3>
        <p style="color: gray;">Get to know about our group</p>
    </div>
""", unsafe_allow_html=True)


    def circular_image(image_path, width=180):
        if not os.path.exists(image_path):
            return f"<p style='color:red;'>Image {image_path} not found!</p>"

        with open(image_path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return f'''
            <img src="data:image/png;base64,{encoded}" 
                 style="border-radius: 50%; width: {width}px; height: {width}px; object-fit: cover; display: block; margin-left: auto; margin-right: auto;">
        '''

    members = [
        {
            "name": "Nguyen Ngoc Thao An (Group leader)",
            "id": "103240210",
            "email": "103240210@student.vgu.edu.vn",
            "major": "Finance & Accounting (BFA)",
            "img": "3.png"
        },
        {
            "name": "Au Hong An",
            "id": "106240010",
            "email": "106240010@student.vgu.edu.vn",
            "major": "Business Administration (BBA)",
            "img": "2.png"
        },
        {
            "name": "Le Ho Thu Giang",
            "id": "106240409",
            "email": "106240409@student.vgu.edu.vn",
            "major": "Business Administration (BBA)",
            "img": "1.png"
        },
        {
            "name": "Luu Ngoc Phuong Khanh",
            "id": "106240260",
            "email": "106240260@student.vgu.edu.vn",
            "major": "Business Administration (BBA)",
            "img": "4.png"
        },
    ]

    # Display members in a single horizontal row
    cols = st.columns(4)
    for col, member in zip(cols, members):
        with col:
            st.markdown(circular_image(member["img"]), unsafe_allow_html=True)
            st.markdown(f"""
            <div style='text-align: center;'>
                <strong>{member['name']}</strong><br>
                ID: {member['id']}<br>
                <a href="mailto:{member['email']}">{member['email']}</a><br>
                Major: {member['major']}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💬 Leave us your message!")
    st.caption("Let us know if you have any recommendations")

    contactform = """
    <style>
        .contact-form-container {
            max-width: 500px;
            margin-left: 0;
        }
        .contact-form-container input,
        .contact-form-container textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }
        .contact-form-container button {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .contact-form-container button:hover {
            background-color: #0056b3;
        }
    </style>

    <div class="contact-form-container">
    <form action="https://formsubmit.co/103240210@student.vgu.edu.vn" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email address" required>
        <textarea name="message" placeholder="What do you think?" rows="4" required></textarea>
        <button type="submit">Send</button>
    </form>
    </div>
    """
    st.markdown(contactform, unsafe_allow_html=True)