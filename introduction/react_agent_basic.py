from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain_community.tools import TavilySearchResults 

load_dotenv()

llm= ChatGoogleGenerativeAI(model= "gemini-1.5-pro")
search_tool= TavilySearchResults(search_depth="basic")

agent= initialize_agent(llm= llm, tools=[search_tool],agent= "zero-shot-react-description",verbose=True)

agent.invoke("wha is the today nepse price in Nepal")