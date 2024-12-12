import streamlit as st
import requests
import re

def extract_username(profile_url):
    """Extract username from TryHackMe profile URL."""
    # Match the username pattern after /p/ in the URL
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

# Streamlit App
st.title("TryHackMe Completed Rooms Checker")

profile_url = st.text_input("Enter your TryHackMe profile URL (e.g., https://tryhackme.com/r/p/username):")

if st.button("Fetch Completed Rooms"):
    if profile_url:
        try:
            username = extract_username(profile_url)
            completed_rooms = get_completed_rooms(username)

            if completed_rooms:
                st.success(f"Completed rooms for user {username}:")
                for i, room_code in enumerate(completed_rooms, start=1):
                    st.write(f"{i}. {room_code}")
            else:
                st.warning("No completed rooms found or an error occurred.")
        except ValueError as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid TryHackMe profile URL.")
