import streamlit as st
import openai
import sqlite3
import datetime
from sqlite3 import Error
from streamlit import components
import uuid

# Set your OpenAI API Key
openai.api_key = st.secrets["openai"]["api_key"]

# Database setup
def create_connection():
    conn = None
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
                content text NOT NULL,
                rating integer
            );
        '''
        conn.execute(query)
        print('Table created successfully')
    except Error as e:
        print(e)

def save_message_in_db(conn, chat_id, role, content, rating=None):
    timestamp = datetime.datetime.now()
    query = '''
        INSERT INTO conversations(chat_id, timestamp, role, content, rating)
        VALUES(?, ?, ?, ?, ?);
    '''
    try:
        conn.execute(query, (chat_id, timestamp, role, content, rating))
        conn.commit()
    except Error as e:
        print(e)

def get_all_chat_ids(conn):
    query = "SELECT DISTINCT chat_id FROM conversations"
    rows = conn.execute(query).fetchall()
    return [row[0] for row in rows]

def get_conversation_by_chat_id(conn, chat_id):
    query = "SELECT * FROM conversations WHERE chat_id = ? ORDER BY timestamp DESC"
    rows = conn.execute(query, (chat_id,)).fetchall()
    messages = [{'role': row[3], 'content': row[4]} for row in rows]
    return messages

# Create connection and table
conn = create_connection()
if conn is not None:
    create_table(conn)

# Chatbot setup
def chat_with_gpt3(chat_id, messages, user_input=None):
    model = 'gpt-3.5-turbo'

    if user_input is not None:
        messages.append({
            'role': 'user',
            'content': user_input
        })

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    reply = response.choices[0].message['content']

    if user_input is not None:
        messages.append({
            'role': 'assistant',
            'content': reply
        })

    for message in messages:
        save_message_in_db(conn, chat_id, message['role'], message['content'])

    return reply, messages

# Streamlit app
st.markdown(f"""
    <style>
        body {{
            background-color: #FFFFFF;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("CUPRA Co-Pilot")

# Initialize session state variables
if 'chat_id' not in st.session_state:
    st.session_state['chat_id'] = ''
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'system', 'content': 'You are chatting with the CUPRA Co-Pilot, how can I help today?'}]
if 'last_user_input' not in st.session_state:
    st.session_state['last_user_input'] = ''

# Create a new chat
chat_id = st.sidebar.text_input('Enter Chat Name', key='new_chat_id')

if st.sidebar.button('Create New Chat') or chat_id:
    st.session_state.chat_id = chat_id
    st.session_state.messages = [{'role': 'system', 'content': 'You are chatting with the CUPRA Co-Pilot, how can I help today?'}]

# Load a chat
chat_ids = get_all_chat_ids(conn)
for chat_id in sorted(chat_ids, reverse=True):
    if st.sidebar.button(f'{chat_id}'):
        st.session_state.chat_id = chat_id
        st.session_state.messages = get_conversation_by_chat_id(conn, st.session_state.chat_id)

# Get conversation of the current chat
if 'chat_id' in st.session_state and 'messages' in st.session_state:
    for message in reversed(st.session_state.messages):
        if message['role'] == 'user':
            st.markdown(f'<div style="padding:10px;margin:5px;border-radius:5px;background-color:#EDF7FF;color:#4E4E4E;">User: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="padding:10px;margin:5px;border-radius:5px;background-color:#F8F8F8;color:black;">CUPRA Co-Pilot: {message["content"]}</div>', unsafe_allow_html=True)

# Create a unique key for the user_input widget
unique_key = str(uuid.uuid4())

user_input = st.text_input("Type your message here...", key=unique_key)

if st.button("Send"):
    st.session_state['last_user_input'] = user_input
    reply, st.session_state.messages = chat_with_gpt3(st.session_state.chat_id, st.session_state.messages, user_input)
    st.markdown(f'<div style="padding:10px;margin:5px;border-radius:5px;background-color:#F8F8F8;color:black;">CUPRA Co-Pilot: {reply}</div>', unsafe_allow_html=True)

if st.button("Regenerate Response"):
    reply, st.session_state.messages = chat_with_gpt3(st.session_state.chat_id, st.session_state.messages, st.session_state['last_user_input'])
    st.markdown(f'<div style="padding:10px;margin:5px;border-radius:5px;background-color:#F8F8F8;color:black;">CUPRA Co-Pilot (Regenerated): {reply}</div>', unsafe_allow_html=True)
components.v1.html('<



