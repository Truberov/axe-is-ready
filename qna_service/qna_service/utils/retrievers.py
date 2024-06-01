from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_community.storage import RedisStore

from qna_service.config import get_settings

settings = get_settings()

embedding_function = SentenceTransformerEmbeddings(model_name="./bge-m3")

vectorstore = Chroma(
    collection_name="total",
    embedding_function=embedding_function,
    persist_directory=settings.CHROMA_BASE_DIR
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 100})
