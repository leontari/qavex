# =============================================================================
#    BUILD STAGE: create the applicatin in the virtual environment
# =============================================================================
# Use an officeal uv debian image with uv pre-installed and no-Python
FROM ghcr.io/astral-sh/uv:bookworm-slim@sha256:22334efe746f1b69217d455049b484d7b8cacfb2d5f42555580b62415a98e0a3 AS builder

ENV APP_NAME=template-app
ENV APP_DIR=backend/${APP_NAME}

# Enable bytecode compilation as it tends to improve image startup time.
ENV UV_COMPILE_BYTECODE=1
# Enable copy from the cache instead of linking. The cache is a mounted volume.
ENV UV_LINK_MODE=copy
# Disable development dependencies (no-install from [tool.uv.dependency-groups])
ENV UV_NO_DEV=1
# Configure the Python directory so it is consistent.
ENV UV_PYTHON_INSTALL_DIR=/python
# Only use the managed Python version.
ENV UV_PYTHON_PREFERENCE=only-managed

# Use `/app` as the working directory.
WORKDIR /app

# Install the workspace Python first for the layer caching.
RUN --mount=type=bind,source=.python-version,target=.python-version \
    uv python install

# Install and cache the workspace member's dependencies.
# NOTE:
#   CI checks guaranty that the lockfile is up to date.
#   Asserting the lockfile reqruieres all workspace members to be at place.
#   Here we can only install from the lockfile.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=${APP_DIR}/pyproject.toml,target=${APP_DIR}/pyproject.toml \
    uv sync --frozen --package ${APP_NAME}

# Copy the application source code.
COPY ${APP_DIR}/src /app/${APP_DIR}/src

# =============================================================================
#    RUNTIME STAGE: debug version as the prod version doesn't have shell
# =============================================================================
# Use an image that has a minimum set of deps
FROM gcr.io/distroless/cc:debug-nonroot

# Use `/app` as the working directory.
WORKDIR /app

# Copy the Python version as root user.
COPY --from=builder /python /python
# Copy the application from the builder as nonroot user.
COPY --from=builder --chown=nonroot:nonroot /app /app

# Activate venv by placing its binary direcotry at the front of the path.
ENV PATH="/app/.venv/bin:$PATH"
# NOTE: Distroless images use nonroot user with UID:65532 and GID:65532 by default.
USER nonroot
# Disable the base image's dafault busybox/sh entrypoint.
ENTRYPOINT []

# Run the application.
CMD ["fastapi", "run", "backend/template-app/src/main.py", "--host", "0.0.0.0", "--port", "8000"]
