
import streamlit as st
import uuid

from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("AI Chatbot")
st.caption("Powered by LangGraph and Groq")

# -------------------------------
# Initialize Session State
# -------------------------------

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())


# -------------------------------
# Display Previous Messages
# -------------------------------

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------------
# Chat Input
# -------------------------------

user_input = st.chat_input("Type your message here...")

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    # Invoke LangGraph Backend
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                config = {
                    "configurable": {
                        "thread_id": st.session_state["thread_id"]
                    }
                }

                response = chatbot.invoke(
                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    },
                    config=config
                )

                # Extract AI response
                ai_response = response["messages"][-1].content

                st.markdown(ai_response)

                # Save AI response
                st.session_state["message_history"].append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
