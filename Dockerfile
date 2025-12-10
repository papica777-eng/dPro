# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Copy requirements.txt first to leverage Docker's cache.
# If requirements.txt doesn't change, this step won't re-run.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files
COPY app.py .

# Create static directory for serving frontend files
RUN mkdir -p /app/static

# Copy frontend files to static directory
COPY index.html ./static/
COPY style.css ./static/

# Copy serviceAccountKey.json if it exists (optional for development)
# Note: In production, this should be mounted as a volume or provided via secrets
COPY serviceAccountKey.jso[n] . || true

# Expose port 5000, as defined in app.py
EXPOSE 5000

# Run the Flask application using Gunicorn for production-ready deployment
# Gunicorn is a production-grade WSGI HTTP Server.
# We will use 'gunicorn' instead of 'flask run' because 'flask run' is for development.
# You need to add 'gunicorn' to your requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]