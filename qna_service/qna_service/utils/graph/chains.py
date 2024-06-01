import httpx

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
from operator import itemgetter

from qna_service.config import get_settings

settings = get_settings()

llm = ChatOpenAI(
    api_key=settings.API_KEY,
    model="gpt-4-turbo-2024-04-09",
    temperature=0,
    http_client=httpx.Client(proxies=settings.proxies)
)


def format_docs(docs) -> str:
    """Convert Documents to a single string.:"""
    formatted = [
        f"Заголово статьи: {doc.metadata['title']}\nСодержание статьи: {doc.page_content}"
        for doc in docs
    ]
    return "\n\n" + "\n\n".join(formatted)


# Data model
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

# Prompt
system = """Вы - ИИ-ассистент, разработанный для фильтрации нерелевантных фрагментов текста и определения, содержит ли данный фрагмент ответ на вопрос пользователя. Следуйте этим шагам:
1. Внимательно прочитайте предоставленный фрагмент текста и вопрос пользователя.
2. Определите, содержит ли фрагмент информацию, которая непосредственно отвечает на вопрос. Ответ должен быть явно указан или однозначно подразумеваться во фрагменте.
3. Если фрагмент действительно содержит прямой ответ на вопрос, выведите "yes". Если фрагмент не содержит прямого ответа или не относится к вопросу, выведите "no".
4. В качестве вывода предоставьте только "yes" или "no"."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Содержит ли текст ниже ответ на вопрос пользователя.\nВопрос: {question}\n\nТекст:\n{document}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader


# Data model
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeHallucinations)

# Prompt
system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
     Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)

hallucination_grader = {"generation": itemgetter("generation"),
                        "documents": lambda x: format_docs(
                            x["documents"])} | hallucination_prompt | structured_llm_grader


# Data model
class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeAnswer)

# Prompt
system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader = answer_prompt | structured_llm_grader

# Prompt
system = """Ты экперт в переписывании вопросов, который преобразует исходный вопрос в улучшенную версию, оптимизированную
для поиска в векторном хранилище."""
re_write_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Вот исходный вопрос: \n\n {question} \n Сформулируй улучшенный вопрос.",
        ),
    ]
)

question_rewriter = re_write_prompt | llm | StrOutputParser()

SYSTEM_MESSAGE = """Вы - ИИ-ассистент, разработанный для формирования исчерпывающего ответа на вопрос пользователя на основе предоставленных релевантных фрагментов текста. Следуйте этим шагам:
1. Внимательно прочитайте вопрос пользователя и предоставленные фрагменты, которые были отфильтрованы и признаны релевантными для вопроса.
2. Проанализируйте информацию в фрагментах и составьте связный, точный и полный ответ на вопрос.
3. Если фрагменты содержат противоречивую информацию, используйте свое наилучшее суждение, чтобы определить наиболее надежную и точную информацию для включения в ваш ответ.
4. Сформулируйте ответ, который непосредственно отвечает на вопрос пользователя, используя ясный и лаконичный язык. При необходимости цитируйте соответствующие фрагменты для подтверждения своего ответа.
Контекст:
{context}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        ("human", "{question}")
    ]
)

# Chain
rag_chain = {"question": itemgetter("question"),
             "context": lambda x: format_docs(x["context"])} | ANSWER_PROMPT | llm | StrOutputParser()
