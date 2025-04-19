from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from retriever import init_retriever
from config import settings

def build_chain():
    retriever = init_retriever()
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.GPT_MODEL,
    )
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
