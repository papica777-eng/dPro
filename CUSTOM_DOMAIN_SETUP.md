# Custom Domain Setup for dpengeneering.site

## 🌐 Configure Firebase Hosting for Custom Domain

### Step 1: Add Custom Domain in Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: **kodi-bot-7**
3. Navigate to **Hosting** in the left sidebar
4. Click **Add custom domain**
5. Enter your domain: `dpengeneering.site`
6. Click **Continue**

### Step 2: Verify Domain Ownership

Firebase will provide you with a TXT record to add to your DNS:

```
Type: TXT
Name: @
Value: [Firebase will provide this value]
TTL: 3600 (or default)
```

Add this record in your domain registrar's DNS management panel.

### Step 3: Configure DNS Records

After verification, Firebase will provide A records. Add these to your DNS:

```
Type: A
Name: @
Value: [Firebase IP addresses - typically provided as multiple records]
TTL: 3600

Type: A  
Name: www
Value: [Same Firebase IP addresses]
TTL: 3600
```

### Common Firebase Hosting A Records:
```
151.101.1.195
151.101.65.195
```

### Step 4: SSL Certificate Provisioning

- Firebase automatically provisions an SSL certificate for your custom domain
- This process can take 24-48 hours after DNS propagation
- Your site will be available at both:
  - `https://dpengeneering.site`
  - `https://www.dpengeneering.site`

## 🚀 Deploy to Custom Domain

### Deploy Frontend and Backend

```bash
# Install Firebase CLI (if not already installed)
npm install -g firebase-tools

# Login to Firebase
firebase login

# Deploy everything
firebase deploy

# Or deploy separately
firebase deploy --only hosting    # Deploy frontend
firebase deploy --only functions  # Deploy backend
```

### Verify Deployment

1. Check Firebase Console → Hosting
2. Verify custom domain status shows "Connected"
3. Visit `https://dpengeneering.site`
4. Test backend endpoints:
   - `https://kodi-bot-7.web.app` (Firebase default)
   - `https://dpengeneering.site` (your custom domain)

## 🔧 Backend Configuration

### API Key Already Configured

The Google Gemini API key is now configured in `functions/index.js`:
```javascript
const API_KEY = "AIzaSyD-V5YcHFaQ7oqsKFFLt8Gg-rTf3IRW24U";
```

### Firebase Functions Endpoints

Your backend functions will be available at:
- Production: `https://us-central1-kodi-bot-7.cloudfunctions.net/[functionName]`
- Custom domain requires Cloud Run or API Gateway for custom function URLs

### Available Functions

1. **callKodyAPI** - AI assistant with Gemini integration
2. **systemHealth** - Health check endpoint
3. **greetUserDB** - User management
4. **getUserLearningStats** - Learning analytics
5. **getConversationHistory** - Chat history

## 📊 Frontend Integration

The frontend (`public/index.html`) is configured to:
- Auto-detect Firebase backend
- Support dual backend mode (Firebase + Flask)
- Use Firestore for real-time data storage

### Test Backend Connection

Open browser console and verify:
```javascript
// Check Firebase initialization
console.log('Firebase app:', firebase.app().name);

// Test Firestore connection
firebase.firestore().collection('qa_projects').get()
  .then(() => console.log('✅ Firestore connected'))
  .catch(err => console.error('❌ Firestore error:', err));
```

## 🔐 Security Configuration

### Security Headers (Already Configured)

```json
{
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "X-XSS-Protection": "1; mode=block",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
}
```

### Firestore Security Rules

Update `firestore.rules` for production:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // QA Projects collection
    match /qa_projects/{project} {
      allow read: if true;
      allow write: if request.auth != null; // Require authentication
    }
    
    // User learning data
    match /user_learning/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Conversations
    match /conversations/{conversation} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 🧪 Testing Your Deployment

### 1. Test Homepage
```bash
curl -I https://dpengeneering.site
# Should return 200 OK with security headers
```

### 2. Test Firebase Functions
```bash
# Health check
curl https://us-central1-kodi-bot-7.cloudfunctions.net/systemHealth

# Expected response:
# {"status":"OK","checks":{"server":{"status":"PASSED","message":"Cloud Function работи."},...}}
```

### 3. Test QA Automation

1. Navigate to `https://dpengeneering.site`
2. Click **Automation** tab
3. Fill in:
   - Project Name: "Test Project"
   - Target URL: "https://example.com"
   - Select test suites
4. Click **START AUTOMATION**
5. Verify data is saved to Firestore
6. Check **History** tab for results

## 📱 Mobile Testing

Test on mobile devices:
- iOS Safari
- Android Chrome
- Responsive design breakpoints

## 🔄 CI/CD Integration (Optional)

### GitHub Actions Deployment

Create `.github/workflows/firebase-deploy.yml`:

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
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: cd functions && npm install
      
      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: live
          projectId: kodi-bot-7
```

## 🆘 Troubleshooting

### Domain Not Working?
1. Wait 24-48 hours for DNS propagation
2. Check DNS records: `nslookup dpengeneering.site`
3. Verify in Firebase Console: Hosting → Custom domains

### SSL Certificate Issues?
1. Ensure DNS records are correct
2. Wait for Firebase to provision certificate (24-48 hours)
3. Check Firebase Console for certificate status

### Backend Not Connecting?
1. Verify API key is correct in `functions/index.js`
2. Check Firebase Console → Functions for deployment status
3. Review function logs: `firebase functions:log`

### CORS Errors?
1. Verify `firebase.json` has proper CORS headers
2. Check browser console for specific errors
3. Ensure backend functions have CORS enabled

## 📞 Support

- Firebase Console: https://console.firebase.google.com
- Firebase Documentation: https://firebase.google.com/docs
- GitHub Issues: https://github.com/papica777-eng/dPro/issues

## ✅ Checklist

- [ ] Custom domain added in Firebase Console
- [ ] DNS records configured (TXT + A records)
- [ ] Domain ownership verified
- [ ] SSL certificate provisioned (wait 24-48 hours)
- [ ] Firebase Functions deployed with API key
- [ ] Frontend deployed to hosting
- [ ] Firestore security rules updated
- [ ] Backend connection tested
- [ ] QA automation tested end-to-end
- [ ] Mobile responsiveness verified

Your dPro QA Automation Platform is now running at **https://dpengeneering.site**! 🎉
