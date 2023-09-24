import streamlit as st
import openai


def chat_with_openai(question, context):
    openai.api_key = st.secrets["openai"]["api_key"]
    model_name = "gpt-4"  # Or any other model you'd prefer
    response = openai.Completion.create(
      model=model_name,
      prompt=f"{context}\n\nUser: {question}\nBot:",
      max_tokens=150,
      temperature=0.7,
      stop=["User:", "Bot:"]
    )
    return response.choices[0].text.strip()

def app2():
    st.title("Chat with CSV Data using OpenAI")

    if "tables_dataframes" in st.session_state:
        context = Document_Chat_Creation.df_to_text(st.session_state["tables_dataframes"])

        user_question = st.text_input("Ask a question about your data:")

        if user_question:
            response = chat_with_openai(user_question, context)
            st.write(f"Bot: {response}")
    else:
        st.write("No data available. Please upload a CSV file on the home page.")


if __name__ == '__main__':
    app2()
