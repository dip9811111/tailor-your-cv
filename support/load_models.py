from langchain_openai import ChatOpenAI


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
