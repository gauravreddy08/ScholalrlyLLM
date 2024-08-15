from LLM import LLM
import streamlit as st
from prompts import systemPrompt

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    with open('AUTHOR.txt', 'r') as file:
        name = file.read()
    st.session_state.name = name
    systemPrompt = systemPrompt.format(name=st.session_state.name)
    st.session_state.llm = LLM(system=systemPrompt)


st.title(f"{st.session_state.name}'s Research Chatbot")
st.markdown("###### Made by Gaurav")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})    

    response = st.session_state.llm.call(prompt)

    if isinstance(response, str):
        with st.chat_message("assistant"):
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})




