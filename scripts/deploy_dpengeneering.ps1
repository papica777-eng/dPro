#!/usr/bin/env pwsh
# Deploy dpengeneering-main Firebase Functions and Hosting
# Usage: run this locally after you have logged in with Firebase CLI and have the proper project selected.

param()

Write-Host "Installing functions dependencies..."
Push-Location "dpengeneering-main/functions"
npm install
Pop-Location

Write-Host "Make sure you are logged in to Firebase CLI and have selected the project (firebase login && firebase use --add)"
Write-Host "If you need to set function config variables (e.g. Gemini API key), run:"
Write-Host "  firebase functions:config:set gemini.key=\"YOUR_GEMINI_API_KEY\""

Write-Host "Deploying functions and hosting..."
Push-Location "dpengeneering-main"
firebase deploy --only functions,hosting
Pop-Location
