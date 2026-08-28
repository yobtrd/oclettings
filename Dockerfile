# Use the official Astral UV image with Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Create a non-root user for security to avoid running the app as root
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock /app

# Install dependencies using BuildKit cache to speed up the build process
# --frozen ensures that uv.lock is not updated during the build
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy the rest of the application code
COPY . /app

# Add the virtual environment bin folder to the system PATH so we can run python/gunicorn directly
ENV PATH="/app/.venv/bin:$PATH"

# Provide a dummy secret key to allow collectstatic to run during build without crashing
ENV SECRET_KEY="build_key" 

# Gather all static files into a single folder for WhiteNoise to serve in production
RUN python manage.py collectstatic --noinput

# Switch to the non-root user for running the application
USER nonroot

# The port the container will listen on
EXPOSE 8000

# Run the production server using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "oc_lettings_site.wsgi:application"]
