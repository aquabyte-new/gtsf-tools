FROM ghcr.io/astral-sh/uv:python3.8-bookworm-slim AS base

ADD pyproject.toml .
RUN uv sync --no-dev

ADD demo.py .
ADD main.py .

ENTRYPOINT ["uv"]