import os
import json

import streamlit as st
import openai

#api key
working_dir=os.path.dirname(os.path.abspath(__file__))
with open(f"{working_dir}/config.json", "r") as f:
    config_data = json.load(f)
#deepseek/deepseek-r1: free deepseek api key with openrouter
OPEN_API_KEY=config_data["OPEN_API_KEY"]
openai.api_key=OPEN_API_KEY

#streamlit settings
st.set_page_config (
    page_title="Streamlit Chatbot",
    page_icon="💬",
    layout="centered"
)

#chat session
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

#page title
st.title("🤖 GPT-4o - ChatBot")

#chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#input feild
user_prompt=st.chat_input("Ask GPT-4o....")

if user_prompt:
    #user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    #user msg -> gpt
    response=openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]
    )

    asistant_response=response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": asistant_response})

    #display response
    with st.chat_message("assistant"):
        st.markdown(asistant_response)