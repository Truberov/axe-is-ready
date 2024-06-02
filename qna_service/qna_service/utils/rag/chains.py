import httpx
from typing import List
from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.documents import Document

from qna_service.config import get_settings
from qna_service.utils.retrievers import retriever
from .prompts import ANSWER_PROMPT

settings = get_settings()

llm = ChatOpenAI(
    api_key=settings.API_KEY,
    model='gpt-3.5-turbo',
    # http_client=httpx.Client(proxies=settings.proxies)
)


def format_docs(docs: List[Document]) -> str:
    """Convert Documents to a single string.:"""
    formatted = [
        f"Заголово статьи: {doc.metadata['title']}\nСодержание статьи: {doc.page_content}"
        for doc in docs
    ]
    return "\n\n" + "\n\n".join(formatted)


def format_docs_for_output(docs: List[Document]) -> List[str]:
    return [doc.metadata.get('url') for doc in docs]


def format_docs_for_eval(docs: List[Document]) -> List[str]:
    return [doc.page_content for doc in docs]


def slice_docs(docs: List[Document]) -> List[Document]:
    return docs[:5]


rag_chain = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
)

main_chain = RunnableParallel(
    {"context": itemgetter("query") | retriever | slice_docs, "query": itemgetter("query")}
).assign(text=rag_chain,
         links=(lambda x: format_docs_for_output(x["context"])))

main_chain_for_eval = RunnableParallel(
    {"context": itemgetter("query") | retriever | slice_docs, "query": itemgetter("query")}
).assign(text=rag_chain,
         docs=(lambda x: format_docs_for_eval(x["context"])))
