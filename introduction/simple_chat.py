from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from typing import TypedDict
load_dotenv()

class chatState(TypedDict):
    messages:list
def get_user_input(state:chatState)-> chatState:
    user_input= input("Enter you query:")
    state['messages'].append({"role":"user","content": user_input})
    return state
llm= ChatGoogleGenerativeAI(model= "gemini-1.5-pro")

def llm_response(state:chatState)-> chatState:
    if state['messages'][-1]['content'].lower().strip()=="exit":
        return state
    response= llm.invoke(state['messages'])
    state['messages'].append({"role":"assistant","content":response.content})
    print("assistant: ", response.content)

def check_exit(state:chatState)->str:
    if state['messages'][-1]['content'].lower().strip()=="exit":
        return END
    else:
        return "user_input"

graph = StateGraph(chatState)
graph.add_node("user_input",get_user_input)
graph.add_node("llm_response",llm_response)

graph.set_entry_point("user_input")
graph.add_edge("user_input","llm_response")
graph.add_conditional_edges("llm_response",check_exit)
#graph.add_exit_condition("EXIT")

chatbot= graph.compile()
chatbot.invoke({"messages":[]})
