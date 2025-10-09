FROM ghcr.io/astral-sh/uv:python3.8-bookworm-slim AS base

# Intall miniserve: https://github.com/svenstaro/miniserve
ARG MINISERVE_VERSION=0.32.0
ARG MINISERVE_RELEASES=https://github.com/svenstaro/miniserve/releases
ARG MINISERVE_URL=${MINISERVE_RELEASES}/download/v${MINISERVE_VERSION}/miniserve-${MINISERVE_VERSION}-aarch64-unknown-linux-gnu
ADD $MINISERVE_URL /usr/local/bin/miniserve
RUN chmod +x /usr/local/bin/miniserve

# Install python packages.
WORKDIR /app
ADD pyproject.toml .
RUN uv sync --no-dev

# Add the UI.
WORKDIR /www
COPY ui.tar.gz .
RUN tar -xzf ui.tar.gz && rm ui.tar.gz

# Add the app.
WORKDIR /app
COPY demo.py .
COPY main.py .
COPY run.sh .

ENTRYPOINT ["/bin/bash", "-c"]