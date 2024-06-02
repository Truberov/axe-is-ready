from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from qna_service.config import get_settings

settings = get_settings()

embedding_function = SentenceTransformerEmbeddings(model_name="BAAI/bge-m3")

vectorstore = Chroma(
    collection_name="total",
    embedding_function=embedding_function,
    persist_directory=settings.CHROMA_BASE_DIR
)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 100})
compressor = CohereRerank(top_n=10, cohere_api_key=settings.COHERE_API_KEY)
retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=base_retriever
)
