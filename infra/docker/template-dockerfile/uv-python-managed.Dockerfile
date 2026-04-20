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

# Copy the rest application source code.
COPY ${APP_DIR}/src /app/${APP_DIR}/src

# =============================================================================
#    RUNTIME STAGE: the final image with correct wrights and without uv
# =============================================================================
# Use an official debian based image without uv and without Python.
FROM docker.io/library/debian:bookworm-slim@sha256:4724b8cc51e33e398f0e2e15e18d5ec2851ff0c2280647e1310bc1642182655d

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the Python version.
COPY --from=builder /python /python
# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Activate the project virtual environment by placing its binary direcotry at the front of the path.
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application.
USER nonroot
# Use `/app` as the working directory.
WORKDIR /app

# Run the FastAPI application by default.
CMD ["fastapi", "run", "backend/template-app/src/main.py", "--host", "0.0.0.0", "--port", "8000"]
