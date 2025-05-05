import streamlit as st
from .chatbot import run_chatbot

def main():
    st.title("Therapy Chatbot")
    st.write("Welcome to the Therapy Chatbot. Please enter your message below.")

    user_input = st.text_input("Your Message:", "")

    if st.button("Send"):
        if user_input:
            response = run_chatbot(user_input)
            st.text_area("Assistant:", value=response, height=300, max_chars=None, key=None)
        else:
            st.warning("Please enter a message before sending.")

if __name__ == "__main__":
    main()