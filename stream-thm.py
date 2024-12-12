import streamlit as st
import requests
import re


def add_neumorphism_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #e0e5ec;
            font-family: 'Courier New', monospace;
        }
        .stApp {
            background-color: #e0e5ec;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 5px 5px 10px #babec4, -5px -5px 10px #ffffff;
        }
        .title {
            text-align: center;
            font-size: 2.5rem;
            color: #333333;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #555555;
        }
        .neumorphic-box {
            background: #e0e5ec;
            border-radius: 15px;
            box-shadow: 5px 5px 10px #babec4, -5px -5px 10px #ffffff;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        img {
            max-width: 100%;
            height: auto;
            margin-top: 10px;
            border-radius: 10px;
            box-shadow: 3px 3px 8px #babec4, -3px -3px 8px #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def extract_username(profile_url):
    """Extract username from TryHackMe profile URL."""
    match = re.search(r'tryhackme\.com/r/p/([^/\s]+)', profile_url)
    if match:
        return match.group(1)
    raise ValueError("Invalid TryHackMe profile URL format. Expected format: https://tryhackme.com/r/p/username")

def get_completed_rooms(username):
    """Fetch completed rooms for a given username."""
    url = "https://tryhackme.com/api/all-completed-rooms"
    headers = {"Content-Type": "application/json"}
    completed_rooms = []
    page = 1

    while True:
        params = {"username": username, "limit": 30, "page": page}
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            completed_rooms.extend([room["code"] for room in data])
            page += 1
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            break
    return completed_rooms


add_neumorphism_css()

st.markdown("<div class='title'>TryHackMe Completed Rooms Checker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Created by <a href='https://733nw0lf.github.io/' target='_blank'>Aswin Krishna</a></div>", unsafe_allow_html=True)

# guest@733nwolf:whoami and badge image
st.markdown("<div class='neumorphic-box'><strong>guest@733nwolf:whoami</strong></div>", unsafe_allow_html=True)
st.markdown(
    "<div class='neumorphic-box'><img src='https://tryhackme-badges.s3.amazonaws.com/733nwolf.png' alt='Your Image Badge' /></div>",
    unsafe_allow_html=True,
)

profile_url = st.text_input("Enter your TryHackMe profile URL (e.g., https://tryhackme.com/r/p/username):")

if st.button("Fetch Completed Rooms"):
    if profile_url:
        try:
            username = extract_username(profile_url)
            completed_rooms = get_completed_rooms(username)

            if completed_rooms:
                st.markdown(f"<div class='neumorphic-box'><strong>Completed rooms for user {username}:</strong></div>", unsafe_allow_html=True)
                for i, room_code in enumerate(completed_rooms, start=1):
                    st.write(f"{i}. {room_code}")
            else:
                st.warning("No completed rooms found or an error occurred.")
        except ValueError as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid TryHackMe profile URL.")
