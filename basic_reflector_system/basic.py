from typing import List, Sequence#this is for type checking
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain,reflection_chain
load_dotenv() 
graph= MessageGraph()
REFLECT= "reflect"
GENERATE= "generate"

def generate_node(state):
    return generation_chain.invoke({
        "messages":state
    })

def reflect_node(state):
    return reflection_chain.invoke({
        "messages":state
    })

graph.add_node(GENERATE,generate_node)
graph.add_node(REFLECT,reflect_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    if len(state)>4:
        return END
    return REFLECT
graph.add_conditional_edges(GENERATE,should_continue)
graph.add_edge(REFLECT,GENERATE)

app= graph.compile()
response= app.invoke(HumanMessage(content= "AI bot for facebook post"))
# #print(app.get_graph().draw_mermaid())
# print(app.get_graph().draw_ascii())


