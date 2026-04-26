# =============================================================================
#    BUILD STAGE: create the application using the system Python version
# =============================================================================
# Use an official Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim@sha256:4f5d923c9dcea037f57bda425dd209f3ec643da2f0b74227f68d09dab0b3bb36 AS builder

ENV APP_NAME=template-app
ENV APP_DIR=backend/${APP_NAME}

# Enable bytecode compilation as it tends to improve image startup time.
ENV UV_COMPILE_BYTECODE=1
# Enable copy from the cache instead of linking. The cache is a mounted volume.
ENV UV_LINK_MODE=copy
# Disable development dependencies (no-install from [tool.uv.dependency-groups])
ENV UV_NO_DEV=1
# Disable Python downloads and use the system interpreter across both images.
ENV UV_PYTHON_DOWNLOADS=0

# Use `/app` as the working directory.
WORKDIR /app

# Install and cache the workspace member's dependencies.
# NOTE:
#   CI checks guaranty that the lockfile is up to date.
#   Asserting the lockfile reqruieres all workspace members to be at place.
#   Here we can only install from the lockfile.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=${APP_DIR}/pyproject.toml,target=${APP_DIR}/pyproject.toml \
    uv sync --frozen --package ${APP_NAME}

# Copy the application source code, the lockfiles and settings.
COPY .python-version uv.lock pyproject.toml /app/
COPY ${APP_DIR} /app/${APP_DIR}

# Sync the application in a new .venv environment from the lockfile.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package ${APP_NAME}

# =============================================================================
#    RUNTIME STAGE: the final image with correct wrights and without uv
# =============================================================================
# Use an final debian base image without uv.
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same.
FROM python:3.11-slim-bookworm@sha256:9c6f90801e6b68e772b7c0ca74260cbf7af9f320acec894e26fccdaccfbe3b47

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application source code from the builder stage
# with the correct ownership.
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path.
ENV PATH="/app/.venv/bin:$PATH"
# Use the non-root user to run our application.
USER nonroot
# Use `/app` as the working directory.
WORKDIR /app

# Run the FastAPI application by default.
CMD ["fastapi", "run", "backend/template-app/src/main.py", "--host", "0.0.0.0", "--port", "8000"]
