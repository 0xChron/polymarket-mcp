import httpx
import json

import mcp.types as types

from polymarket_mcp.config import Settings


async def get(url: str, params: dict | None = None, timeout: int | None = None):
    """Thin async GET wrapper; raises on HTTP errors."""
    settings = Settings()
    async with httpx.AsyncClient(timeout=timeout or settings.default_timeout) as client:
        resp = await client.get(url, params={k: v for k, v in (params or {}).items() if v is not None})
        resp.raise_for_status()
        return resp.json()
    
def text(data: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
 
def err(msg: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=f"Error: {msg}")]