# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Copy requirements.txt first to leverage Docker's cache.
# If requirements.txt doesn't change, this step won't re-run.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files (do NOT copy secrets into the image)
# serviceAccountKey.json should NOT be baked into the image. Mount it at runtime
# or provide credentials via environment variables (GOOGLE_CREDENTIALS_BASE64).
COPY app.py .
COPY index.html .

# Expose port 5000, as defined in app.py
EXPOSE 5000

# Run the Flask application using Gunicorn for production-ready deployment
# Gunicorn is a production-grade WSGI HTTP Server.
# We will use 'gunicorn' instead of 'flask run' because 'flask run' is for development.
# You need to add 'gunicorn' to your requirements.txt
ENV PORT=5000
CMD ["sh", "-lc", "gunicorn --bind 0.0.0.0:${PORT} app:app"]

# Create a non-root user and group for running the app
RUN groupadd -r appuser && useradd -r -g appuser appuser && mkdir -p /home/appuser
RUN chown -R appuser:appuser /app
USER appuser