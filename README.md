# dPro - QA Automation Assistant

A full-stack web application for automated quality assurance testing with AI-powered analysis.

## Features

- 🤖 Automated QA testing with Selenium WebDriver
- 🔍 AI-powered analysis with Gemini Flash
- 📊 Comprehensive reporting and metrics
- 🎯 Customizable test goals and scenarios
- 🔥 Firebase backend for data persistence
- 🎨 Modern, responsive UI

## Tech Stack

**Backend:**
- Python 3.x
- Flask (REST API)
- Firebase Admin SDK (Firestore)
- Gunicorn (WSGI server)

**Frontend:**
- HTML5/CSS3/JavaScript
- Modern ES6+ features
- Responsive design

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Firebase project (optional - can run in DEMO mode)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/papica777-eng/dPro.git
cd dPro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Firebase:
   - Create a Firebase project at https://console.firebase.google.com/
   - Download your service account key
   - Save it as `serviceAccountKey.json` in the project root
   - **IMPORTANT:** Never commit this file to Git (it's in .gitignore)

4. Run the application:
```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn -b 0.0.0.0:5000 app:app
```

5. Open your browser and navigate to:
   - Backend API: `http://localhost:5000`
   - Frontend: Open `index.html` in your browser

## Deployment

### Docker Deployment

Build and run with Docker:
```bash
docker build -t dpro-app .
docker run -p 5000:5000 dpro-app
```

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -b 0.0.0.0:$PORT app:app`
4. Add environment variables if using Firebase
5. Deploy!

### Environment Variables (Production)

For production deployments, use environment variables instead of committing credentials:

- `FIREBASE_PROJECT_ID`: Your Firebase project ID
- `FIREBASE_PRIVATE_KEY`: Your Firebase private key
- `FIREBASE_CLIENT_EMAIL`: Your Firebase client email

## DEMO Mode

The application can run without Firebase in DEMO mode:
- All QA tests and reports work normally
- Projects are not persisted to database
- Perfect for testing and development

## API Endpoints

### POST /api/project
Create a new QA project and run tests.

**Request body:**
```json
{
  "project_name": "My Website",
  "target_url": "https://example.com",
  "selected_goals": {
    "Browser Navigation & URL Validation": true,
    "Page Element & Content Integrity": true,
    "Performance Metrics & Load Times": true,
    "Accessibility Conformance (WCAG)": true,
    "Form Interaction & Data Submission": false,
    "Screenshot & Visual Regression": true
  }
}
```

### GET /api/projects
Retrieve all saved projects (latest 15).

## Security

- Never commit `serviceAccountKey.json` or any credentials
- Use environment variables for production secrets
- The `.gitignore` file is configured to exclude sensitive files
- Regular security scans with CodeQL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.