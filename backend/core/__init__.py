# core/__init__.py
# Ensures the project root is in the Python path for imports to work from subfolders

import sys
import os

# Dynamically add project root to sys.path when any core module is imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
