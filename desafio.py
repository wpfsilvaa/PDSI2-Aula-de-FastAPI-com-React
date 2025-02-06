import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def desafio():
    url = f"http://ufu.br"
    response = requests.get(url)
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        blocos = soup.find_all('li')
        
        # Lista para armazenar os resultados
        links_info = []

        # Iterando sobre os elementos encontrados
        for bloco in blocos:
            link_tag = bloco.find('a')  # Encontra a tag <a> dentro de <li>
            if link_tag:  # Verifica se a tag <a> existe
                nome_link = link_tag.get_text(strip=True)  # Extrai o texto (nome do link)
                link = urljoin(url, link_tag['href'])  # Cria o URL completo
                links_info.append({
                    'nome_link': nome_link,
                    'link': link
                })
        return json.dumps(links_info, indent=4)

# Chamando a função
resultados = desafio()
print(resultados)  # Isso irá imprimir o resultado como um JSON