from typing import TypedDict, Annotated
import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

# Robustly find and load .env from current or parent directories
load_dotenv(find_dotenv())

# Initialize Groq LLM with a valid model ID
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5
)

# Define chat state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Define chatbot node
def chat_bot(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": [response]
    }

# Build graph
graph_builder = StateGraph(ChatState)
graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

# Add checkpointer and compile
checkpointer = InMemorySaver()
chatbot = graph_builder.compile(checkpointer=checkpointer)
