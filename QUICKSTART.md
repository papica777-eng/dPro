# QUICKSTART.md

## dPro QA Assistant - Quickstart Guide

This guide will help you get the application running in under 5 minutes.

### Option 1: Fastest Start (Using run.sh)

```bash
chmod +x run.sh
./run.sh
```

**That's it!** Open http://localhost:5000 in your browser.

### Option 2: Using Make

```bash
make run
```

### Option 3: Using Docker

```bash
docker-compose up --build
```

### What You'll See

1. **Demo Mode Warning**: If you don't have Firebase configured, the app runs in DEMO mode
   - You can still use all features
   - Projects won't be persisted
   - Perfect for testing!

2. **Web Interface**: Navigate to http://localhost:5000
   - Fill in project details
   - Select automation goals
   - Click "PLAN & EXECUTE AUTOMATION SEQUENCE"
   - View results in the console

### Next Steps

- **Add Firebase** (optional): See README_DEPLOY.md for instructions
- **Explore Features**: Try different automation goals
- **View Documentation**: Check README.md for full details

### Troubleshooting

**Port 5000 in use?**
```bash
# Kill process on port 5000 (Linux/Mac)
lsof -ti:5000 | xargs kill -9
```

**Permission denied?**
```bash
chmod +x run.sh
```

**Need help?**
See README_DEPLOY.md for detailed troubleshooting.

---

**You're all set!** 🎉 Start automating your QA tests with Mister Mind!
