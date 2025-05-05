import streamlit as st
import os
from chatbot import State, graph, HumanMessage, AIMessage  # Import from chatbot.py

# Set Google API key (same as in chatbot.py)
os.environ["GOOGLE_API_KEY"] = "AIzaSyB38nvrIt6MFrEchALd6Eouz9UHVrt9Tso"

# Streamlit page configuration
st.set_page_config(page_title="Therapist (RAFQ FM)", page_icon=":(", layout="centered")

# Initialize session state for chat history and state
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "message_type": None
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.title("Therapist (RAFQ FM)")
st.markdown("Type your message below. Type 'exit' to end the conversation.")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user message
user_input = st.chat_input("Your message:")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Check for exit command
    if user_input.lower() == "exit":
        st.session_state.chat_history.append({"role": "assistant", "content": "Bye."})
        with st.chat_message("assistant"):
            st.markdown("Bye.")
        st.session_state.state = {
            "messages": [],
            "message_type": None
        }  # Reset state
        st.stop()
    
    # Update state with user message
    st.session_state.state["messages"].append(HumanMessage(content=user_input))
    
    # Invoke the chatbot graph
    try:
        new_state = graph.invoke(st.session_state.state)
        
        # Update state
        st.session_state.state = new_state
        
        # Get and display assistant response
        if new_state.get("messages") and len(new_state["messages"]) > 0:
            last_message = new_state["messages"][-1]
            if isinstance(last_message, AIMessage):
                response = last_message.content
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")