import openai
import streamlit as st
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone
import uuid
import random

st.title("Welcome To The CUPRA Co-Pilot")

openai.api_key = st.secrets["openai"]["api_key"]

st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
gc = gspread.authorize(credentials)

sheet = gc.open('CUPRADB').sheet1

# Sidebar for input chat name and new conversation button
with st.sidebar:
    st.header("Chat Options")
    chat_name = st.text_input("Chat Name")
    if st.button("New Conversation"):
        # Empty the messages
        st.session_state.messages = []

    # Display historical conversations
    st.header("Historical Conversations")
    all_records = sheet.get_all_records()
    for record in all_records:
        chat_id = record['chat_id']  # get the chat_id from record
        if chat_id != "load":
            chat_name = chat_id.split('-')[0]  # only display the name part
            if st.button(chat_name):
                st.session_state.messages = [r for r in all_records if r["chat_id"] == chat_id]

# Main chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Generate a unique chat_id for this conversation
    if "chat_id" in st.session_state:
        chat_id = st.session_state.chat_id
    else:
        chat_id = f"{chat_name}-{random.randint(10000000, 99999999)}"
        st.session_state.chat_id = chat_id

    st.session_state.messages.append({"role": "user", "content": prompt, "chat_id": chat_id})
    with st.chat_message("user"):
        st.markdown(prompt)
        sheet.append_row([str(uuid.uuid4()), str(chat_id), str(datetime.now(timezone.utc)), "user", prompt])  # Add user prompt to Google Sheet

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
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