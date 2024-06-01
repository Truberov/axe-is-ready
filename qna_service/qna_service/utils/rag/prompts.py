from langchain_core.prompts import ChatPromptTemplate


SYSTEM_MESSAGE = """Ты очень умный ассистент клиентов Тинькофф Бизнес, ответь на вопрос пользователя используя приведенный контекст
Контекст:
{context}
Помни, что твоя задача быть максимально полезным.
Если в контексте нет ответа на вопрос, ответь я не знаю.
"""

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        ("human", "{query}")
    ]
)
