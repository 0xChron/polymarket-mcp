import json

import httpx
import pytest
import respx

from polymarket_mcp.utils.helpers import err, get, text


def test_text_wraps_markdown_in_json() -> None:
    result = text("# Hello")
    assert len(result) == 1
    assert result[0].type == "text"
    assert json.loads(result[0].text) == "# Hello"


def test_err_prefixes_message() -> None:
    result = err("something failed")
    assert result[0].text == "Error: something failed"


@respx.mock
@pytest.mark.asyncio
async def test_get_filters_none_params() -> None:
    route = respx.get("https://example.com/search").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    await get("https://example.com/search", params={"q": "btc", "status": None})

    assert route.called
    assert route.calls[0].request.url.params["q"] == "btc"
    assert "status" not in route.calls[0].request.url.params


@respx.mock
@pytest.mark.asyncio
async def test_get_uses_settings_timeout() -> None:
    respx.get("https://example.com/data").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    result = await get("https://example.com/data", timeout=30)
    assert result == {"ok": True}
