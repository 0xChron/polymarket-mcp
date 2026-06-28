FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md /app/
COPY src/ /app/src/

RUN pip install uv
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "--frozen", "polymarket-mcp"]