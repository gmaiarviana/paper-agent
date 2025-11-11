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

    This allows scripts to import modules from agents/, utils/, etc.
    without requiring package installation.

    Note: This is a temporary solution for development. For production,
    prefer proper package installation with `pip install -e .`
    """
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
