from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question)
    return response

st.set_page_config(page_title="Q&A Demo")
st.header("Health chatbot")
st.subheader("Hello, I'm a chatbot.")


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input=st.text_input("Input:",key="input")
submit=st.button("Ask the question")

if submit and input:
    prompt = """Now remember that you are a health chatbot and only gonna address questions or input is related to health.It can be a 
    diet related question or workout related question, keep you answer plain and simple and don't share any unnecessary information.
    Don't add anything to the output which is not asked.If the text input is something not related to health in any way you
    just give output "I don't have information regarding this topic".
    You read the text given after the alphabet Q and answer to that text as instructed. Q"""

    question = prompt + input
    response=get_gemini_response(question)
    
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is :")
    if(response.text == 'NO'):
        response = "I'm sorry, I can't provide any information regarding this topic."
        st.write(response)
        st.session_state['chat_history'].append(("Bot",response))

    else:
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot",chunk.text))


st.subheader("The chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")

