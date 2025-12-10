# Render Deployment Guide

## Issue: "requirements.txt: not found" Error

If you see this error during Docker build on Render, it means you're using Docker deployment when you should use **native Python deployment**.

## ✅ Solution: Use Native Python Deployment (Recommended)

### Option 1: Using render.yaml (Automatic)
1. In Render dashboard, create a **New Web Service**
2. Connect your GitHub repository
3. Render will auto-detect `render.yaml`
4. Ensure the service type shows **"Python"** (NOT "Docker")
5. Click **"Create Web Service"**
6. Done! ✅

### Option 2: Manual Configuration
1. Create a **New Web Service** in Render
2. Connect your repository
3. **Important Settings:**
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -b 0.0.0.0:$PORT app:app`
   - **Root Directory**: `.` (leave empty or use root)
4. Click **"Create Web Service"**

## 🐳 Alternative: Docker Deployment (Not Recommended)

Only use Docker if you have specific requirements. If you must use Docker:

1. Edit `render.yaml` - uncomment the Docker service section
2. Comment out the Python service section
3. In Render dashboard:
   - **Environment**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.` (root directory)
   - **Docker Build Context Directory**: `.` (root)

## Why Native Python is Better

- ✅ Faster builds (no Docker layer overhead)
- ✅ Simpler configuration
- ✅ Lower resource usage
- ✅ Automatic Python version management
- ✅ No Docker build context issues

## Verification

After deployment succeeds:
- Your app will run in DEMO mode (no Firebase needed)
- API will be available at your Render URL
- Health check: Visit `https://your-app.onrender.com/api/projects`

## Adding Firebase (Optional)

1. Go to Render dashboard → Your service → Environment
2. Add environment variables:
   - `FIREBASE_PROJECT_ID`: Your project ID
   - `FIREBASE_PRIVATE_KEY`: Your private key
   - `FIREBASE_CLIENT_EMAIL`: Your client email
3. Restart service

## Still Having Issues?

Make sure:
- [ ] You selected "Python 3" as environment (NOT "Docker")
- [ ] Build command is exactly: `pip install -r requirements.txt`
- [ ] Start command is exactly: `gunicorn -b 0.0.0.0:$PORT app:app`
- [ ] Root directory is empty or `.`
- [ ] Your branch is `main` (or update in render.yaml)
