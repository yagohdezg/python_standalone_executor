import re
import sys
import typing
import subprocess
import importlib.util
from pathlib import Path
import string


ORIG_MODULES = list(sys.modules.keys())
TMP_MODULE = "ASDHJJSJDASJS"
FILE_DIR = Path(__file__).parent
IMPORTS_FILE = FILE_DIR / "imports.txt"

command = f"pyinstaller --onefile -n {sys.argv[1]} .\\src\\wrapper.py"

modules = set()
files = list((FILE_DIR.parent / "src").glob("**/*.py"))

for file in files:
    with open(file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r"(import ([\w\.]+))|(from ([\w\.]+) import ([\w\., ]+))", line)
            if match is not None:
                import_group = match.group(2)
                from_group = match.group(4)
                
                module = []
                if from_group is not None:
                    module.append(from_group)
                    import_group = match.group(5)

                import_group = import_group.split(" as ")[0].strip()
                for import_ in import_group.split(","):
                    module_tmp = module + [import_.strip()]
                    modules.add(module_tmp[0])

bad_modules = []
for module in modules:
    try:
        __import__(module)
    except:
        bad_modules += [module]

modules = [x for x in modules if x not in bad_modules]

for import_ in modules[:-1]:
    command += f" --hidden-import={import_}"

subprocess.check_call(command, stderr=subprocess.STDOUT)
