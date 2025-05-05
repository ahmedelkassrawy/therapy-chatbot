from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

# Import the existing chatbot logic
from chatbot import run_chatbot

def main():
    st.title("Therapy Chatbot")
    st.write("Welcome to the Therapy Chatbot. Please enter your message below.")

    # Initialize session state for messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # User input
    user_input = st.text_input("Your message:", "")

    if st.button("Send"):
        if user_input:
            # Append user message to session state
            st.session_state.messages.append(HumanMessage(content=user_input))

            # Run the chatbot logic
            state = {
                "messages": st.session_state.messages,
                "message_type": None
            }
            state = run_chatbot(state)

            # Display the assistant's response
            if state.get("messages") and len(state["messages"]) > 0:
                last_message = state["messages"][-1]
                st.session_state.messages.append(AIMessage(content=last_message.content))

    # Display all messages
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            st.write(f"You: {message.content}")
        elif isinstance(message, AIMessage):
            st.write(f"Assistant: {message.content}")

if __name__ == "__main__":
    main()