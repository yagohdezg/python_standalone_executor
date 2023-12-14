import re
import time
import json
import urllib3
import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from scrapers.frame import create_frame


def get_urls():
    root = "https://abogadium.com/"
    options = Options()
    options.add_argument("--headless")
    abogados_urls = []
    with webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options) as driver:
        driver.get(root)
        urls = driver.find_element(By.XPATH, '//ul[@class="ul-prov"]').find_elements(By.TAG_NAME, "li")
        urls = [url.find_element(By.TAG_NAME, "a").get_attribute("href") for url in urls]
        
        for url in urls:
            driver.get(url)
            original_html = driver.page_source
            cond = True
            while cond:
                try:
                    driver.find_element(By.XPATH, '//input[@id="ver_mas"]').click()

                    if driver.page_source == original_html:
                        cond = False

                    else:
                        original_html = driver.page_source

                except:
                    cond = False

            abogados_html = driver.page_source
            abogados_div = BeautifulSoup(abogados_html, "html.parser").find_all("div", {"class": "caj-row"})
            abogados_urls  += [div.find("a").attrs["href"] for div in abogados_div[:-1]]

    return list(set([urljoin(root, url) for url in abogados_urls]))


def download_single_url(url: str):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    profile = soup.find("h1", {"class": "miname"}).parent
    profile_paragraphs = profile.find_all("p")
    name = soup.find("h1").text
    despacho = profile_paragraphs[0].text
    colegiado, comunidad_autonoma = re.search(r"colegiado (\d+) de (\S+)", profile_paragraphs[1].text).groups()
    ubicacion = profile_paragraphs[2].text

    description = soup.find("p", {"id": "texto_presentacion"}).text.replace("\n", " ").replace("\r", "")

    # GET TELEPHONE
    abogado_id = re.search(r"id_usuario=(\d+)", profile.parent.find("div").find("div").attrs["style"]).group(1)
    telephone = requests.post("https://abogadium.com/ajax.php", data={"modo": "ver_telefono", "id_usuario": abogado_id}).json()["telefono"]

    # Descripcion
    experience_soup = BeautifulSoup(
        requests.post("https://abogadium.com/ajax.php", {"modo": "listar_sentencias", "id_usuario": abogado_id}).json()["html"],
        "html.parser"
    )
    experiences = ",".join([
        x.text.replace("Sentencias ganadas", "").replace("Ver sentencias", "").split("(")[0].strip() for x in experience_soup.find_all("tr")
    ])
    idiomas = [x.text.replace("\n", "") for x in soup.find("tbody", {"id": "tbl-idiomas"}).find_all("tr")]
    idiomas = ",".join(idiomas)
    
    return pd.Series({
        "link": [url],
        "nombre": [name],
        "direccion": [ubicacion],
        "despacho": [despacho],
        "numero_colegiado": [colegiado],
        "comunidad_autonoma": [comunidad_autonoma],
        "telefono": [telephone],
        "descripcion": [description],
        "idiomas": [idiomas],
        "experiencia": [experiences]
    })
        

def get_data():
    urls = get_urls()
    # with open(Path(__file__).parent / __file__.replace(".py", ".json"), "r") as file:
    #     urls = json.loads(file.read())
    
    frames = []
    for index, url in enumerate(urls):
        frame = download_single_url(url)
        yield (frame, index, len(urls))
