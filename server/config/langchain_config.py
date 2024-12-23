from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks import StdOutCallbackHandler
from langsmith.run_helpers import traceable
from langsmith.client import Client
from langchain.callbacks.manager import CallbackManager
import os


def setup_llm():
    """Configura o modelo de linguagem base"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")

    callback_manager = get_callback_manager()

    return ChatGoogleGenerativeAI(
        temperature=float(os.getenv("LLM_TEMPERATURE", 0)),
        model="gemini-pro",
        google_api_key=google_api_key,
        convert_system_message_to_human=True,
        callbacks=[StdOutCallbackHandler()],
        callback_manager=callback_manager,
    )


def setup_embeddings():
    """Configura o modelo de embeddings"""
    from ..langchain_components.embeddings import CachedEmbeddings

    return CachedEmbeddings()


def setup_retriever(embeddings, supabase_client):
    """Configura o retriever personalizado"""
    from ..langchain_components.retriever import CustomRetriever

    return CustomRetriever(embeddings, supabase_client)


def setup_document_processor():
    """Configura o processador de documentos"""
    from ..langchain_components.document_processor import DocumentProcessor

    return DocumentProcessor()


def setup_note_processing():
    """Configura a chain de processamento de notas"""
    from ..langchain_components.chains import NoteProcessingChain

    return NoteProcessingChain()


def setup_langchain_tracing():
    """Configura o tracing do LangChain com LangSmith"""
    if os.getenv("LANGCHAIN_TRACING_V2") == "true":
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "keepai")
        client = Client(
            api_url=os.getenv("LANGCHAIN_ENDPOINT"),
            api_key=os.getenv("LANGCHAIN_API_KEY"),
        )
        return client
    return None


def get_callback_manager():
    client = setup_langchain_tracing()
    return CallbackManager([StdOutCallbackHandler()])
