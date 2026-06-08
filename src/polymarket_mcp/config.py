from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gamma_url: str = "https://gamma-api.polymarket.com"
    data_url: str = "https://data-api.polymarket.com"
    default_timeout: int = 15