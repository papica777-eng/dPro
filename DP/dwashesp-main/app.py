import os
import json
import time
import logging
import uuid
import base64
from datetime import datetime
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except Exception:
    firebase_admin = None
    credentials = None
    firestore = None

app = Flask(__name__)

# Config
class Config:
    USE_FIREBASE = os.environ.get('USE_FIREBASE', 'false').lower() == 'true'
    ALLOWED_ORIGINS = [o for o in os.environ.get('ALLOWED_ORIGINS', '*').split(',') if o]
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

app.config.from_object(Config)
if app.config['ALLOWED_ORIGINS']:
    CORS(app, resources={r"/api/*": {"origins": app.config['ALLOWED_ORIGINS']}})
else:
    CORS(app)

logging.basicConfig(level=Config.LOG_LEVEL, format='%(asctime)s %(levelname)s [%(request_id)s] %(name)s: %(message)s')
logger = logging.getLogger('dwashesp')

class AddRequestIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = '-'
        return True

for h in logging.root.handlers:
    h.addFilter(AddRequestIdFilter())

@app.before_request
def _attach_request_id():
    request.request_id = request.headers.get('X-Request-Id') or str(uuid.uuid4())


@app.after_request
def _add_request_id_header(response):
    request_id_val = getattr(request, 'request_id', None)
    if request_id_val:
        response.headers['X-Request-Id'] = request_id_val
    return response

# --- Firebase Initialization ---
db = None
if Config.USE_FIREBASE:
    SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
    gcb64 = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
    try:
        if gcb64:
            cred_bytes = base64.b64decode(gcb64)
            with open(SERVICE_ACCOUNT_KEY_PATH, 'wb') as f:
                f.write(cred_bytes)
            logger.info('Decoded GOOGLE_CREDENTIALS_BASE64 into %s', SERVICE_ACCOUNT_KEY_PATH)
        if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            logger.error('serviceAccountKey.json not found at %s', SERVICE_ACCOUNT_KEY_PATH)
            raise FileNotFoundError(SERVICE_ACCOUNT_KEY_PATH)
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info('Firebase initialized')
    except Exception as e:
        logger.exception('Failed to initialize Firebase')
        raise
else:
    logger.info('Running in LOCAL mode (Firestore disabled)')

# --- API Endpoints ---

@app.route('/api/project', methods=['POST'])
def create_project():
    """
    Receives project details from the frontend and saves them to Firestore.
    Simulates running QA checks and generates a report.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "No JSON body provided"}), 400

    project_name = (data.get('project_name') or '').strip()
    target_url = (data.get('target_url') or '').strip()
    selected_goals = data.get('selected_goals', {})

    if not project_name:
        return jsonify({"success": False, "error": "Project Name is required"}), 400
    if not target_url:
        return jsonify({"success": False, "error": "Target URL is required"}), 400
    parsed = urlparse(target_url)
    if not parsed.scheme or not parsed.netloc:
        return jsonify({"success": False, "error": "Invalid Target URL"}), 400

    logger.info('Received new project: %s for %s', project_name, target_url)
    logger.debug('Selected Goals: %s', selected_goals)

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

    try:
        # Add project to Firestore
        # The add() method returns a tuple: (update_time, document_reference)
        # We need the document_reference to get the ID
        doc_ref = db.collection('projects').add(project_data)
        project_id = doc_ref[1].id
        logger.info("Project '%s' saved to Firestore with ID: %s", project_name, project_id)
        
        # Return the saved project data including the ID and the full report
        project_data['id'] = project_id
        # Convert datetime object to string for JSON serialization
        project_data['timestamp'] = project_data['timestamp'].isoformat()
        
        return jsonify({"success": True, "message": "Project created and QA simulated successfully", "project_id": project_id, "report": project_data}), 201
    except Exception as e:
        logger.exception('Error saving project: %s', e)
        return jsonify({"success": False, "error": "Failed to save project"}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """
    Retrieves all stored projects from Firestore, ordered by timestamp.
    """
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
        return jsonify({"success": True, "projects": projects}), 200
    except Exception as e:
        logger.exception('Error retrieving projects: %s', e)
        return jsonify({"success": False, "error": "Failed to retrieve projects"}), 500


    @app.route('/health', methods=['GET'])
    def health():
        try:
            if db:
                _ = db.collection('system_checks').document('health_check').get()
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            logger.exception('Health check failed: %s', e)
            return jsonify({"status": "error", "message": "dependency check failed"}), 500


    @app.route('/api/ping', methods=['GET'])
    def ping():
        return jsonify({
            "success": True,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "message": "DWASHESP Flask API",
        }), 200


    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception('Unhandled exception: %s', e)
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    # When running locally without Docker for testing:
    # app.run(debug=True, port=5000)
    # When running with Gunicorn via Docker, the CMD in Dockerfile takes over.
    # This block will typically not run inside the Docker container when Gunicorn is used.
    # It's here for direct local execution without Docker.
    logger.info("Running Flask app directly for local development (not via Gunicorn/Docker).")
    PORT = int(os.environ.get('PORT', '5000'))
    app.run(debug=True, port=PORT, host='0.0.0.0')
