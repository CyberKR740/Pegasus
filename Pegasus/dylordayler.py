import re
import sys
import nltk
import time
import html
import requests
import threading
import difflib

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from data_base.database import criar_tabela, salvar_em_db
from data_base.database import buscar_resposta_db, inicializar_db
from concurrent.futures import ThreadPoolExecutor, as_completed
from aki_waiko import tipos_de_coisas
from unicodeNLP.normalized import custom_stop_words_normalized
from ortografo_org.biotxa import corrigir_texto
from sinonimo.sinonimo_nobu import introducao_sinonimos
from receita.queey import extrair_receita_universal
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime, timedelta

DATABASE = 'historico_perguntas_respostas.db'

stop_words = set(stopwords.words('portuguese'))
stop_words.update(custom_stop_words_normalized)

def calcular_validade(data_coleta):
    """Calcula a validade do resultado com base na data de coleta."""
    data_atual = datetime.now()
    prazo_validade = timedelta(days=1)
    validade = prazo_validade - (data_atual - data_coleta)
    
    if validade.total_seconds() > 0:
        return validade.total_seconds() / prazo_validade.total_seconds()
    else:
        return 0

def calcular_relevancia(texto, palavras_chave, sinônimos):
    """Calcula a relevância de um texto baseado nas palavras-chave e sinônimos."""
    relevancia = 0
    texto_normalizado = texto.lower()

    for palavra in palavras_chave:
        if palavra.lower() in texto_normalizado:
            relevancia += 1

    for sinonimo in sinônimos:
        if sinonimo.lower() in texto_normalizado:
            relevancia += 1

    return relevancia

def verificar_robots_txt(url):
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        response = requests.get(robots_url)
        if response.status_code == 200:
            if "Disallow:" in response.text:
                lines = response.text.splitlines()
                for line in lines:
                    if line.startswith("Disallow:"):
                        disallowed_path = line.split(":")[1].strip()
                        if disallowed_path in url:
                            return False
        return True
    except Exception as e:
        print(f"Erro ao verificar robots.txt: {e}")
        return

def decodificar_texto(texto_codificado):
    texto_limpo = texto_codificado.replace(", [", "")
    texto_limpo = re.sub(r"\[[0-9]+\]", "", texto_limpo)

    return texto_limpo

def acessar_site(url, semaphore, limite_caracteres=1000):
    with semaphore:
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                conteudo = response.content.decode('utf-8')
                soup = BeautifulSoup(conteudo, "html.parser")

                for tag in ['header', 'footer', 'aside', 'nav']:
                    [s.extract() for s in soup.find_all(tag)]
                for class_name in ['sidebar', 'advertisement', 'social', 'footer', 'header']:
                    [s.extract() for s in soup.find_all(class_=class_name)]
                for id_name in ['header', 'footer', 'sidebar', 'ads']:
                    [s.extract() for s in soup.find_all(id=id_name)]
                
                paragrafos = [p.get_text(strip=False) for p in soup.find_all('p')]
                
                paragrafos_filtrados = []
                for paragrafo in paragrafos:
                    if len(paragrafo) > 50 and paragrafo.count('http') < 2:
                        paragrafos_filtrados.append(paragrafo)
                
                texto_limpo = ' '.join(paragrafos_filtrados)
                texto_limpo = texto_limpo.replace('\xa0', ' ')

                if len(texto_limpo) > limite_caracteres:
                    texto_limpo = texto_limpo[:limite_caracteres]

                return texto_limpo if texto_limpo else None
            else:
                pass
        except Exception as e:
            pass

def processar_links(links):
    """Faz o scraping de múltiplos links de forma concorrente usando threads."""
    resultados = []
    max_threads = 10
    semaphore = threading.Semaphore(max_threads)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(acessar_site, link, semaphore): link for link in links}
        
        for future in as_completed(futures):
            resultado = future.result()
            if resultado:
                resultados.append(resultado)

    return resultados

