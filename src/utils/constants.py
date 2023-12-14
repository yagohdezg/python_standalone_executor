import os
import tempfile
from pathlib import Path
from utils import dir_management

PROJECT_DIR = dir_management.get_project_dir()
SRC_DIR = PROJECT_DIR / "src"
RESOURCES_DIR = PROJECT_DIR / "resources"
RESOURCES_DIR.mkdir(exist_ok=True)
SHASUMS_FILE = PROJECT_DIR / "sha256sums.txt"

PROJECT_DIR_ABSOLUTE_DEPTH = len(str(PROJECT_DIR).split(os.sep))
CONF_DEFAULT_PATH = PROJECT_DIR / "app_conf.yaml"

TEMPDIR = Path(tempfile.gettempdir())

KILOBYTE = 1024
FILE_CHUNK_SIZE = 8*KILOBYTE
