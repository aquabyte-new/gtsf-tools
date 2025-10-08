FROM ghcr.io/astral-sh/uv:python3.8-bookworm-slim AS base

WORKDIR /app
ADD pyproject.toml .
RUN uv sync --no-dev

WORKDIR /www
COPY ui.tar.gz .
RUN tar -xzf ui.tar.gz && rm ui.tar.gz

WORKDIR /app
COPY demo.py .
COPY main.py .

ENTRYPOINT ["/bin/bash", "-c"]