def formatar_receita(titulo, ingredientes, modo_preparo):
    """Formata a receita para uma mensagem legível no Telegram."""
    
    # Título em negrito
    mensagem = f"{titulo}\n\n"  

    if ingredientes:
        mensagem += "Ingredientes:\n"
        mensagem += "\n".join(f"• {ingrediente}" for ingrediente in ingredientes) + "\n\n"

    if modo_preparo:
        mensagem += "Modo de Preparo:\n"
        mensagem += "\n".join(f"{i+1}. {passo.strip()}" for i, passo in enumerate(modo_preparo)) + "\n"

    return mensagem

def rankear_resultados(pergunta, palavras_chave, resultados, exibir_impressao=True):
    """
    Classifica os resultados com base nas palavras-chave e sinônimos, retornando o melhor resultado.
    Quando importada, suprime as mensagens e retorna apenas o conteúdo final.

    Args:
        pergunta (str): A pergunta que está sendo respondida.
        palavras_chave (list): Lista de palavras-chave para avaliação.
        resultados (list): Lista de resultados, cada um contendo um 'link' para a fonte de conteúdo.
        exibir_impressao (bool): Define se as mensagens de impressão devem ser exibidas.

    Returns:
        str: Melhor resultado encontrado ou uma mensagem de erro.
    """
    resultados_rankeados = []
    sinonimos = []

    # Gera sinônimos das palavras-chave
    for palavra in palavras_chave:
        sinonimos_palavra = introducao_sinonimos(palavra)
        if sinonimos_palavra:
            sinonimos.extend(sinonimos_palavra)  # Adiciona os sinônimos, se houver

    # Exibe sinônimos encontrados se necessário
    if exibir_impressao and not sinonimos:
        print(f"Nenhum sinônimo encontrado para {palavras_chave}")
    elif exibir_impressao:
        print(f"Sinônimos encontrados: {sinonimos}")

    for resultado in resultados:
        conteudo = extrair_conteudo_relevante(resultado['link'])

        if conteudo:
            conteudo_lower = conteudo.lower()
            # Calcula o score de relevância com base em palavras-chave e sinônimos
            ranking_score = (
                sum(1 for palavra in palavras_chave if palavra.lower() in conteudo_lower) +
                sum(1 for sinonimo in sinonimos if sinonimo.lower() in conteudo_lower)
            )

            resultados_rankeados.append({
                'link': resultado['link'],
                'conteudo': conteudo,
                'ranking_score': ranking_score
            })

    # Ordena os resultados com base no score de relevância
    resultados_rankeados = sorted(resultados_rankeados, key=lambda x: x['ranking_score'], reverse=True)

    if exibir_impressao:
        print("Resultados e seus scores:")
        for resultado in resultados_rankeados:
            print(f"Link: {resultado['link']}, Score: {resultado['ranking_score']}")

    melhor_resultado = resultados_rankeados[0] if resultados_rankeados else None

    if melhor_resultado:
        soup = BeautifulSoup(melhor_resultado['conteudo'], 'html.parser')
        paragrafos = soup.find_all('p')
        conteudo_final = '\n'.join(p.get_text(strip=False) for p in paragrafos)
        conteudo_final = re.sub(r"\[[0-9]+\]", "", conteudo_final)

        # Verifica se a pergunta envolve a extração de uma receita
        if any(palavra.lower() in tipos_de_coisas or palavra.lower() == 'como fazer' for palavra in palavras_chave):
            receita = extrair_receita_universal(melhor_resultado['link'])
            resultado_receita = formatar_receita(receita['titulo'], receita['ingredientes'], receita['modo_preparo'])
            if exibir_impressao:
                print(f"Título: {receita['titulo']}")
                print("\nIngredientes:\n" + "\n".join(receita['ingredientes']))
                print("\nModo de Preparo:\n" + "\n".join(receita['modo_preparo']))
            return resultado_receita
        else:
            resultado_final = {
                'link': melhor_resultado['link'],
                'conteudo': conteudo_final,
                'ranking_score': melhor_resultado['ranking_score']
            }
            if exibir_impressao:
                print(f"\nMelhor resultado encontrado (Ranking Score: {melhor_resultado['ranking_score']}):")
                print(f"Link: {resultado_final['link']}")
                print("\nConteúdo Extraído:\n" + limitar_resposta(resultado_final['conteudo'], pergunta) + "\n")
            return limitar_resposta(resultado_final['conteudo'], pergunta)
    else:
        if exibir_impressao:
            print("\nNenhum resultado relevante encontrado.")
        return {"erro": "Nenhum resultado relevante encontrado."}

