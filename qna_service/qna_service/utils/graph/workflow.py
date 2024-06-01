from langgraph.graph import END, StateGraph

from .state import (
    GraphState, retrieve,
    grade_documents, generate,
    transform_query, decide_to_generate,
    grade_generation_v_documents_and_question,
)

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)
workflow.add_node("no_answer", lambda state: {"generation": "Я не знаю."})  # transform_query

# Build graph
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
        "no attempts left": "no_answer"
    },
)
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "no attempts left": "no_answer",
        "not useful": "transform_query",
    },
)
workflow.set_finish_point("no_answer")
