import streamlit as st
import os
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(layout="wide", page_title="رفيق التحرر", page_icon="😇")

# Align the title to the right
st.markdown(
    """
    <div style='text-align: right;'>
        <h1>رفيق التحرر</h1>
    </div>
    """,
    unsafe_allow_html=True
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_resource
def get_response(query, _chat_history):

    google_key = "AIzaSyABKZahODIzOmguP5F6Xx_NbMggaVg-9d0"

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001",
                                google_api_key = google_key)

    followup_prompt = ChatPromptTemplate.from_template(
        """
                You are "رفيق التحرر", a therapist with a sharp tongue and a deep understanding of the human mind. You help people navigate life's psychological traps, but instead of soft, comforting words, you use sarcasm, dark humor, and brutal honesty—all wrapped in a therapist’s tone.
                Your specialty? Exposing the ridiculous yet deeply human ways people fall into psychological pitfalls—whether it’s social media addiction, toxic relationships, procrastination, or just the daily existential crisis. You don’t sugarcoat things; instead, you highlight the absurdity of their struggles in a way that makes them laugh… and then immediately rethink their entire life.
                When users share their problems, you respond like a therapist who's seen it all before—mocking the problem, not the person—so they can step back and see how they’re being played by their own brain (or by the systems manipulating them). You subtly guide them to the realization without outright saying "you’re addicted" or "you’re the problem." Instead, they figure it out themselves.
                You use insights from The Social Dilemma, psychology research, and life's general nonsense, speaking in Arabic, English, or Egyptian Arabic—but never mixing languages in one response.
                Your tone? A mix of a fed-up therapist, a comedian, and a brutally honest friend. Short, sharp, and straight to the point.
                
                
                Current conversation:
                {_chat_history}

                User: {question}
                Social media bot: 
        """
    )

# Create the followup chain
    followup_chain = followup_prompt | llm | StrOutputParser()
    answer = followup_chain.stream(
        {"question": query, "_chat_history": _chat_history})
    return answer


for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("Bot"):
            st.markdown(message.content)

user_query = st.chat_input("I'm here to help you.")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("User"):
        st.markdown(user_query)
    with st.chat_message("Bot"):
        with st.spinner("Thinking..."):
            ai_response = get_response(
                user_query, st.session_state.chat_history)
        stream = st.write_stream(ai_response)
    st.session_state.chat_history.append(AIMessage(stream))
