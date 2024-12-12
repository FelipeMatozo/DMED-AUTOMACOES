import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL do site que você quer copiar
URL = "https://copelmercadolivre.com/mercado-livre/"

# Diretório para salvar os arquivos localmente
SAVE_DIR = "copel_site"

# Função para baixar arquivos
def download_file(url, folder):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filename = os.path.basename(url.split("?")[0])
        filepath = os.path.join(folder, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Baixado: {url} -> {filepath}")
        return filename
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return None

# Função principal para salvar o site localmente
def save_site(url, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.join(save_dir, "assets"), exist_ok=True)

    # Baixar o HTML
    response = requests.get(url, verify=False)

    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Atualizar links de CSS e JS
    for tag, attr in [("link", "href"), ("script", "src"), ("img", "src")]:
        for element in soup.find_all(tag, {attr: True}):
            file_url = urljoin(url, element[attr])
            filename = download_file(file_url, os.path.join(save_dir, "assets"))
            if filename:
                element[attr] = os.path.join("assets", filename)

    # Salvar o HTML modificado
    with open(os.path.join(save_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Site salvo localmente em {save_dir}/index.html")

# Executar o script
save_site(URL, SAVE_DIR)
