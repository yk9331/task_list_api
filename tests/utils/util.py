from src.core.config import settings


def get_versioned_endpoint(endpoint: str, version: str = settings.API_VERSION) -> str:
    endpoint = endpoint.lstrip("/")
    return f"/{version}/{endpoint}"
