import os
import hashlib
from utils import constants
from pathlib import Path


KB = 1024
CHUNK_SIZE = KB*8
SHASUM_PATHS: list[Path] = [constants.RESOURCES_DIR, constants.SRC_DIR]
ALLOWED_EXTENSIONS = [".py", ".json"]


def shasum256_file(path):
    sha256 = hashlib.sha256()

    with open(path, 'rb') as file:
        file_read = False
        while not file_read:
            data = file.read(CHUNK_SIZE)
            if not data:
                file_read = True

            else:
                sha256.update(data)

    return sha256.hexdigest()


def shasum256_folder(folder: str):
    files_sums = []
    for root, _, files in os.walk(folder):
        for file in files:
            file = Path(root) / file

            if file.suffix in ALLOWED_EXTENSIONS:
                files_sums.append(shasum256_file(file))

    return hashlib.sha256("".join(sorted(files_sums)).encode("utf-8")).hexdigest()


def get_sha_file_text():
    shasum_text = ""
    for path in SHASUM_PATHS:
        project_relative_path = os.sep.join(str(path).split(os.sep)[constants.PROJECT_DIR_ABSOLUTE_DEPTH:])
        if path.is_dir():
            sha256 = shasum256_folder(path)

        elif path.is_file():
            sha256 = shasum256_file(path)

        shasum_text += f"{sha256} {project_relative_path}\n"

    return shasum_text


def create_sha_file():
    with open(constants.SHASUMS_FILE, "w+") as file:
        file.write(get_sha_file_text())


if __name__ == "__main__":
    create_sha_file()