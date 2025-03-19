FROM python:3.12-slim AS builder

## 这种方式也不错
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install uv package manager
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

ENV TZ="Asia/Shanghai"
#ENV PYTHONPATH=/app

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY packages/ packages/
COPY .env .
COPY config.yml .
COPY README.md .
COPY config.local.yml .
COPY uv.lock .

# Install dependencies
RUN uv sync --frozen  --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Use the correct module path for the application
CMD ["uv", "run", "uvicorn", "demo_fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
