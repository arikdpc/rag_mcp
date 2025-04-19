from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings import OpenAIEmbeddings
from config import settings
from supabase import create_client

def init_retriever():
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)
    return SupabaseVectorStore(
        client=supabase,
        table_name="documents",
        embedding=embeddings
    ).as_retriever()
