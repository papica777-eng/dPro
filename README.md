# dPro - QA Assistant Bot

An AI-powered Quality Assurance assistant bot interface with Selenium WebDriver automation capabilities.

## Features

- **AI QA Assistant (Mister Mind)**: Intelligent automation planning and execution
- **Selenium WebDriver Integration**: Production-ready browser automation scripts
- **Multiple Test Suites**: 
  - Browser Navigation & URL Validation
  - Page Element & Content Integrity
  - Performance Metrics & Load Times
  - Accessibility Conformance (WCAG)
  - Form Interaction & Data Submission
  - Screenshot & Visual Regression
- **Firebase/Firestore Integration**: Persistent project storage and history
- **Web Interface**: Beautiful, responsive UI for managing QA projects

## Quick Start

### Using Make (Recommended if you have make installed)

```bash
make run
```

Or see all available commands:
```bash
make help
```

### Using the Run Script

```bash
./run.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up static files
- Start the application at `http://localhost:5000`

### Using Docker

```bash
docker-compose up --build
```

Then open `http://localhost:5000` in your browser.

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up static files
mkdir -p static
cp index.html static/
cp style.css static/

# Run the application
python app.py
```

## Deployment

For detailed deployment instructions, see [README_DEPLOY.md](README_DEPLOY.md)

## Firebase Configuration (Optional)

The application runs in DEMO mode without Firebase. To enable full functionality:

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Download the service account key as `serviceAccountKey.json`
4. Place it in the project root directory

## Project Structure

```
dPro/
├── app.py                  # Flask backend API
├── index.html              # Frontend interface
├── style.css              # Styling (embedded in HTML)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── run.sh                 # Quick start script
└── README_DEPLOY.md       # Detailed deployment guide
```

## API Endpoints

- `GET /` - Web interface
- `POST /api/project` - Create new QA project
- `GET /api/projects` - Retrieve project history

## Development

The application uses:
- **Backend**: Python Flask with Firebase Admin SDK
- **Frontend**: Vanilla JavaScript with modern CSS
- **Deployment**: Docker + Gunicorn

## License

Copyright © 2023 dPro QA Assistant
