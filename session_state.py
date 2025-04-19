import streamlit as st
import json
import os

# Define the name of the file where session data will be stored
DATA_FILE = "data.json"

# Function to initialize or retrieve session state
def get_session():
    # Initialize 'attempts' in session state if not already present
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0

    # Initialize 'authorized' in session state if not already present
    if 'authorized' not in st.session_state:
        st.session_state.authorized = True

    # Initialize 'data_store' in session state if not already present
    if 'data_store' not in st.session_state:
        # Check if the data file exists
        if os.path.exists(DATA_FILE):
            try:
                # Open and read the data file
                with open(DATA_FILE, "r") as f:
                    content = f.read().strip()
                    if content:  # If the file is not empty, load its content into session state
                        st.session_state.data_store = json.loads(content)
                    else:  # If the file is empty, initialize an empty dictionary
                        st.session_state.data_store = {}
            except json.JSONDecodeError:
                # Handle corrupted JSON file by warning the user and resetting the file
                st.warning("⚠️ data.json is corrupted. Resetting it.")
                st.session_state.data_store = {}
                save_to_file()  # Reset the file with an empty dictionary
        else:
            # If the file does not exist, initialize an empty dictionary
            st.session_state.data_store = {}

# Function to save the session state data to the file
def save_to_file():
    # Write the current session state data to the file in JSON format
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data_store, f)