FROM eclipse-temurin:17-jre-jammy

ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON=3.10

COPY pyproject.toml uv.lock README.md /app/
RUN uv sync --no-install-project --no-dev

COPY src /app/src
RUN uv sync --no-dev

