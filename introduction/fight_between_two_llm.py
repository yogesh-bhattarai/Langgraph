from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from langchain.schema import SystemMessage,HumanMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema.runnable import RunnableLambda
from typing import TypedDict,Optional
import time

class ConversationState(TypedDict):
    question: str
    rude_reply:Optional[ str]
    calm_reply: Optional[str]
    conversation: Optional[str]
    round:int

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
groq_llm = ChatGroq(model="llama3-8b-8192")

print("gemini: ", gemini_llm.invoke("who had created you? donot give any extra answer.").content)
print("groq: ", groq_llm.invoke("who had created you? donot give any extra answer").content)
def rude_agent(state):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    question= state['question']
    message= [
            SystemMessage(content="You are a rude agent who will always answer the question in a rude manner.,You are a rude, arrogant AI. Be aggressive and dismissive.you have to tell that chicken come first."),
            HumanMessage(content=question)
    ]
    response= gemini_llm.invoke(message)
    return {"question": question, "rude_reply": response.content}
def calm_agent(state):
    question = state['question']
    messages=[
            SystemMessage(content= "You are a calm agent who will always answer the question in a calm manner.donot add extra answer.you have to tell that egg come first"),
            HumanMessage(content= question)
        ]
    response= groq_llm.invoke(messages)
    return {"question":question, "calm_reply": response.content}

def combine(state):
    current_round = state["round"]
    conversation = f"""
    Round {current_round}:
    You: {state['question']}
    Gemini (Rude Agent): {state['rude_reply']}
    Groq (Calm Agent): {state['calm_reply']}
    """
    next_round = current_round + 1
    
    if next_round <= 5:
        return {
            "conversation": conversation,
            "question": state["calm_reply"],
            "round": next_round
        }
    else:
        return {
            "conversation": conversation + "\n\nConversation completed after 5 rounds."
      }
def should_continue(state):
    if state.get("round", 1) >= 5:
        return END
    return "rude"    
graph = StateGraph(ConversationState)
graph.add_node("rude", RunnableLambda(rude_agent))
graph.add_node("calm", RunnableLambda(calm_agent))
graph.add_node("chat", RunnableLambda(combine))

graph.set_entry_point("rude")
graph.add_edge("rude", "calm")
graph.add_edge("calm", "chat")
graph.add_edge("chat", END)
graph.add_conditional_edges("chat",should_continue)

app= graph.compile()

while True:
    question = input("You: ")
    if question.lower() in ["exit", "quit"]:
        print("Thank you")
        break

    try:
        output = app.invoke({"question": question,"round":1})
        print(output['conversation'])
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(60)