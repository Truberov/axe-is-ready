from typing import List, Tuple

from langserve.pydantic_v1 import BaseModel, Field


class RAGInput(BaseModel):
    """Input for the assist endpoint."""

    query: str


class RAGOutput(BaseModel):
    """Output for the assist endpoint."""

    text: str
    links: List[str]


class RAGOutputForEval(BaseModel):
    """Output for the assist endpoint."""

    text: str
    docs: List[str]
