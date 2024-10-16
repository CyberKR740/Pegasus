import requests
from bs4 import BeautifulSoup
from bs4 import Comment

import re
import json

# Função para extrair a receita
def extrair_receita_universal(url):
    # Definir o header, simulando uma requisição feita por um navegador comum
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Fazer a requisição HTTP com o header
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tentar extrair dados estruturados (JSON-LD)
    schema_list = soup.find_all('script', type='application/ld+json')
    for schema in schema_list:
        try:
            data = json.loads(schema.string)
            # Alguns sites têm múltiplos JSON-LD, verificar se contém uma receita
            if isinstance(data, list):
                for item in data:
                    if '@type' in item and item['@type'] == 'Recipe':
                        return formatar_receita(item)
            elif '@type' in data and data['@type'] == 'Recipe':
                return formatar_receita(data)
        except json.JSONDecodeError:
            pass

    # Caso JSON-LD não esteja disponível, usar parsing manual baseado em HTML
    titulo = soup.find('h1').get_text(strip=False) if soup.find('h1') else 'Título não encontrado'
    ingredientes = extrair_ingredientes(soup)
    modo_preparo = extrair_modo_preparo(soup)
    modo_preparo = [item.replace(";", ".\n") for item in modo_preparo]
    modo_preparo = adicionar_espacamento(modo_preparo)

    return {
        "titulo": titulo,
        "ingredientes": ingredientes,
        "modo_preparo": modo_preparo
    }


def adicionar_espacamento(modo_preparo):
    if isinstance(modo_preparo, list):
        # Aplica o espaçamento em cada item da lista
        return [re.sub(r'([a-z])([A-Z])', r'\1 \2', item) for item in modo_preparo]
    else:
        # Caso seja uma string, aplica diretamente
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', modo_preparo)

# Função para extrair os ingredientes usando os seletores informados
def extrair_ingredientes(soup):
    ingredientes = []
    
    # Padrão para identificar ingredientes
    padrao_ingredientes = re.compile(r'(\d+\s?(xícaras?|colheres?|gramas?|colher|ml|sal|pitada?|colher de sopa|fermento|litros?|fermento|químico?|kg|unidades?|ovos?|tabletes?|pacotes?|latas?)\s?[\w\s,]+)', re.IGNORECASE)
    
    # Palavras-chave para identificar a seção de modo de preparo
    palavras_chave_modo_preparo = ["modo de preparo", "preparo", "Modo", "1 No liquidificador", "instruções", "como fazer", "passo a passo"]

    # Função para verificar se o texto contém alguma palavra-chave do modo de preparo
    def encontrou_modo_preparo(texto):
        return any(palavra.lower() in texto.lower() for palavra in palavras_chave_modo_preparo)

    encontrado_modo_preparo = False

    # [Seletores]: 1 Buscar em listas, tabelas e parágrafos
    for ul in soup.find_all(['ul', 'ol']):
        for li in ul.find_all('li'):
            texto = li.get_text(strip=False)
            # Interrompe a busca ao encontrar o "Modo de Preparo"
            if encontrou_modo_preparo(texto):
                encontrado_modo_preparo = True
                break
            if padrao_ingredientes.search(texto):
                ingredientes.append(texto)
        if encontrado_modo_preparo:
            break

    if not encontrado_modo_preparo:
        # [Seletores]: 2 Verificar se ingredientes estão em parágrafos
        for p in soup.find_all('p'):
            texto = p.get_text(strip=False)
            if encontrou_modo_preparo(texto):
                encontrado_modo_preparo = True
                break
            if padrao_ingredientes.search(texto):
                ingredientes.append(texto)

    if not encontrado_modo_preparo:
        # [Seletores]: 3 Verificar se ingredientes estão em tabelas
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cols = row.find_all(['td', 'th'])
                for col in cols:
                    texto = col.get_text(strip=False)
                    if encontrou_modo_preparo(texto):
                        encontrado_modo_preparo = True
                        break
                    if padrao_ingredientes.search(texto):
                        ingredientes.append(texto)
                if encontrado_modo_preparo:
                    break
            if encontrado_modo_preparo:
                break

    # Verificar se o título "Modo de Preparo" está em tags como <h2>, <h3>, <strong>, etc.
    if not encontrado_modo_preparo:
        for tag in soup.find_all(['h2', 'h3', 'strong', 'b']):
            texto = tag.get_text(strip=False)
            if encontrou_modo_preparo(texto):
                encontrado_modo_preparo = True
                break

    return ingredientes or ["Ingredientes não encontrados."]

def extrair_modo_preparo(soup):
    # Regex para ações típicas de preparo
    padrao_acoes = re.compile(r'\b(misture|bata|cozinhe|leve ao forno|combinar|juntar|incorporar|assar|minutos|adicione|ferva|pique|derreta)\b', re.IGNORECASE)
    modo_preparo = set()

    if not modo_preparo:
        for tag in soup.find_all(['p','ol', 'ul']):
            texto = tag.get_text(strip=True)
            if padrao_acoes.search(texto):
                modo_preparo.add(texto)

    # Convertendo o conjunto de volta para uma lista (se necessário)
    modo_preparo = list(modo_preparo)


    # Se ainda não encontrar nada
    if not modo_preparo:
        return ["Modo de preparo não encontrado."]
    
    return modo_preparo


# Função para formatar a receita usando dados estruturados (JSON-LD)
def formatar_receita(data):
    return {
        "titulo": data.get('name', 'Título não encontrado'),
        "ingredientes": data.get('recipeIngredient', ['Ingredientes não encontrados']),
        "modo_preparo": [step.get('text', 'Modo de preparo não encontrado') for step in data.get('recipeInstructions', []) if 'text' in step]
    }

# Testar a função com diferentes URLs
url = [
    "https://receitas.globo.com/receitas-da-tv/mais-voce/bolo-de-mandioca-facil.ghtml",
    "https://amp.tudogostoso.com.br/receita/309779-bolo-de-chocolate-simples.html",  # Site com formatação complicada
    "https://vovopalmirinha.com.br/bolo-de-morango/",
    "https://receitas.globo.com/google/amp/tipos-de-prato/bolos/bolo-de-cenoura-de-liquidificador-4e80cb6a8811965be7003c43.ghtml", "https://globorural.globo.com/vida-na-fazenda/receitas/noticia/2021/12/faca-esse-lindo-e-delicioso-bolo-de-morango-para-suas-comemoracoes.html"
]

#for link in url:
    #search = extrair_receita_universal(link)
    #print(search)