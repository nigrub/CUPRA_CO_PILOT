import streamlit as st
import openai
import sqlite3
import datetime
from sqlite3 import Error

# Set your OpenAI API Key
openai.api_key = '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'

# Database setup
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('conversations.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        query = '''
            CREATE TABLE IF NOT EXISTS conversations (
                id integer PRIMARY KEY,
                chat_id text NOT NULL,
                timestamp text NOT NULL,
                role text NOT NULL,
                content text NOT NULL
            );
        '''
        conn.execute(query)
        print('Table created successfully')
    except Error as e:
        print(e)

def save_message_in_db(conn, chat_id, role, content):
    timestamp = datetime.datetime.now()
    query = '''
        INSERT INTO conversations(chat_id, timestamp, role, content)
        VALUES(?, ?, ?, ?);
    '''
    try:
        conn.execute(query, (chat_id, timestamp, role, content))
        conn.commit()
    except Error as e:
        print(e)

def get_all_chat_ids(conn):
    query = "SELECT DISTINCT chat_id FROM conversations ORDER BY id DESC"
    rows = conn.execute(query).fetchall()
    return [row[0] for row in rows]

def get_conversation_by_chat_id(conn, chat_id):
    query = "SELECT * FROM conversations WHERE chat_id = ?"
    rows = conn.execute(query, (chat_id,)).fetchall()

    # Convert rows to the correct format
    messages = [{'role': row[3], 'content': row[4]} for row in rows]

    return messages

# Create connection and table
conn = create_connection()
if conn is not None:
    create_table(conn)

# Chatbot setup
def chat_with_gpt3(chat_id, messages, user_input):
    model = 'gpt-3.5-turbo'

    messages.append({
        'role': 'user',
        'content': user_input
    })

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    reply = response.choices[0].message['content']

    messages.append({
        'role': 'assistant',
        'content': reply
    })

    # Store all messages in the database
    for message in messages:
        save_message_in_db(conn, chat_id, message['role'], message['content'])

    return reply, messages

# Streamlit app
st.title("CUPRA Co-Pilot")

# Initialize session state variables
if 'chat_id' not in st.session_state:
    st.session_state.chat_id = ''
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are chatting with the CUPRA Co-Pilot, how can I help today?'}]

# Create a new chat
chat_name = st.sidebar.text_input('Enter Chat Name')
if st.sidebar.button('Create New Chat') or chat_name:
    st.session_state.chat_id = chat_name
    st.session_state.messages = [{'role': 'system', 'content': 'You are chatting with the CUPRA Co-Pilot, how can I help today?'}]

# Load a chat
chat_ids = get_all_chat_ids(conn)
for chat_id in chat_ids:
    if st.sidebar.button(f'{chat_id}'):
        st.session_state.chat_id = chat_id
        st.session_state.messages = get_conversation_by_chat_id(conn, st.session_state.chat_id)

# Get conversation of the current chat
if 'chat_id' in st.session_state and 'messages' in st.session_state:
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px;">User: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color: #d0d0d0; padding: 10px; border-radius: 10px;">CUPRA Co-Pilot: {message["content"]}</div>', unsafe_allow_html=True)

user_input = st.text_input("Type your message here...", key='user_input')

if st.button("Send", key='send_button') or user_input:
    reply, st.session_state.messages = chat_with_gpt3(st.session_state.chat_id, st.session_state.messages, user_input)
    st.markdown(f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px;">User: {user_input}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background-color: #d0d0d0; padding: 10px; border-radius: 10px;">CUPRA Co-Pilot: {reply}</div>', unsafe_allow_html=True)
    st.session_state.user_input = ""
