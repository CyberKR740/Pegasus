
import requests

# Substitua pela sua chave de API do Google
API_KEY = "AIzaSyB545W1MYY9Ktjt2VHfYuXLgRCl1NYB0Ps"

def verificar_wikipedia(termo):
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": termo,
        "language": "pt",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['search']:
        return True, data['search'][0]['label'], f"https://pt.wikipedia.org/wiki/{data['search'][0]['label'].replace(' ', '_')}"
    else:
        return False, None, None

def verificar_google_knowledge_graph(termo):
    url = f"https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        'query': termo,
        'key': API_KEY,
        'limit': 1,
        'indent': True,
        'languages': 'pt'
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'itemListElement' in data and data['itemListElement']:
        description = data['itemListElement'][0]['result'].get('description', 'Descrição não disponível.')
        detailed_description = data['itemListElement'][0]['result'].get('detailedDescription', {}).get('articleBody', description)
        return True, detailed_description
    else:
        return False, None

def buscar_informacao(termo):
    """Busca informações sobre o termo na Wikipedia e no Google Knowledge Graph."""
    
    resultado_wikipedia = verificar_wikipedia(termo)
    
    if resultado_wikipedia is None:
        return "Informação não encontrada."

    if resultado_wikipedia:
        return resultado_wikipedia
    
    resultado_google, descricao_google = verificar_google_knowledge_graph(termo)
    if resultado_google:
        return descricao_google
    
    return "Informação não encontrada."