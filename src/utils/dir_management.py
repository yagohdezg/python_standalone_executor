import sys
from pathlib import Path


def get_project_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    
    else:
        return Path(__file__).parent.parent.parent
