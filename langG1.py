from langchain.tools import tools
from langchain.chat_models import init_chat_models
from langchain_google_genai import ChatGoogleGenerativeAI

model=model=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    # max_output_tokens,
    temperature=0.5
)
@tools 
def multiply(a:int,b:int):
    """Multiply `a` and `b`
    Args:
        a: First int
        b: Second int
    """

    return a*b;
@tools 
def add(a:int,b:int):
    """Add `a` and `b`
    Args:
        a: First int
        b: Second int
    """
    return a+b
@tools 
def divide(a:int,b:int):
    """Divide `a` and `b`
    Args:
        a: First int
        b: Second int
    """
    return a/b;
tools=[multiply,add,divide]
tools_by_name={tool.name: tool for tool in tools}
model_with_tools=model.bind_tools(tools);

#Step2: Define state
from langchain.messages import AnyMessage, ToolMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

from langchain.messages import SystemMessage

def llm_call(state:MessagesState):
    """LLM decides weather to call a tool or not"""

    return {
        "messages":[
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="you are a helpful assistant  tasked with performing arithmetic on a set of inputs."
                    )
                ]+state["messages"]
            )
        ],
        "llm_calls":state.get('llm_calls',0)+1
    }
#4 define with tools
def tool_node(state: MessagesState):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

from typing import Literal
from langgraph.graph import StateGraph, START, END


# Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END
