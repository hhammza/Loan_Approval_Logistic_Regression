# ─── WSGI Configuration for PythonAnywhere ───────────────────────────────────
#
# INSTRUCTIONS:
#   1. In PythonAnywhere dashboard → Web → WSGI configuration file
#   2. Replace the entire contents with this file, OR point the WSGI path here.
#   3. Update the path below to match YOUR username and project folder.
#
# Example:
#   If your PythonAnywhere username is "hamzaafzal" and you uploaded the
#   project to /home/hamzaafzal/loan_app/, set:
#     project_folder = '/home/hamzaafzal/loan_app'
# ─────────────────────────────────────────────────────────────────────────────

import sys
import os

# ↓ CHANGE THIS to your actual project path on PythonAnywhere
project_folder = '/home/YOUR_USERNAME/loan_app'

if project_folder not in sys.path:
    sys.path.insert(0, project_folder)

os.chdir(project_folder)

from app import app as application  # noqa
