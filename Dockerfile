# ============================
# Stage 1: Build Stage
# ============================
FROM python:3.10-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.4.0
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set work directory
WORKDIR /home/appuser/app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry 
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi


# Link to git repository if needed
LABEL org.opencontainers.image.source=https://github.com/heatomato/fastapi-template

# Copy Mise configuration if needed
#COPY mise.toml ./

# ============================
# Stage 2: Production Stage
# ============================
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install runtime system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.4.0
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Create a non-root user
RUN useradd --create-home appuser

# Set work directory
WORKDIR /home/appuser/app

# Copy the dependencies from the builder stage
COPY --from=builder /home/appuser/app /home/appuser/app

# If Mise requires installation, add here
# Example: RUN pip install mise-tool

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Health check (optional)
#HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#  CMD curl -f http://localhost:8000/health || exit 1

# Define the default command to run the application
# Adjust the command based on how Mise is used in your application
CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4"]