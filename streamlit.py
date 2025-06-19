import streamlit as st
import os
from chatbot import State, graph, HumanMessage, AIMessage

os.environ["GOOGLE_API_KEY"] = "AIzaSyB38nvrIt6MFrEchALd6Eouz9UHVrt9Tso"

st.set_page_config(page_title="Therapist Chatbot", page_icon=":(", layout="centered")

if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "message_type": None
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Therapist Chatbot")
st.markdown("Type your message below. Type 'exit' to end the conversation.")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Your message:")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    if user_input.lower() == "exit":
        st.session_state.chat_history.append({"role": "assistant", "content": "Bye."})
        with st.chat_message("assistant"):
            st.markdown("Bye.")
        st.session_state.state = {
            "messages": [],
            "message_type": None
        }
        st.stop()
    
    st.session_state.state["messages"].append(HumanMessage(content=user_input))
    
    try:
        new_state = graph.invoke(st.session_state.state)
        
        st.session_state.state = new_state
        
        if new_state.get("messages") and len(new_state["messages"]) > 0:
            last_message = new_state["messages"][-1]
            if isinstance(last_message, AIMessage):
                response = last_message.content
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
