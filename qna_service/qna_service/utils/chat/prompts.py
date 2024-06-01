from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

_TEMPLATE = """Учитывая диалог и последний вопрос, перефразируй
последний вопрос в отдельный вопрос.

Последний вопрос: {human_input}

В ответ напиши только перефразированный вопрос и ничего более
Отдельный вопрос:"""

CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", _TEMPLATE),
    ]
)

SYSTEM_MESSAGE = """Ты очень умный ассистент клиентов Тинькофф Бизнес, ответь на вопрос пользователя используя приведенный контекст
Контекст:
{context}
Помни, что твоя задача быть максимально полезным, тебе нужно сделать все возможное, чтобы удержать клиента. Отвечай на русском языке.
"""
ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        ("human", "{question}")
    ]
)
