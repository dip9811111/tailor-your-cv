from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def load_openAI_model():
    MODEL = ChatOpenAI(
        model="gpt-4.1",
        temperature=0,
        top_p=0,
        max_tokens=None,
        timeout=None,
        max_retries=1,
        seed=42,
    )

    return MODEL

def load_gemini_model():
    MODEL = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        top_p=0,
        max_tokens=None,
        timeout=None,
        max_retries=1,
        seed=42,
    )

    return MODEL

