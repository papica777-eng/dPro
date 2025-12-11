# dPro

Improvements & How to run

This repository includes two apps:
- Root Flask app (API + embedded frontend) — runs on port 5000
- DP/dwashesp-main Flask-based QA assistant (separate app) — runs on port 5001

New improvements include:
- Structured logging and request IDs for easier observability
- CORS config via ALLOWED_ORIGINS environment variable
- Health check endpoints (`/health`) for use by Render or orchestrators
- Robust config via environment variables for production
- Improved input validation and consistent JSON errors
- Optional Firestore integration if `USE_FIREBASE=true` and credentials provided
- Scripts for building, running, and testing locally (`scripts/`)

Quick local test
1. Build the images and start them using docker-compose:
```powershell
cd "C:\Users\papic\OneDrive\Документи\FeedbackHub\dPro"
docker-compose build
docker-compose up --build
```

2. Run the verification script to smoke-test the endpoints (PowerShell):
```powershell
.\scripts\verify_local.ps1
```

3. The frontends will point to `http://localhost:5000/api` or `http://localhost:5001/api` depending on which app you want to use.

For deployment, use the `README_RENDER.md` and GitHub Actions workflows for professional CI/CD.
