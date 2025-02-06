import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import date

def editais_ufu(filtros_orgs_on = False , filtros_tipos_on = False):
    # Os filtros são definidos nessas duas listas
    filtros_orgs = {"FMVZ","PET Sistemas de Informação", "PET Sistemas de Informação - Monte Carmelo", "PETSIMC", "PET Sistemas de Informação - Monte Carmelo", "PET Ciência da Computação", "PROPP", "PET Sistemas de Informação",  }
    filtros_tipos = {"Programa PET", "Estágio UFU", "Mest./Dout./Especializ.", "Monitoria"}

    # Obtém o ano atual para comparar com a data dos editais e transforma em String
    data_atual = date.today()
    ano_atual = '{}'.format(data_atual.year)

    # Inicializa variáveis de controle
    id_pag = 0  # Página inicial
    QTD_MAX = 20  # Última página
    continuar = True  # Variável que indica se devemos continuar a busca

    # Lista que vai armazenar todos os dados de editais coletados
    editais_data = []

    # Laço que percorre as páginas de editais enquanto a quantidade de páginas for menor que QTD_MAX e devemos continuar
    while (id_pag < QTD_MAX and continuar):
        # Formata a URL da página de editais com o número da página atual
        url = f"http://www.editais.ufu.br/discente?page={id_pag}&order=field_data_publicacao_value&sort=desc"

        # Faz uma requisição HTTP para obter o conteúdo da página
        response = requests.get(url)

        # Verifica se a requisição foi bem-sucedida (status 200)
        if response.status_code == 200:
            # Analisa o conteúdo da página HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontra todos os blocos de editais (linhas da tabela de editais)
            edital_blocks = soup.find_all('tr')

            # Itera sobre cada edital encontrado na página
            for edital in edital_blocks:
                numero_edital = edital.find('td', class_='views-field-field-nro-value')
                numero_edital = numero_edital.get_text(strip=True) if numero_edital else 'N/A'

                orgao_responsavel = edital.find('td', class_='views-field-field-setor-responsavel-value')
                orgao_responsavel = orgao_responsavel.get_text(strip=True) if orgao_responsavel else 'N/A'

                titulo = edital.find('td', class_='views-field-title')
                titulo_text = titulo.get_text(strip=True) if titulo else 'N/A'

                link_edital = None
                if titulo:
                    a_tag = titulo.find('a', href=True)  # Encontra a tag que contém o link
                    if a_tag:
                        # Cria a URL completa do edital usando urljoin
                        link_edital = urljoin(url, a_tag['href'])

                tipo = edital.find('td', class_='views-field-field-tipo-value')
                tipo = tipo.get_text(strip=True) if tipo else 'N/A'

                data_publicacao = edital.find('td', class_='views-field-field-data-publicacao-value')
                data_publicacao = data_publicacao.get_text(strip=True) if data_publicacao else 'N/A'

                # Extrai o ano da data de publicação
                ano_edital = '{}'.format(data_publicacao[4:9].strip())
                # Se qualquer uma dessas informações estiver disponível, cria um dicionário com os dados do edital
                if numero_edital != 'N/A' or orgao_responsavel != 'N/A' or titulo_text != 'N/A' or tipo != 'N/A' or data_publicacao != 'N/A' or link_edital:
                    edital_info = {
                        'numero_edital': numero_edital,
                        'orgao_responsavel': orgao_responsavel,
                        'titulo': titulo_text,
                        'tipo': tipo,
                        'data_publicacao': data_publicacao,
                        'link': link_edital
                    }
                    if(ano_edital == ano_atual):
                        if (filtros_orgs_on and filtros_tipos_on):
                            if (orgao_responsavel in filtros_orgs) and (tipo in filtros_tipos):
                                editais_data.append(edital_info)
                        elif (filtros_orgs_on == False) and (filtros_tipos_on):
                            if(tipo in filtros_tipos):
                                editais_data.append(edital_info)
                        elif (filtros_orgs_on) and (filtros_tipos_on == False):
                            if(orgao_responsavel in filtros_orgs):
                                editais_data.append(edital_info)
                        else:
                            editais_data.append(edital_info)
            # Se o ano do edital não for o ano atual, interrompe a busca
            if(ano_edital < ano_atual):
                continuar = False

        else:
            # Exibe uma mensagem de erro se a página não for acessada com sucesso
            print(f"Erro ao acessar a página. Status code: {response.status_code}")
            break

        # Incrementa o número da página para acessar a próxima
        id_pag += 1

    return editais_data

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
        #return json.dumps(links_info, indent=4)
        return links_info


if __name__ == 'main':
    print("Webscraping Carregado")
