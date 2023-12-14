import os
import sys
import hashlib
from pathlib import Path

PROJECT_FOLDER = Path(__file__).parent.parent
SRC_FOLDER = PROJECT_FOLDER / "src"

sys.path.append(str(SRC_FOLDER))
from utils.shasum import shasum256_file

EXE_FILE = PROJECT_FOLDER / f"{sys.argv[1]}.exe"
RESOURCES_FOLDER = PROJECT_FOLDER / "resources"
SHASUM_FOLDERS = [SRC_FOLDER, RESOURCES_FOLDER]
ALLOWED_EXTENSIONS = [
    ".py", ".json"
]

SHASUMS_FILE = PROJECT_FOLDER / "shasums.txt"


sha_sums = f"{shasum256_file(EXE_FILE)} {EXE_FILE.stem}"
for folder in SHASUM_FOLDERS:
    for root, dirs, files in os.walk(folder):
        for file in files:
            file = Path(root) / file

            if file.suffix in ALLOWED_EXTENSIONS:
                files_sums.append(shasum256_file(file))

    sha_sums = hashlib.sha256("".join(sorted(files_sums)).encode("utf-8")).hexdigest()

with open(SHASUMS_FILE, "w+") as file:
    file.write(
        
    )

