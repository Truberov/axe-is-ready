from os import environ


class DefaultSettings:
    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))
    LLM_BASE_URL: str = environ.get("LLM_BASE_URL", 'http://0.0.0.0:11434')
    REDIS_URL: str = environ.get("REDIS_URL", 'redis://0.0.0.0:6379')
    CHROMA_BASE_DIR: str = environ.get("CHROMA_BASE_DIR", "./chroma_data")
    API_KEY: str = environ.get("API_KEY")
    PROXY: dict = environ.get("PROXY")

    @property
    def proxies(self) -> dict:
        return {
            "http://": self.PROXY,
            "https://": self.PROXY,
        }
