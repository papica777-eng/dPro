import os
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing frontend (index.html) to connect

# --- Firebase Initialization ---
# Path to your service account key.json
SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')

if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
    print(f"WARNING: serviceAccountKey.json not found at {SERVICE_ACCOUNT_KEY_PATH}")
    print("Firebase functionality will be disabled. Running in DEMO mode.")
    print("To enable Firebase:")
    print("1. Download your Firebase service account key")
    print("2. Save it as 'serviceAccountKey.json' in the project root")
    print("3. NEVER commit this file to Git (it's in .gitignore)")
    print("For production: Use environment variables or secret management service")
    db = None  # Set db to None to indicate Firebase is not available
else:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully!")
    except Exception as e:
        print(f"ERROR: Failed to initialize Firebase: {e}")
        print("Running in DEMO mode without Firebase")
        db = None



# --- API Endpoints ---

@app.route('/api/project', methods=['POST'])
def create_project():
    """
    Receives project details from the frontend and saves them to Firestore.
    Simulates running QA checks and generates a report.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    project_name = data.get('project_name')
    target_url = data.get('target_url')
    selected_goals = data.get('selected_goals', {})

    if not project_name or not target_url:
        return jsonify({"error": "Project Name and Target URL are required"}), 400

    print(f"Received new project: {project_name} for {target_url}")
    print(f"Selected Goals: {selected_goals}")

    # --- SIMULATE ACTUAL QA LOGIC HERE ---
    # This is where you would integrate your Python Selenium WebDriver scripts,
    # Gemini Flash analysis, or other QA tools.
    # For now, we'll just simulate processing time and generate a placeholder report.
    time.sleep(4) # Simulate work being done by the bot

    # Generate a placeholder report summary based on selected goals
    report_summary_templates = {
        "Browser Navigation & URL Validation": "Redirect successful to HTTPS, final URL verified, no navigation errors.",
        "Page Element & Content Integrity": "All critical elements (logo, navigation, main content blocks) found and visible. No broken images detected.",
        "Performance Metrics & Load Times": "Initial page load time: ~3.5s. TTFB: ~0.8s. Suggestions: Image lazy-loading and resource compression.",
        "Accessibility Conformance (WCAG)": "Minor contrast issues detected on secondary buttons and some text elements (severity: low). Missing ARIA labels on a few interactive components.",
        "Form Interaction & Data Submission": "Simulated form submission successful. Input validation effective. (Note: Actual forms were not present/tested in this simulated run).",
        "Screenshot & Visual Regression": "Reference screenshots captured for all major breakpoints (desktop, tablet, mobile). Awaiting visual comparison.",
    }
    
    # Filter report summary to only include selected goals
    filtered_report_summary = {
        goal: summary for goal, summary in report_summary_templates.items() if selected_goals.get(goal)
    }

    # Generate recommendations based on the simulated findings
    recommendations = []
    if selected_goals.get("Performance Metrics & Load Times"):
        recommendations.append("Implement image lazy-loading and consider optimizing large assets to meet sub-3s load target.")
    if selected_goals.get("Accessibility Conformance (WCAG)"):
        recommendations.append("Review and adjust contrast ratios for identified elements to comply with WCAG AA standards. Add ARIA labels for better screen reader experience.")
    if selected_goals.get("Screenshot & Visual Regression"):
        recommendations.append("Integrate a visual regression tool to automatically compare new screenshots against baselines.")
    if not recommendations:
        recommendations.append("Initial scan shows good health. Focus on continuous monitoring and performance tuning.")


    # Prepare data for Firestore
    project_data = {
        "project_name": project_name,
        "target_url": target_url,
        "selected_goals": selected_goals, # Store the boolean map of selected goals
        "status": "Completed", # Or "Pending", "Failed" based on actual outcome
        "timestamp": datetime.now(),
        "report_summary": filtered_report_summary,
        "recommendations": recommendations,
        "raw_log": "Simulated raw log data here. In a real scenario, this would be comprehensive output from automation tools."
    }

    # If Firebase is available, save to Firestore
    if db is not None:
        try:
            # Add project to Firestore
            # The add() method returns a tuple: (update_time, document_reference)
            # We need the document_reference to get the ID
            doc_ref = db.collection('projects').add(project_data)
            project_id = doc_ref[1].id
            print(f"Project '{project_name}' saved to Firestore with ID: {project_id}")
            
            # Return the saved project data including the ID and the full report
            project_data['id'] = project_id
            # Convert datetime object to string for JSON serialization
            project_data['timestamp'] = project_data['timestamp'].isoformat()
            
            return jsonify({"message": "Project created and QA simulated successfully", "project_id": project_id, "report": project_data}), 201
        except Exception as e:
            print(f"Error saving project to Firestore: {e}")
            return jsonify({"error": f"Failed to save project to Firestore: {e}"}), 500
    else:
        # DEMO mode - return report without saving to database
        project_data['id'] = 'demo-' + str(int(time.time()))
        project_data['timestamp'] = project_data['timestamp'].isoformat()
        print(f"DEMO MODE: Project '{project_name}' processed (not saved - Firebase disabled)")
        return jsonify({
            "message": "Project created and QA simulated successfully (DEMO MODE - not persisted)", 
            "project_id": project_data['id'], 
            "report": project_data,
            "demo_mode": True
        }), 201

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """
    Retrieves all stored projects from Firestore, ordered by timestamp.
    In DEMO mode, returns empty list with demo notice.
    """
    if db is not None:
        try:
            # Get latest 15 projects, ordered by timestamp descending
            projects_ref = db.collection('projects').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(15)
            docs = projects_ref.stream()
            projects = []
            for doc in docs:
                project_data = doc.to_dict()
                project_data['id'] = doc.id
                # Convert Firestore Timestamp objects to string for JSON serialization
                if 'timestamp' in project_data and hasattr(project_data['timestamp'], 'isoformat'):
                    project_data['timestamp'] = project_data['timestamp'].isoformat()
                projects.append(project_data)
            return jsonify(projects), 200
        except Exception as e:
            print(f"Error retrieving projects from Firestore: {e}")
            return jsonify({"error": f"Failed to retrieve projects: {e}"}), 500
    else:
        # DEMO mode - no persistence
        print("DEMO MODE: No projects to retrieve (Firebase disabled)")
        return jsonify({
            "demo_mode": True,
            "message": "Running in DEMO mode - projects are not persisted",
            "projects": []
        }), 200

if __name__ == '__main__':
    # When running locally without Docker for testing:
    # app.run(debug=True, port=5000)
    # When running with Gunicorn via Docker, the CMD in Dockerfile takes over.
    # This block will typically not run inside the Docker container when Gunicorn is used.
    # It's here for direct local execution without Docker.
    print("Running Flask app directly for local development (not via Gunicorn/Docker).")
    app.run(debug=True, port=5000)
