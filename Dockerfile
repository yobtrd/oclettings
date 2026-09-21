# Use the official Astral UV image with Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Run the application as a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock /app

# Install dependencies using BuildKit cache
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

COPY . /app

# Use the virtual environment executables
ENV PATH="/app/.venv/bin:$PATH"

# Dummy key required during image build for collectstatic
ENV SECRET_KEY="build_key"

RUN python manage.py collectstatic --noinput

USER nonroot

EXPOSE 8000

# Run migrations before starting Gunicorn
CMD ["sh", "-c", "python manage.py migrate && exec gunicorn --bind 0.0.0.0:8000 oc_lettings_site.wsgi:application"]

