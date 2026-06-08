import httpx
import json

import mcp.types as types

async def get(url: str, params: dict | None = None):
    """Thin async GET wrapper; raises on HTTP errors."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params={k: v for k, v in (params or {}).items() if v is not None})
        resp.raise_for_status()
        return resp.json()
    
def text(data: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
 
def err(msg: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=f"Error: {msg}")]