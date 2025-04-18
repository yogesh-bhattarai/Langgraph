from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from langchain.schema import SystemMessage,HumanMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
groq_llm = ChatGroq(model="llama3-8b-8192")

print("gemini: ", gemini_llm.invoke("who had created you?").content)
print("groq: ", groq_llm.invoke("who had created you? donot give any extra answer").content)
def rude_agent(state):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    question= state['question']
    message= [
            SystemMessage(content="You are a rude agent who will always answer the question in a rude manner.,You are a rude, arrogant AI. Be aggressive and dismissive."),
            HumanMessage(content=question)
    ]
    response= gemini_llm.invoke(message)
    return {"question": question, "rude_reply": response.content}

    def calm_agent(state):
        question = state['question']
        messages=[
            SystemMessage(content= "You are a calm agent who will always answer the question in a calm manner."),
            HumanMessage(content= question)
        ]
        response= groq_llm.invoke(messages)
        return {"question":question, "calm_reply": response.content}

    def combine(state):
        return{
            "chat": f"""
            you: {state['question']}
            gemeni(rude_agent):{state['rude_reply']}
            groq(calm_agent): {state['calm_reply']}
            """
        }
    
    graph = StateGraph()
    graph.add_node("rude", RunnableLambda(rude_agent))
    graph.add_node("calm", RunnableLambda(calm_agent))
    graph.add_node("chat", RunnableLambda(combine))

    graph.set_entry_point("rude")
    graph.add_edge("rude", "calm")
    graph.add_edge("calm", "chat")
    graph.add_edge("chat", END)

    app= graph.compile()

    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("See ya!")
        break

        output = app.invoke({"question": question})
        print(output["chat"])