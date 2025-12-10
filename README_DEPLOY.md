# Deployment and Running Guide

This guide explains how to deploy and run the dPro QA Assistant Bot application.

## Quick Start (Local Development)

### Option 1: Run with Python directly

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

### Option 2: Run with Docker

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Firebase Configuration (Optional)

The application can run in DEMO mode without Firebase, but for full functionality:

1. **Create a Firebase Project:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or select an existing one

2. **Enable Firestore:**
   - In your Firebase project, go to Firestore Database
   - Click "Create Database"
   - Start in test mode or production mode as needed

3. **Download Service Account Key:**
   - Go to Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `serviceAccountKey.json` in the project root directory

4. **Restart the application** to use Firebase storage

## Production Deployment

### Using Docker

1. **Build the Docker image:**
   ```bash
   docker build -t dpro-qa-assistant .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     -p 5000:5000 \
     -v $(pwd)/serviceAccountKey.json:/app/serviceAccountKey.json:ro \
     --name dpro-app \
     dpro-qa-assistant
   ```

### Using Docker Compose (Recommended)

1. **Ensure serviceAccountKey.json exists** (or remove the volume mount in docker-compose.yml)

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

3. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the services:**
   ```bash
   docker-compose down
   ```

## Environment Variables

Copy `.env.example` to `.env` and customize as needed:

```bash
cp .env.example .env
```

Available variables:
- `FLASK_ENV`: Set to `development` or `production`
- `FLASK_DEBUG`: Enable/disable debug mode
- `PORT`: Application port (default: 5000)

## API Endpoints

- `GET /` - Main web interface
- `POST /api/project` - Create a new QA project
- `GET /api/projects` - Get all projects (requires Firebase)

## Features

### Demo Mode
When Firebase is not configured, the application runs in DEMO mode:
- Project submissions are accepted but not persisted
- History is empty
- All QA simulations work normally

### Full Mode (with Firebase)
When Firebase is configured:
- Projects are stored in Firestore
- Full history tracking
- Persistent storage across restarts

## Troubleshooting

### Port already in use
If port 5000 is already in use, either:
- Stop the application using that port
- Change the port in docker-compose.yml or when running directly

### Firebase connection errors
- Verify serviceAccountKey.json is in the correct location
- Check that the service account has necessary permissions
- Ensure Firestore is enabled in your Firebase project

### Docker build issues
- Ensure Docker is installed and running
- Try rebuilding without cache: `docker-compose build --no-cache`
- **SSL Certificate Issues**: If you encounter SSL certificate errors during Docker build, you may need to:
  - Update your Docker daemon's certificate configuration
  - Use a different base image
  - Build in an environment with proper SSL certificates

### Static files not found
If the web interface shows 404 errors:
- Ensure the `static/` directory exists and contains `index.html` and `style.css`
- Run `./run.sh` which automatically sets up static files
- Or manually: `mkdir -p static && cp index.html static/ && cp style.css static/`

## Development

To modify the application:

1. Edit source files (app.py, index.html, style.css)
2. For Docker: rebuild and restart
   ```bash
   docker-compose up --build
   ```
3. For direct Python: just restart the app

## Support

For issues or questions, please refer to the main README.md file.
