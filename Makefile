run:
	uv run src/polymarket_mcp/server.py

inspector:
	npx -y @modelcontextprotocol/inspector

build:
	docker build -t polymarket-mcp .

start:
	docker run --rm -p 8000:8000 polymarket-mcp