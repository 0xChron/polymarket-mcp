from polymarket_mcp.config import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.gamma_url == "https://gamma-api.polymarket.com"
    assert settings.data_url == "https://data-api.polymarket.com"
    assert settings.default_timeout == 15
