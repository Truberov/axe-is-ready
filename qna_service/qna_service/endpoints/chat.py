from typing import Dict, Any

from fastapi import Request, HTTPException

from qna_service.utils.chat import chain_with_history
from qna_service.schemas import InputChat


def _per_request_config_modifier(
        config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    """Update the config"""
    config = config.copy()
    configurable = config.get("configurable", {})
    # Look for a cookie named "user_id"
    user_id = request.cookies.get("user_id", None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="No user id found. Please set a cookie named 'user_id'.",
        )

    configurable["user_id"] = user_id
    config["configurable"] = configurable
    return config


rag_config = {
    "runnable": chain_with_history.with_types(input_type=InputChat),
    "path": "/chat",
    "enable_feedback_endpoint": True,
    # "per_req_config_modifier": _per_request_config_modifier,
    # "disabled_endpoints": ["playground", "batch"]
}
