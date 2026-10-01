# AI Design Office v0.1.2 — PythonAnywhere

This package is prepared for PythonAnywhere WSGI deployment.

## Files
- `app.py` — Flask application
- `wsgi.py` — WSGI entry point
- `requirements.txt` — dependencies
- `templates/` and `static/` — interface assets

## PythonAnywhere setup
1. Upload and extract this folder under `/home/YOUR_USERNAME/ai_design_office`.
2. Open a Bash console and create a virtualenv:
   `mkvirtualenv --python=/usr/bin/python3.13 ai-office`
3. Install dependencies:
   `cd ~/ai_design_office && pip install -r requirements.txt`
4. Open **Web → Add a new web app → Manual configuration**, choosing the same Python version.
5. In the Web tab, set the virtualenv to `ai-office`.
6. Open the WSGI configuration file and use:

       import sys
       path = '/home/YOUR_USERNAME/ai_design_office'
       if path not in sys.path:
           sys.path.insert(0, path)
       from app import app as application

7. Save, then press **Reload** in the Web tab.
8. Open the `YOUR_USERNAME.pythonanywhere.com` address shown by PythonAnywhere.

Note: this MVP stores state in server memory and simulates agents with background threads. It is suitable for testing the interaction concept, not persistent production use. A later version should move jobs/state to persistent storage and a proper task queue.