def limitar_resposta(texto, pergunta, limite_curto=300, limite_longo=800, limite_linhas=300):
    """
    Limita o tamanho da resposta com base no contexto da pergunta e nas palavras-chave. Se não encontrar
    palavras-chave ou sinônimos suficientes, ainda tenta retornar conteúdo relevante.

    Args:
        texto (str): O texto completo do qual a resposta será extraída.
        pergunta (str): A pergunta original feita pelo usuário.
        limite_curto (int): O limite de caracteres para respostas curtas.
        limite_longo (int): O limite de caracteres para respostas longas.
        limite_linhas (int): O número máximo de linhas para a resposta.

    Returns:
        str: A resposta limitada, ou uma mensagem de erro.
    """
    if texto is None:
        return "Desculpe, não há resposta disponível."
    limite_longo= len(texto)
    # Determinar se a resposta deve ser curta ou longa
    limite = limite_longo if necessita_resposta_longa(pergunta, texto) else limite_curto
    texto_limpo = BeautifulSoup(texto, 'html.parser').get_text(strip=False)

    # Gera palavras-chave e seus sinônimos
    palavras_chave = gerar_palavras_chave(pergunta)
    palavras_chave_processadas = introducao_sinonimos(palavras_chave)

    # Se não houver palavras-chave ou sinônimos, não retornar erro, mas buscar o conteúdo
    if not palavras_chave_processadas:
        print("Aviso: Nenhuma palavra-chave ou sinônimo encontrado, extraindo conteúdo genérico.")
        return limitar_conteudo_generico(texto_limpo, limite, limite_linhas)

    paragrafos = texto_limpo.split('\n')

    if not paragrafos:
        print("Nenhum parágrafo foi encontrado no conteúdo.")
        return "Nenhuma informação relevante encontrada."

    paragrafo_inicial = None

    # Busca o parágrafo inicial que contém palavras-chave ou seus sinônimos
    for i, paragrafo in enumerate(paragrafos):
        for chave in palavras_chave_processadas:
            if chave in paragrafo.lower():
                paragrafo_inicial = i
                break
        if paragrafo_inicial is not None:
            break

    # Se não encontrar nenhuma palavra-chave ou sinônimo, retornar conteúdo genérico
    if paragrafo_inicial is None:
        print("Nenhuma das palavras-chave ou sinônimos foi encontrada no texto.")
        return limitar_conteudo_generico(texto_limpo, limite, limite_linhas)

    # Extrai o texto a partir do parágrafo encontrado
    texto_extraido = []
    linhas_contadas = 0
    total_caracteres = 0

    for j in range(paragrafo_inicial, len(paragrafos)):
        paragrafo_atual = paragrafos[j].strip()

        if paragrafo_atual:
            texto_extraido.append(paragrafo_atual)
            linhas_contadas += 1
            total_caracteres += len(paragrafo_atual)

            if linhas_contadas >= limite_linhas or total_caracteres >= limite:
                break

    texto_final = ' '.join(texto_extraido)

    # Se o texto final ultrapassar o limite, cortá-lo adequadamente
    if len(texto_final) > limite:
        texto_cortado = texto_final[:limite]
        ultima_ocorrencia_ponto = max(texto_cortado.rfind('.'),
                                      texto_cortado.rfind('!'),
                                      texto_cortado.rfind('?'))

        if ultima_ocorrencia_ponto != -1:
            return texto_cortado[:ultima_ocorrencia_ponto + 1]
        else:
            return texto_cortado

    return texto_final

