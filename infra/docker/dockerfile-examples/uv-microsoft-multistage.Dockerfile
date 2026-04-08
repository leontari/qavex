# https://devblogs.microsoft.com/ise/dockerizing-uv/
# Use a Python image with uv pre-installed
FROM mcr.microsoft.com/cbl-mariner/base/python:3 AS base

# Makes installation faster
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/usr/app/.venv/bin:$PATH"

# Set the working directory
WORKDIR /usr/app
COPY . .
RUN ls -la

# Install necessary build tools for compiling dependencies
RUN bash scripts/setup/Dockerfile/base.ba.sh

# Development Stage
FROM base AS dev
RUN bash scripts/uv/sync.ba.sh

# Testing Stage
FROM dev AS tested
RUN uvx pypyr ci_docker

# Release Stage: Sync production dependencies and freeze versions
FROM base AS release
RUN uv sync --locked --no-dev && uv pip install .
RUN uv pip freeze

# Final Service Stage: Configure runtime environment and expose port
FROM release AS service
EXPOSE 5000
ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0"]
