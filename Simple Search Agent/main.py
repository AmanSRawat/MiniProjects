from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="Gemma 4 26B", temperature=0.7)

response = model.invoke(
    "What is langgraph and how can it be used in Python?"
)

print(response.text)