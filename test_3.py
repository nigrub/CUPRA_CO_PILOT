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
        # Empty the messages
        st.session_state.messages = []
        # Generate a new chat_id
        if chat_name:
            st.session_state.chat_id = generate_chat_id(chat_name)
            # Add the new chat_id to the historical conversations list
            unique_chat_ids = set(record['chat_id'] for record in sheet.get_all_records() if record['chat_id'] != "load")
            unique_chat_ids.add(st.session_state.chat_id)
            st.session_state.historical_conversations = list(unique_chat_ids)

    # Display historical conversations
    st.header("Historical Conversations")
    all_records = sheet.get_all_records()
    unique_chat_ids = list(set(record['chat_id'] for record in all_records if record['chat_id'] != "load"))  # get unique chat_ids
    st.session_state.historical_conversations = st.session_state.historical_conversations if "historical_conversations" in st.session_state else unique_chat_ids

    # Sort chat_ids based on the most recent message timestamp
    sorted_chat_ids = sorted(
        st.session_state.historical_conversations,
        key=lambda chat_id: max(r["timestamp"] for r in all_records if r["chat_id"] == chat_id),
        reverse=True
    )

    for chat_id in sorted_chat_ids:
        chat_name = str(chat_id).split('-')[0]  # only display the name part
        if st.button(chat_name, key=f"chat_button_{chat_id}", help=chat_id):
            st.session_state.messages = [r for r in all_records if r["chat_id"] == chat_id]
            st.session_state.chat_id = chat_id

# Main chat
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if st.session_state.chat_id is None:
    if chat_name:
        st.session_state.chat_id = generate_chat_id(chat_name)

# Display the currently engaged chat name at the top
if st.session_state.chat_id:
    current_chat_name = str(st.session_state.chat_id).split('-')[0]
    st.header(f"Engaged Chat: {current_chat_name}")

if st.session_state.chat_id:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ...

    if prompt := st.chat_input("What is up?"):
        # Generate a unique chat_id for this conversation
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
                    ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response, "chat_id": chat_id})
        sheet.append_row([str(uuid.uuid4()), str(chat_id), str(datetime.now(timezone.utc)), "assistant", full_response])  # Add assistant response to Google Sheet
