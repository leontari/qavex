FROM python:3.11-slim

# Install system tools
RUN apt-get update && apt-get install -y \
    curl git docker.io docker-compose \
    nodejs npm \
    kubectl \
    && apt-get clean

# Install pnpm (better for Svelte)
RUN npm install -g pnpm

# Create workspace
WORKDIR /workspace
