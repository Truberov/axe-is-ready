from operator import itemgetter
from typing import List

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.documents import Document

from qna_service.config import get_settings
from qna_service.utils.retrievers import retriever
from .prompts import ANSWER_PROMPT, CONDENSE_QUESTION_PROMPT
from .session import create_session_factory_in_persistent_storage

settings = get_settings()

llm = ChatOllama(model='llama3:instruct', base_url=settings.LLM_BASE_URL)


def format_docs(docs: List[Document]) -> str:
    """Convert Documents to a single string.:"""
    formatted = [
        f"Article Title: {doc.metadata['title']}\nArticle Snippet: {doc.page_content}"
        for doc in docs
    ]
    return "\n\n" + "\n\n".join(formatted)


_inputs = CONDENSE_QUESTION_PROMPT | llm | StrOutputParser()

_context = {
    "context": itemgetter("human_input") | retriever | format_docs,
    "question": itemgetter("human_input"),
}

_context_with_history = {
    "context": RunnablePassthrough() | retriever | format_docs,
    "question": RunnablePassthrough(),
}

conversational_qa_chain_without_history = (
        _context | ANSWER_PROMPT | llm | StrOutputParser()
)

conversational_qa_chain = (
        _inputs | _context_with_history | ANSWER_PROMPT | llm | StrOutputParser()
)


def route_chain(_input):
    if len(_input.get('history')) > 0:
        return conversational_qa_chain
    return conversational_qa_chain_without_history


general_chain = (
    RunnableLambda(
        route_chain
    )
)

chain_with_history = RunnableWithMessageHistory(
    general_chain,
    create_session_factory_in_persistent_storage(settings.REDIS_URL),
    input_messages_key="human_input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)
