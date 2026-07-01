FROM apache/spark-py:v3.4.0

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src:/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.7-src.zip

USER root
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md .
COPY src/ ./src/

RUN uv sync --frozen

CMD ["uv", "run", "python", "-m"]
