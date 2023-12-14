
import re
import os
import time
import json
import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

import constants


session = requests.Session()
def download_single_url(url: str):
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    name = soup.find("h1").text
    categories = [
        x.text for x in soup.find(string=re.compile(r"Áreas de Práctica")).parent.parent.find_all("span")
        if x.text != ""
    ]
    colegiado = soup.find(string=re.compile(r"Núm. Colegiado:")).parent.text
    colegiado = re.search(r"\d+", colegiado).group(0)
    phone = soup.find("i", {"class": "fa-phone"}).parent.text
    

def get_urls():
    url = "https://lexgoapp.com/directorio/localizacion"
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    urls = []
    for url in soup.find_all("a"):
        url = url.attrs["href"]
        if "espana" in url:
            urls.append(url)

    results = []
    prev_line = ""
    for index, url in enumerate(urls):
        r = session.get(url)
        curr_line = f"\tComunidad autonoma ({index + 1} / {len(urls)}): {Path(url).stem}"
        print("\r" + curr_line.ljust(len(prev_line)), end="")
        prev_line = curr_line

        abogados = BeautifulSoup(r.text, "html.parser").find_all("ul")[1]
        for abogado in abogados.find_all("li"):
            results.append(abogado.find("a").attrs["href"])

    print()

    return list(set(results))


def get_data():
    return
    # print(f"LEXGOAPP")
    # folder = Path("lexgoapp")
    # os.makedirs(folder, exist_ok=True)
    # # urls = get_urls()
    # with open(folder / "urls.json", "r") as file:
    #     urls = list(set(json.loads(file.read())))

    # for index, url in enumerate(urls):
    #     print(f"\tUrl {index + 1} / {len(urls)}\r", end="")
    #     abogado_path = folder / f"{Path(url).stem}.html"
    #     if abogado_path.exists():
    #         continue

    #     r = session.get(url)
    #     with open(abogado_path, "w+") as file:
    #         file.write(r.text)

    #     time.sleep(1)

    
