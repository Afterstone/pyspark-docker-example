FROM debian:13.5-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN : \
    && apt-get update \
    && JRE_VERSION=$(apt-cache madison openjdk-21-jre-headless | { head -n1; cat >/dev/null; } | awk '{print $3}') \
    && apt-get install -y --no-install-recommends \
        "openjdk-21-jre-headless=${JRE_VERSION}" \
    && rm -rf /var/lib/apt/lists/* \
    :

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev --frozen

COPY src /app/src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

ENV JAVA_HOME=/usr/lib/jvm/java-1.21.0-openjdk-amd64
ENV PATH="/app/.venv/bin:${JAVA_HOME}/bin:${PATH}"
