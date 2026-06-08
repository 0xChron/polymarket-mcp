FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/
COPY src/ /app/src/

ENV PYTHONPATH="/app/src"

RUN pip install uv
RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "src/polymarket_mcp/server.py"]