import sys
from pathlib import Path

project_home = str(Path(__file__).resolve().parent)
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
