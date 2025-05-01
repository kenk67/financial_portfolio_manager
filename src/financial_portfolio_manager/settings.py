from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using Pydantic."""

    DATA_PROVIDER_URL: dict[str, str] = Field(
        default={
            "ALPHA_VANTAGE": "https://www.alphavantage.co/query",
        },
        description="Mapping of data provider types to their class names",
    )


class AuthSettings(BaseSettings):
    """Authentication settings using Pydantic."""

    ALPHA_VANTAGE_API_KEY: str = Field(
        default="dummy",
        description="API key for Alpha Vantage Financial Data Provider",
    )
    GEMINI_API_KEY: str = Field(
        default="dummy",
        description="API key for Gemini LLM Provider",
    )


def get_settings():
    return Settings()
