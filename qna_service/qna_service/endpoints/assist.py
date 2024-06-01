from fastapi import APIRouter, Body
from starlette import status

from qna_service.schemas import RAGOutput, RAGInput, RAGOutputForEval
from qna_service.utils.rag import main_chain, main_chain_for_eval
from qna_service.utils.graph import graph_app

api_router = APIRouter(tags=["Health check"])


@api_router.post(
    "/assist_legacy",
    response_model=RAGOutput,
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        query: RAGInput = Body(...),
):
    chain = main_chain.with_types(input_type=RAGInput, output_type=RAGOutput)
    return chain.invoke(input=query.dict())


@api_router.post(
    "/assist_for_eval",
    response_model=RAGOutputForEval,
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        query: RAGInput = Body(...),
):
    chain = main_chain_for_eval.with_types(input_type=RAGInput, output_type=RAGOutputForEval)
    return chain.invoke(input=query.dict())


def format_docs_for_output(docs):  # TODO: убрать отсюда
    return [doc.metadata['url'] for doc in docs]


@api_router.post(
    "/assist",
    response_model=RAGOutput,
    status_code=status.HTTP_200_OK,
)
async def get_answer(
        query: RAGInput = Body(...),
):
    question = query.query
    result = graph_app.invoke({"question": question, "remaining_transform_attempts": 3})
    return RAGOutput(text=result["generation"], links=format_docs_for_output(result["documents"]))
