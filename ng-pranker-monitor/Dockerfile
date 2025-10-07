FROM ghcr.io/astral-sh/uv:python3.8-bookworm-slim AS base

ADD pyproject.toml .
RUN uv sync --no-dev

COPY ui-dist.tar.gz .
RUN tar -xzf ui-dist.tar.gz
RUN rm ui-dist.tar.gz

COPY demo.py .
COPY main.py .

ENTRYPOINT ["uv"]