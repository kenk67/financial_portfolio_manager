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


def get_settings():
    return Settings()