def limitar_conteudo_generico(texto_limpo, limite, limite_linhas):
    """
    Limita o conteúdo de forma genérica, sem depender de palavras-chave, retornando o primeiro conjunto de parágrafos.

    Args:
        texto_limpo (str): O texto limpo extraído do HTML.
        limite (int): O número máximo de caracteres permitidos.
        limite_linhas (int): O número máximo de linhas permitidas.

    Returns:
        str: O conteúdo limitado.
    """
    paragrafos = texto_limpo.split('\n')
    texto_extraido = []
    linhas_contadas = 0
    total_caracteres = 0

    for paragrafo in paragrafos:
        paragrafo_atual = paragrafo.strip()

        if paragrafo_atual:
            texto_extraido.append(paragrafo_atual)
            linhas_contadas += 1
            total_caracteres += len(paragrafo_atual)

            if linhas_contadas >= limite_linhas or total_caracteres >= limite:
                break

    texto_final = ' '.join(texto_extraido)

    if len(texto_final) > limite:
        texto_cortado = texto_final[:limite]
        ultima_ocorrencia_ponto = max(texto_cortado.rfind('.'),
                                      texto_cortado.rfind('!'),
                                      texto_cortado.rfind('?'))

        if ultima_ocorrencia_ponto != -1:
            return texto_cortado[:ultima_ocorrencia_ponto + 1]
        else:
            return texto_cortado

    return texto_final

