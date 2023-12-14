import os
import sys
import yaml
import tarfile
import requests
import importlib.util
from utils import constants, shasum


class App:
    def __init__(self, config_path) -> None:
        self.config = self.__load_config(config_path)
        self.app_name = self.config["app_name"]

    def __load_config(self, config_path: str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        return config
    
    def update_from_github(self):
        github_repo = self.config.get("github_repo")
        if github_repo is not None:
            github_api = f'https://api.github.com/repos/{github_repo["owner"]}/{github_repo["repo"]}/releases/latest'
            headers = {
                "Authorization": f"Bearer {github_repo["key"]}",
            }
            latest_release = requests.get(github_api, headers=headers)
            latest_release_json = latest_release.json()
            for asset in latest_release_json["assets"]:
                if asset["name"] == constants.SHASUMS_FILE.name:
                    download_url = asset["url"]

            # If shasums are different, we update the repo
            headers['Accept'] = 'application/octet-stream'
            response_text = requests.get(download_url, headers=headers).text.replace("\r", "")
            if response_text != shasum.get_sha_file_text():
                headers['Accept'] = 'application/json'
                r = requests.get(latest_release_json["tarball_url"], headers=headers, stream=True)
                tmp_file = constants.TEMPDIR / f"{str(id(self))}.tar.gz"
                with open(tmp_file, "wb") as file:
                    for chunk in r.iter_content(constants.FILE_CHUNK_SIZE):
                        file.write(chunk)

                with tarfile.open(tmp_file) as tar:
                    for member in tar.getmembers()[1:]:
                        true_path = constants.SRC_DIR / member.name.split("/", 1)[1]
                        if member.isdir():
                            os.makedirs(true_path, exist_ok=True)
                        else:
                            print(true_path)
                            with tar.extractfile(member) as new_file:
                                with open(true_path, "wb") as old_file:
                                    old_file.write(new_file.read())


def load_module(path):
    spec = importlib.util.spec_from_file_location("main", path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules["main"] = foo

    spec.loader.exec_module(foo)
    foo.main()


if __name__ == "__main__":
    # Load config
    app = App(constants.CONF_DEFAULT_PATH)

    os.chdir(constants.PROJECT_DIR)
    if getattr(sys, "frozen", False):
        app.update_from_github()

    # Start program
    path = constants.SRC_DIR / "main.py"
    sys.path.append(os.getcwd())
    load_module(path)
