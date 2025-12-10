# dPro Fullstack Deployment Guide

## 🚀 Production Deployment (HTTPS)

### Firebase Hosting (Recommended for HTTPS)

Firebase Hosting automatically provides HTTPS for your application.

#### Prerequisites
- Node.js and npm installed
- Firebase CLI installed: `npm install -g firebase-tools`
- Firebase account

#### Deployment Steps

1. **Login to Firebase**
   ```bash
   firebase login
   ```

2. **Initialize Firebase (if not already done)**
   ```bash
   firebase init
   ```
   - Select Hosting, Functions, and Firestore
   - Choose existing project: `kodi-bot-7`
   - Set public directory to `public`
   - Configure as single-page app: Yes

3. **Deploy Backend Functions**
   ```bash
   cd functions
   npm install
   cd ..
   firebase deploy --only functions
   ```

4. **Deploy Frontend**
   ```bash
   firebase deploy --only hosting
   ```

5. **Your app will be available at:**
   - `https://kodi-bot-7.web.app` (HTTPS enabled by default)
   - `https://kodi-bot-7.firebaseapp.com`

### Custom Domain with HTTPS

1. In Firebase Console, go to Hosting
2. Click "Add custom domain"
3. Enter your domain (e.g., `dpro.yourdomain.com`)
4. Follow DNS configuration instructions
5. Firebase automatically provisions SSL certificate

## 🔧 Backend Configuration

### Firebase Functions Backend

The application uses Firebase Functions for:
- QA project management
- AI-powered test case generation
- Real-time data storage in Firestore

**Functions Available:**
- `callKodyAPI` - AI assistant for coding help
- `systemHealth` - Health check endpoint
- `greetUserDB` - User management
- `getUserLearningStats` - Learning analytics
- `getConversationHistory` - Chat history

### Flask Backend (Development)

For local development, you can use the Flask backend:

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

Flask server runs on `http://localhost:5000`

## 🌐 Frontend Configuration

The frontend automatically detects and uses:
- **Firebase Backend** (default) - for production
- **Flask Backend** - for local development

Switch backends in Settings:
1. Click Settings button
2. Select "Backend Type"
3. Choose Firebase or Flask

## 📦 Project Structure

```
dPro/
├── public/              # Frontend files (served by Firebase Hosting)
│   └── index.html       # Main UI with QA features
├── functions/           # Firebase Cloud Functions
│   ├── index.js         # Backend API
│   └── package.json
├── app.py              # Flask backend (optional, for development)
├── firebase.json       # Firebase configuration
└── .firebaserc         # Firebase project settings
```

## 🔐 Security & HTTPS

### Firebase Hosting Security Features
- ✅ Automatic HTTPS with SSL certificate
- ✅ HTTP to HTTPS redirect (automatic)
- ✅ CDN distribution (global)
- ✅ DDoS protection
- ✅ Firestore security rules

### Firestore Security Rules

Update `firestore.rules`:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /qa_projects/{project} {
      allow read: if true;
      allow write: if true; // Update with proper auth
    }
  }
}
```

## 🧪 Testing

### Local Testing with Firebase Emulators

```bash
# Start emulators
firebase emulators:start

# Access at:
# - Hosting: http://localhost:5000
# - Functions: http://localhost:5001
# - Firestore: http://localhost:8080
```

### Production Testing

After deployment, test:
1. Open `https://kodi-bot-7.web.app`
2. Verify HTTPS (look for lock icon)
3. Create a test project
4. Check Firestore console for saved data

## 🔄 Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Firebase
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm ci
      - run: npm run build
      - uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: live
          projectId: kodi-bot-7
```

## 📊 Monitoring

Monitor your application:
- Firebase Console: https://console.firebase.google.com
- Hosting metrics: Bandwidth, requests, errors
- Functions logs: View execution logs
- Firestore usage: Database operations

## 🆘 Troubleshooting

### HTTPS Not Working
- Verify Firebase deployment completed
- Check custom domain DNS settings
- Wait 24-48 hours for DNS propagation

### Functions Not Working
- Check function logs: `firebase functions:log`
- Verify environment variables
- Test locally with emulators

### Frontend Not Loading
- Clear browser cache
- Check Firebase Hosting status
- Verify `public` folder contains index.html

## 🎯 Next Steps

1. ✅ Deploy to Firebase Hosting (HTTPS enabled)
2. ✅ Configure custom domain (optional)
3. ✅ Set up Firestore security rules
4. ✅ Add authentication (recommended)
5. ✅ Enable monitoring and alerts

Your dPro Prototype is now a fullstack web application with:
- ✅ HTTPS enabled by default
- ✅ Firebase backend integration
- ✅ Real-time database
- ✅ AI-powered features
- ✅ Professional QA testing capabilities
