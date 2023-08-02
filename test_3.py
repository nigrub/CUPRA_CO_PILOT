import openai
import streamlit as st
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone
import uuid
import random
import time

st.title("Welcome To The CUPRA Co-Pilot")

openai.api_key = st.secrets["openai"]["api_key"]

st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4"

# Function to generate a new chat_id
def generate_chat_id(chat_name):
    return f"{chat_name}-{random.randint(10000000, 99999999)}"

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
gc = gspread.authorize(credentials)
sheet = gc.open('CUPRADB').sheet1

# Sidebar for input chat name and new conversation button
with st.sidebar:
    st.header("Chat History")
    chat_name = st.text_input("Chat Name")
    if st.button("New Conversation"):
        if chat_name:
            # Generate a new chat_id
            st.session_state.chat_id = generate_chat_id(chat_name)
            # Empty the messages
            st.session_state.messages = []
            # Add the new chat_id to the Google Sheet as a load record
            sheet.append_row([str(uuid.uuid4()), str(st.session_state.chat_id), str(datetime.now(timezone.utc)), "load", "load"])

    # Display historical conversations
    st.header("Historical Conversations")
    all_records = sheet.get_all_records()
    unique_chat_ids = list(set(record['chat_id'] for record in all_records if record['chat_id'] != "load"))  # get unique chat_ids
    unique_chat_names = list(set(chat_id.split("-")[0] for chat_id in unique_chat_ids))  # Get the list of unique chat names from chat_ids
    sorted_chat_names = sorted(
        unique_chat_names,
        key=lambda chat_name: max((r["timestamp"] for r in all_records if r["chat_id"].startswith(chat_name)), default='0001-01-01T00:00:00Z'),
        reverse=True
    )  # Sort chats based on the most recent message timestamp

    # Add blank lines between each chat name
    formatted_chat_names = [chat for sublist in [[chat_name, " "] for chat_name in sorted_chat_names] for chat in sublist]
    formatted_chat_names = formatted_chat_names if formatted_chat_names else ["No Conversations Available"]

    selected_chat_name = st.radio("Choose a conversation", options=formatted_chat_names, key="selected_chat_name")

    # If a chat name is selected, load its messages
    if selected_chat_name and selected_chat_name not in [" ", "No Conversations Available"]:
        selected_chat_id_full = max((record['chat_id'] for record in all_records if record["chat_id"].startswith(selected_chat_name)), default=None)
        st.session_state.messages = [r for r in all_records if r["chat_id"] == selected_chat_id_full]
        st.session_state.chat_id = selected_chat_id_full

# Main chat
if st.session_state.chat_id:
    for message in st.session_state.messages:
        if message["role"] != "load":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        chat_id = st.session_state.chat_id

        st.session_state.messages.append({"role": "user", "content": prompt, "chat_id": chat_id})
        with st.chat_message("user"):
            st.markdown(prompt)
            sheet.append_row([str(uuid.uuid4()), str(chat_id), str(datetime.now(timezone.utc)), "user", prompt])  # Add user prompt to Google Sheet

        # predefined responses
        predefined_answers = {
            "What is Amy's favourite colour?": "Red"
            # You can add more predefined answers here...
        }

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            if prompt in predefined_answers:
                full_response = predefined_answers[prompt]
                time.sleep(3)  # pause for 3 seconds
                message_placeholder.markdown(full_response)
            else:
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                        if m["role"] != "load"
                    ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response, "chat_id": chat_id})
        sheet.append_row([str(uuid.uuid4()), str(chat_id), str(datetime.now(timezone.utc)), "assistant", full_response])  # Add assistant response to Google Sheet
