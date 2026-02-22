# Build context: backend/ (e.g. docker build -f backend/Dockerfile backend/)
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies (uv lock must be generated first: uv lock)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-workspace --package app

COPY scripts /app/scripts
COPY app /app/app
COPY pyproject.toml /app/
COPY uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package app

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/utils/health-check/')" || exit 1

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "app/main.py"]
