# Use official Python runtime as a parent image
FROM python:3.13-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.0.0
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app/src

# System deps
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Workdir
WORKDIR /app

# Copy dependencies
COPY pyproject.toml poetry.lock* ./

# Install deps (inclui gunicorn!)
RUN poetry install --no-root

# Copy code
COPY . .

# Copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Entry
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["gunicorn", "src.cinereserve_api.wsgi:application", "--bind", "0.0.0.0:8000"]