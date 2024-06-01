import re
from pathlib import Path
from typing import Union, Callable

from fastapi import HTTPException
from langchain_community.chat_message_histories import FileChatMessageHistory, RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


def _is_valid_identifier(value: str) -> bool:
    """Check if the session ID is in a valid format."""
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))


def create_session_factory_in_local_filesystem(
        base_dir: Union[str, Path],
) -> Callable[[str], BaseChatMessageHistory]:
    """Create a session ID factory that creates session IDs from a base dir.

    Args:
        base_dir: Base directory to use for storing the chat histories.

    Returns:
        A session ID factory that creates session IDs from a base path.
    """
    base_dir_ = Path(base_dir) if isinstance(base_dir, str) else base_dir
    if not base_dir_.exists():
        base_dir_.mkdir(parents=True)

    def get_chat_history(session_id: str) -> FileChatMessageHistory:
        """Get a chat history from a session ID."""
        if not _is_valid_identifier(session_id):
            raise HTTPException(
                status_code=400,
                detail=f"Session ID `{session_id}` is not in a valid format. "
                       "Session ID must only contain alphanumeric characters, "
                       "hyphens, and underscores.",
            )
        file_path = base_dir_ / f"{session_id}.json"
        return FileChatMessageHistory(str(file_path))

    return get_chat_history


def create_session_factory_in_persistent_storage(
        redis_url: str,
) -> Callable[[str, str], BaseChatMessageHistory]:
    def get_chat_history(user_id: str, conversation_id: str) -> RedisChatMessageHistory:
        if not _is_valid_identifier(user_id):
            raise ValueError(
                f"User ID {user_id} is not in a valid format. "
                "User ID must only contain alphanumeric characters, "
                "hyphens, and underscores."
                "Please include a valid cookie in the request headers called 'user-id'."
            )
        if not _is_valid_identifier(conversation_id):
            raise ValueError(
                f"Conversation ID {conversation_id} is not in a valid format. "
                "Conversation ID must only contain alphanumeric characters, "
                "hyphens, and underscores. Please provide a valid conversation id "
            )

        session_id = f"{user_id}_{conversation_id}"
        return RedisChatMessageHistory(session_id, url=redis_url)

    return get_chat_history
