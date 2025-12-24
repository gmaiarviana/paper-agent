"""
Common utilities for validation scripts.

This module provides shared setup functionality to avoid code duplication
across manual validation scripts in the scripts/ directory.

These are MANUAL validation tools for local development, not automated tests.
For automated tests, see tests/unit/ and tests/integration/.
"""

import sys
from pathlib import Path

def setup_project_path():
    """
    Add project root to Python path for imports.

    This allows scripts to import modules from core/agents/, core/utils/, etc.
    without requiring package installation.

    Note: This is a temporary solution for development. For production,
    prefer proper package installation with `pip install -e .`
    """
    project_root = Path(__file__).resolve().parent.parent
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    return project_root
