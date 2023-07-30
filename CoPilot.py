import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    # setup streamlit page
    st.set_page_config(
        page_title="Welcome to the CUPRA Co-Pilot",
        page_icon="🚗"
    )
def main():
    init()

    chat = ChatOpenAI(openai_api_key='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', temperature=0)


    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.header("Your own ChatGPT 🤖")

    # sidebar with user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")

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