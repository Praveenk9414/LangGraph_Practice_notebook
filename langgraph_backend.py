from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph.message import add_messages   

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash'
)
     
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]         

def chat_node(state: ChatState):
    query = state['messages']
    response = model.invoke(query)
    return {
        'messages': [response]
    }

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer=checkpointer)
