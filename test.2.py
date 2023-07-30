import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    # Load the OpenAI API key from the environment variable
    openai.api_key = st.secrets["openai"]["api_key"]


    # setup streamlit page
    st.set_page_config(
        page_title="Welcome to the CUPRA Co-Pilot",
        page_icon="🤖"
    )

def main():
    init()

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are designed to create marketing content for CUPRA. There is a focus on fleet decision makers at corporation as this is for B2B marketing via email and social media.")
        ]

    st.header("Welcome to the CUPRA Co-Pilot 🤖")

    # User input at the bottom of the page
    user_input = st.chat_input("Your message: ", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(
            AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')

if __name__ == '__main__':
    main()
