from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from qdrant_client import QdrantClient
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain import hub
from pydantic import BaseModel, Field
from typing import Literal
from functools import partial
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyB38nvrIt6MFrEchALd6Eouz9UHVrt9Tso"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

class MessageClassifier(BaseModel):
    message_type : Literal["emotional","logical"] = Field(
        ...,
        description = "Classify if message requeries an emotional(therapist) or logical"
    )

class State(MessagesState):
    message_type: str | None


def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    # Pass a list of messages instead of a dictionary
    response = classifier_llm.invoke([
        SystemMessage(content="""Classify the user message as either:
                          - 'emotional': if it asks for emotional support, therapy, deals with feelings or personal problems.
                          - 'logical': if it asks for facts, advice, information, logical analysis, or practical solutions.
                          """),
        HumanMessage(content=last_message.content)
    ])

    # Access the message_type attribute directly
    return {"message_type": response.message_type}

def router(state:State):
    if state["message_type"] == "emotional":
        return {"next":"therapist"}
    elif state["message_type"] == "logical":
        return {"next":"logical"}
    else:
        raise ValueError("Invalid message type")

def therapist_agent(state: State):
    last_message = state["messages"][-1]

    messages = [
        SystemMessage(content="""You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""),
        HumanMessage(content=last_message.content)
    ]

    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=response.content)]}

def logical_agent(state: State):
    last_message = state["messages"][-1]

    messages = [
        SystemMessage(content="""You are a purely logical assistant. Focus only on facts and information.
            Provide clear, concise answers based on logic and evidence.
            Do not address emotions or provide emotional support.
            Be direct and straightforward in your responses."""),
        HumanMessage(content=last_message.content)
    ]

    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=response.content)]}



def chatbot(state:State):
    return {"messages":[llm.invoke(state["messages"])]}

builder = StateGraph(State)

builder.add_node("classifier", classify_message)
builder.add_node("router", router)
builder.add_node("therapist", therapist_agent)
builder.add_node("logical", logical_agent)

builder.add_edge(START, "classifier")
builder.add_edge("classifier", "router")

builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist": "therapist", "logical": "logical"}
)

builder.add_edge("therapist", END)
builder.add_edge("logical", END)

graph = builder.compile()

def run_chatbot():
    state = {
        "messages" : [],
        "message_type": None
    }

    while True:
        user_input = input("Message: ")

        if user_input.lower() == "exit":
            print("Bye.")
            break

        state["messages"].append(HumanMessage(content=user_input))

        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print(f"Assistant: {last_message.content}")


if __name__ == "__main__":
    run_chatbot()