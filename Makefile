run:
	uv run --frozen polymarket-mcp

test:
	uv run --frozen pytest

inspector:
	npx -y @modelcontextprotocol/inspector

build:
	docker build -t polymarket-mcp .

start:
	docker run --rm -p 8000:8000 polymarket-mcp