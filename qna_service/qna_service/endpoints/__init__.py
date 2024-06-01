from .health_check import api_router as health_check_router
from .chat import rag_config
from .assist import api_router as assist_router

list_of_routes = [
    health_check_router,
    assist_router,
]

list_of_config_routes = [
    rag_config,
]

__all__ = [
    "list_of_routes",
    "list_of_config_routes",
]
