# Use a specialized uv image for fast builds
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy only the files needed for installing dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies without the project itself
RUN uv sync --frozen --no-install-project --no-dev

# --- Final Stage ---
FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the source code
COPY . /app/

# Set Python path to find the src module
ENV PYTHONPATH="/app"

# For now, we run the seed script to verify everything works
CMD ["python", "src/scripts/seed_data.py"]
