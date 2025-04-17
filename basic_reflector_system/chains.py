from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
generation_prompts= ChatPromptTemplate.from_messages([
    ("system",
    "you are a facebook AI bot tasked with excellent facebook posts"
    "Generate the facebook post possible for the user's request"
    "If the user's provide Critique ,respond with a polite and professional critique of their post",
),
MessagesPlaceholder(variable_name="messages")
])
reflection_prompts= ChatPromptTemplate.from_messages([
("system",
"you are a facebook AI bot tasked with excellent facebook posts"
"Generate the facebook post possible for the user's request"
"Always provide detailed recommendation ,including requests for lenght,virality, sytle etc",
),
MessagesPlaceholder(variable_name="messages"),
])

llm= ChatGoogleGenerativeAI(model="gemini-1.5-pro")

generation_chain = generation_prompts|llm
reflection_chain= reflection_prompts|llm