def extrair_conteudo_relevante(url, keywords=None):
    """
    Extrai conteúdo relevante de uma URL dada, incorporando:

    - Priorização de elementos semânticos (article, section, main)
    - Filtragem opcional por palavras-chave para maior precisão
    - Remoção de seções irrelevantes (footer, header, nav, etc.)
    - Preservação da formatação usando BeautifulSoup4
    - Tratamento de erros para potenciais exceções de requisição
    - Flexibilidade para personalização através do parâmetro de palavras-chave

    Args:
        url (str): A URL da página da qual extrair conteúdo.
        keywords (list, optional): Uma lista de palavras-chave para filtrar o conteúdo. Padrão é None.

    Returns:
        str: O conteúdo extraído, formatado com tags preservadas.

    Raises:
        requests.exceptions.RequestException: Se ocorrer um erro durante a requisição.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in ['header', 'footer', 'aside', 'nav']:
            [s.extract() for s in soup.find_all(tag)]
        for class_name in ['sidebar', 'advertisement', 'social']:
            [s.extract() for s in soup.find_all(class_=class_name)]
        for id_name in ['header', 'footer', 'sidebar', 'ads']:
            [s.extract() for s in soup.find_all(id=id_name)]

        content_element = soup.find('article') or soup.find('section') or soup.find('main')

        if content_element is None:
            return ""

        paragraphs = content_element.find_all('p')
        filtered_paragraphs = []

        for p in paragraphs:
            text = p.get_text(strip=False)

            if keywords:
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    filtered_paragraphs.append(str(p))
            else:
                filtered_paragraphs.append(str(p))

        formatted_content = '\n'.join(filtered_paragraphs)

        return formatted_content.strip()

    except requests.exceptions.RequestException as e:
        return ""

def necessita_resposta_longa(pergunta, conteudo_final):
    """
    Determina se uma pergunta requer uma resposta longa baseada em palavras-chave.
    A decisão é tomada com base nas palavras-chave presentes na pergunta, e não no conteúdo final.
    """
    
    if pergunta is None or conteudo_final is None:
        return False
    
    if isinstance(pergunta, list):
        pergunta = ' '.join(pergunta)
    
    palavras_chave_curta = [
        'quem é', 'onde fica', 'o que é', 'qual é', 'quando foi', 'quem e'
    ]
    palavras_chave_longa = [
        'explique', 'detalhe', 'como funciona', 'por que', 'quais são',
        'quais sao', 'de um exemplo', 'historia', 'informacoes', 'explicacao',
        'comparacao', 'de datalhes', 'analise', 'diferenca',
        'dê um exemplo', 'descreva', 'biografia', 'pesquise', 'Pesquise', 'pesquisa',
        'Pesquisa', 'história', 'informações', 'como fazer', 'Como fazer',
        'passos', 'processo', 'funcionamento', 'exemplos', 'explicação', 
        'diferença', 'comparação', 'vantagens', 'desvantagens', 'dê detalhes',
        'carreira', 'perfil', 'origem', 'contexto', 'background', 'análise'
    ]
    
    if any(palavra in pergunta.lower() for palavra in palavras_chave_curta):
        return False

    if any(palavra in pergunta.lower() for palavra in palavras_chave_longa):
        return True

    return False

def encontrar_melhor_resultado(texto, palavras_chave, palavras_chave_especiais=[]):
    """
    Verifica se o texto contém todas as palavras-chave e dá mais importância às palavras-chave especiais.
    
    Args:
        texto (str): O texto a ser verificado.
        palavras_chave (list): Lista de palavras-chave a serem encontradas no texto.
        palavras_chave_especiais (list): Lista de palavras-chave especiais que têm prioridade.
        
    Returns:
        bool: True se todas as palavras-chave e as especiais forem encontradas, False caso contrário.
    """
    texto = texto.lower()

    for palavra in palavras_chave:
        if palavra.lower() not in texto:
            return False

    if palavras_chave_especiais:
        for palavra_especial in palavras_chave_especiais:
            if palavra_especial.lower() in texto:
                return True

        return False

    return True

def obter_melhor_resultado(textos_rankeados, palavras_chave, palavras_chave_especiais=[]):
    """
    Encontra o melhor texto nos resultados rankeados que contenha todas as palavras-chave e, se houver, palavras-chave especiais.
    
    Args:
        textos_rankeados (list): Lista de textos com ranking, cada item é um dicionário com 'texto' e 'ranking'.
        palavras_chave (list): Lista de palavras-chave a serem verificadas no texto.
        palavras_chave_especiais (list): Lista de palavras-chave especiais que têm prioridade.
        
    Returns:
        dict: O texto com o melhor ranking que contém todas as palavras-chave e, se aplicável, as palavras-chave especiais.
    """
    for resultado in textos_rankeados:
        texto = resultado['texto']
        
        if encontrar_melhor_resultado(texto, palavras_chave, palavras_chave_especiais):
            return resultado
    return None

def identificar_tipo_pergunta(conteudo):
    """
    Identifica padrões de perguntas no conteúdo para refinar a extração de palavras-chave.
    Args:
        conteudo (str): O conteúdo textual a ser analisado.
    Returns:
        bool: Retorna True se o padrão indicar uma pergunta específica, False caso contrário.
    """
    # Detecta padrões comuns de perguntas relacionadas a eventos históricos, biográficos, criação e atributos
    padrao_pergunta = re.search(r'\b(qual|quanto|como|preço|custa|valor|idade|altura|nascimento|morreu|falecimento|fundação|criação|origem|nasceu|ano|história|fundou|criou|criador|inventou|invenção|descobriu|descoberta)\b', conteudo.lower())
    return bool(padrao_pergunta)

def palavras_chave_especiais(conteudo, num_palavras=10):
    """
    Gera uma lista de palavras-chave mais relevantes a partir do conteúdo do texto,
    priorizando palavras de atributos importantes se forem encontradas.
    
    Args:
        conteudo (str): O conteúdo textual a ser analisado.
        num_palavras (int): Número de palavras-chave a serem retornadas.
    
    Returns:
        list: Lista das palavras-chave mais relevantes.
    """
    
    # Tokeniza o conteúdo e remove pontuação e stopwords
    tokens = word_tokenize(conteudo.lower())
    stop_words = set(stopwords.words('portuguese'))
    palavras = [word for word in tokens if word.isalpha() and word not in stop_words]

    # Lista de palavras que têm maior prioridade (palavras de atributos)
    palavras_de_atributos = ['idade', 'nascimento', 'altura', 'peso', 'preço', 'custo', 'valor', 'custa', 'tarifa', 
                             'taxa', 'quantia', 'ano', 'nasceu', 'morreu', 'fundação', 'criação', 'origem', 
                             'falecimento', 'fundou', 'história', 'criou', 'criador', 'inventou', 'invenção', 
                             'descobriu', 'descoberta', 'fundador', 'inovação']

    if identificar_tipo_pergunta(conteudo):
        palavras = [word for word in palavras if word in palavras_de_atributos or word.isalpha()]

    if not palavras:
        return []

    vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    X = vectorizer.fit_transform([' '.join(palavras)])
    
    tfidf_scores = dict(zip(vectorizer.get_feature_names_out(), X.toarray()[0]))
    palavras_chave = sorted(tfidf_scores, key=tfidf_scores.get, reverse=True)[:num_palavras]

    # Se houver palavras prioritárias (como 'preço', 'valor', 'nasceu'), priorizá-las
    palavras_chave_prioritarias = [word for word in palavras_chave if word in palavras_de_atributos]
    if palavras_chave_prioritarias:
        return palavras_chave_prioritarias

    return palavras_chave

def gerar_palavras_chave(pergunta):
    """
    Gera palavras-chave relevantes de uma pergunta.
    Se 'pergunta' for uma lista, converte para string antes de processar.
    """
    if isinstance(pergunta, list):
        pergunta = ' '.join(pergunta)

    palavras = word_tokenize(pergunta.lower())
    palavras_chave = [palavra for palavra in palavras if palavra.isalnum() and palavra not in stop_words]

    return palavras_chave

def extrair_texto(soup):
    textos = []
    
    for tag in ['h1', 'h2', 'h3', 'p']:
        for elemento in soup.find_all(tag):
            textos.append(elemento.get_text(strip=False))

    texto_final = '\n\n'.join(textos)
    return texto_final

def buscar_sites_google(query, num_resultados=50):
    """Realiza uma busca no Google e retorna uma lista de URLs relevantes de forma síncrona."""
    resultados = []
    url = f"https://www.google.com/search?q={query}&num={num_resultados}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for result in soup.find_all('a'):
            href = result.get('href')
            if href and '/url?q=' in href:
                link = href.split('/url?q=')[1].split('&')[0]
                if "google.com" not in link and link.startswith('http'):
                    resultados.append(link)

    except requests.RequestException as e:
        print(f"Erro ao buscar sites: {e}")

    return resultados

def executar_scraping(pergunta, imprimir=False):
    """
    Função central para executar o scraping baseado na pergunta do usuário.

    Args:
        pergunta (str): A pergunta que o usuário deseja investigar.
        imprimir (bool): Se True, imprime os resultados no terminal. Se False, apenas retorna os resultados.

    Returns:
        None
    """
    if not pergunta:
        if imprimir:
            print("Entrada vazia, tente novamente.")
        return

    palavras = gerar_palavras_chave(pergunta)
    if not palavras:
        if imprimir:
            print("Nenhuma palavra-chave gerada.")
        return

    links = buscar_sites_google(pergunta)
    if not links:
        if imprimir:
            print("Nenhum link encontrado para a pesquisa.")
        return

    resposta_site = processar_links(links)

    if resposta_site and isinstance(resposta_site, list):
        conteudo_extraido = []

        for link, conteudo in zip(links, resposta_site):
            if conteudo:
                time.sleep(1)
                conteudo_extraido.append({'link': link, 'conteudo': conteudo})

        return rankear_resultados(pergunta, palavras, conteudo_extraido, exibir_impressao=imprimir)
    else:
        if imprimir:
            print("Nenhum conteúdo encontrado nos sites.")

def checar_similaridade(pergunta, conteudo_site):
    """Calcula a similaridade entre a pergunta e o conteúdo do site."""
    return difflib.SequenceMatcher(None, pergunta, conteudo_site).ratio()

def scarping_init():
    while True:
        pergunta = input("\033[1;36mScarping[0@/ Prompt\033[m: ")
        if pergunta in ["99", "exit", "sair", "goingout", "logout"]:
            print("logout popup byee!")
            time.sleep(1.0)
            sys.exit()

        if not pergunta:
            print("Entrada vazia, tente novamente.")
            continue

        palavras = gerar_palavras_chave(pergunta)

        if not palavras:
            print("Nenhuma palavra-chave gerada.")
            continue

        print(f"Palavras-chave: {palavras}")

        links = buscar_sites_google(pergunta)

        if not links:
            print("Nenhum link encontrado para a pesquisa.")
            continue

        resposta_site = processar_links(links)

        if resposta_site and isinstance(resposta_site, list):
            conteudo_extraido = []

            for link, conteudo in zip(links, resposta_site):
                if conteudo:
                    print(f"Acessando: {link}")
                    time.sleep(1)
                    conteudo_extraido.append({'link': link, 'conteudo': conteudo})
                else:
                    continue

            # Chamada corrigida da função rankear_resultados
            limitar_resposta(rankear_resultados(pergunta, palavras, conteudo_extraido), pergunta)

            scarping_init()
        else:
            print("Nenhum conteúdo encontrado nos sites.")

if __name__ == "__main__":
    scarping_init()