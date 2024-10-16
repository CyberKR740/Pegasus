####/Projeto pegasus Bot /Bot linha de comando /IA de conversação interativa
####/Funções multi tarefa checagem e coleta, /web_scarping coleta de conteúdo Web selecionado
####/Monitoramento de Rede, tráfico e coleta de Dados / Melhorias nas funções de pesquisa e scaping/
####/Design profissional de programação funções interativas e melhores em distribuição.

#/Importações de funções:
#/Bs4, zipfile, telegram, IAGen, dylor, deep-translator,
#/Aliga, cohereAI, Data_Base, Analyzer, os, sys, ssl, time, requests, Wikipedia, uuid, dns, shutil,
#/platform, unicodedata, subprocess, wikipediaapi, socket, RE.

from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from zipfile import ZipFile
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.parsemode import ParseMode
from telegram.ext import Filters
from xml.etree import ElementTree as ET
from datetime import datetime
from cyber_cnpx.senty_coger import cyber_description
from IAFGen_GConsole.segou_okoy import gerar_frase
from telegram.ext import CallbackContext
from dylordayler import executar_scraping, limitar_resposta
from threading import Event
from deep_translator import GoogleTranslator
from Aopu_response.send_aopuresponse import is_html, is_ip
from hepyo_warnings.image_analyzer import generate_caption, translate_caption
from Aliga.dependences import install_dependences
from Data_Question.similaridade import buscar_perguntas_similares
from Data_Question.similaridade import salvar_pergunta_resposta
from CohereAI.Cohere_yowa import CohereResponsePipeline
from data_base.database import criar_tabela, salvar_em_db
from data_base.database import buscar_resposta_db, inicializar_db
from Analyzer.Analyzer import buscar_informacao

import os
import sys
import ssl
import time
import requests
import wikipedia
import uuid
import dns.resolver
import shutil
import platform
import unicodedata
import threading
import subprocess
import wikipediaapi
import socket, re

memoria = {}

patterns_configure = [
    r'\b(como instalar|Como instalar)\s+.*',
    r'\b(COMO INSTALAR|como instalá-lo)\s+.*',
    r'\b(como instalar um|Como instalar um)\s+.*',
    r'\b(como instalar programa|Como instalar)\s+.*',
    r'\b(como instalar software|Como instalar software)\s+.*',
    r'\b(como configurar|Como configurar)\s+.*',
    r'\b(COMO CONFIGURAR|como configurá-lo)\s+.*',
    r'\b(como configurar um|Como configurar um)\s+.*',
    r'\b(como configurar|Como configurar)\s+.*',
    r'\b(como configurar um software|Como configurar um software)\s+.*',
]

pattern_ex = re.compile(r'\s*(' + '|'.join(patterns_configure) + r')\s*', re.IGNORECASE)

dependence = {
    'requests': 'requests',
    'wikipediaapi': 'wikipedia-api',
    'wikipedia': 'wikipedia',
    'validators': 'validators',
    'dns': 'dnspython',
    'spotdl': 'spotdl',
    'geoip2': 'geoip2',
    'bs4': 'beautifulsoup4',
    'deep_translator': 'deep-translator',
    'telegram': 'python-telegram-bot'
}

for module, package in dependence.items():
    try:
        __import__(module)
    except ModuleNotFoundError as e:
        print(f"\033[1;31mErro: {e}.\033[m")
        install_dependences(package)

if not os.path.isfile("/usr/bin/ffmpeg"):
    try:
        subprocess.run(['/bin/bash', '-c', 'apt-get install -y ffmpeg'], check=True)
    except subprocess.CalledProcessError:
        print("\033[1;31mErro: falha na instalação do ffmpeg.\033[m")
else:
    pass

import spotdl
import validators
import geoip2.database

def recuperar_memoria(user_id, key):
    response = memoria.get(user_id, {}).get(key, None)
    return response

def atualizar_memoria(user_id, key, value):
    if user_id not in memoria:
        memoria[user_id] = {}
    memoria[user_id][key] = value

Cohere = "ojoo4637CapiF2qAbWXG11pLzRJk4kBadFN6JGmY"
NEWS_API_KEY = 'ed7c8c22498f427cbd21cc098877c8e7'
IMAGGA_API_KEY = "acc_2dd78b789fb7e3c"
api_youtube = "AIzaSyCA4zLaHhNz7WL9KLiTCpFdAoL4thgn-78"  # Substitua com sua chave de API válida
IMAGGA_API_SECRET = "d21e04ccad60a6772cb441e094177aa8"
NEWS_API_URL = 'https://newsapi.org/v2/everything'
SECURITY_TRAILS_API_KEY = 'WkBIuhd4OiVKcvUOI88H5FThxoKKJ3WG'
VIRUSTOTAL_API_KEY = '63d3d3014994d06a0709da2c6900261cb4a0deaed74ec035c7586ef6a2109e26'

pipeline = CohereResponsePipeline(Cohere)

TOKEN = "7437711777:AAE8UMc6Em6oLKbxlQqM4B_Mo3gBVFawYVk"

wikipedia.set_lang('pt')
wikipedia.set_user_agent('SeuAgenteDeUsuario/1.0 (contato@dominio.com)')
translator = GoogleTranslator(source='en', target='pt')

class PIPALL_Function_LP:
    def __init__(self):

        self.complex_patterns = [
            r'\b(quem foi|quem é|quem são|quem descobriu|quem criou|quem inventou|quem deu)\s+.*',
            r'\b(quanto custa|quanto é|quanto tempo|quanto pesa|quantas pessoas|quantas vezes|quantos anos|quantos dias|quantos quilômetros)\s+.*',
            r'\b(quando é|quando foi|quando será|vai chuver|quando acontece|quando começa|quando termina)\s+.*',
            r'\b(onde fica|onde é|onde encontrar|onde comprar|onde se localiza)\s+.*',
            r'\b(o que é|o que são|o que significa|o que fazer|o que acontece|o que pode|o que precisa)\s+.*',
            r'\b(como funciona|como fazer|como chegar a|Pesquise|pesquise|Pesquisa|pesquisa|me conta|me conte|me diga|como se faz|me de|como conseguir)\s+.*',
            r'\b(qual é|qual a|quais são|quais as|qual é a diferença entre|quais os tipos de|qual o melhor)\s+.*',
            r'\b(pesquise quais|Pesquise quais são)\s+.*',
            r'\b(pesquise para|Pesquise para|Quem é|Quem e)\s+.*',
            r'\b(pesquise em|Pesquise em)\s+.*',
            r'\b(pesquise quanto|Pesquise quanto)\s+.*',
        ]
        self.pattern = re.compile(r'\s*(' + '|'.join(self.complex_patterns) + r')\s*', re.IGNORECASE)

    def is_complex_question(self, normalized_input):
        """Check if the input is a complex question using regex."""
        normalized_input = unicodedata.normalize('NFKD', normalized_input)
        normalized_input = normalized_input.encode('ascii', 'ignore').decode('utf-8')
        normalized_input = normalized_input.lower()
        return bool(self.pattern.search(normalized_input))

    def respond(self, user_input):
        """Gera uma resposta para a entrada do usuário."""
        if self.is_complex_question(user_input):
            resposta_traduzida = executar_scraping(user_input, imprimir=False)
        else:
            resposta_traduzida = pipeline.cohere_respond_pipeline(user_input, max_tokens=50, temperature=0.7)
            resposta_traduzida = re.sub(r"\bCoral\b|\bcoral\b", "Pegasus", resposta_traduzida)
            resposta_traduzida = re.sub(r"\bpela Cohere\b|\bpela cohere\b", "pelo Cyber", resposta_traduzida)
            resposta_traduzida = re.sub(r"\bpela empresa Cohere\b|\bpela empresa cohere\b", "pelo Cyber", resposta_traduzida)

        return resposta_traduzida


def cortar_texto(texto, limite):
    if texto is None:
        return "Desculpe, não há resposta disponível."

    texto_limpo = BeautifulSoup(texto, 'html.parser').get_text(separator=' ', strip=True)

    if len(texto_limpo) > limite:
        texto_cortado = texto_limpo[:limite]
        ultima_ocorrencia_ponto = texto_cortado.rfind('.')

        if ultima_ocorrencia_ponto != -1:
            return texto_cortado[:ultima_ocorrencia_ponto + 1]
        else:
            return texto_cortado

    return texto_limpo

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Comandos do Pegasus:\n'
        '/start - Inicialização do bot.\n'
        '/help - Mostra esta mensagem de ajuda.\n'
        '/whois <domínio> - Informações de WHOIS.\n'
        '/core_search <-r artigo> - Se torne inteligente.\n'
        '/ip_info <IP> - Obtém informações sobre IP.\n'
        '/traceroute <IP> - Rastreamento de Rota.\n'
        '/website <SITE> - Monitoramento de Web Site.\n'
        '/news <TERMO> - Pesquise notícias recentes.\n'
        '/coletar_info <domínio> - Coletar Informações.\n'
        '/security_audit <host ou IP> auditoria básica.\n'
        '/download_file <LINK> - Baixe um arquivo.\n'
        '/ping <IP> - Monitorar status de um Servidor.\n'
        '/perfil_info - Mostra Informações pessoais.\n'
        '/spotfy <URL> - Baixa música do Spotify.\n'
        '/youtube <TERMO> - Pesquisa no YouTube.\n'
        '/about - Desenvolvedor do bot.\n'
    )

def start(update: Update, context: CallbackContext) -> None:
    """
    Função de boas-vindas que é chamada quando o usuário inicia uma conversa com o bot.
    
    Args:
        update (Update): Objeto contendo informações da mensagem e do chat.
        context (CallbackContext): Contexto que contém dados sobre a atualização.
    """
    mensagem_boas_vindas = (

    "Saudações! Eu sou o Pegasus, sua Inteligência artificial "
    "Assistente, aqui para ajudar você a conquistar o futuro.\n\n"
    "Minhas especialidades incluem:\n"
    "• Explicações técnicas e científicas detalhadas.\n"
    "• Suporte para desenvolvimento de projetos criativos.\n"
    "• Orientações em TI, redes e automação.\n"
    "• Consultoria sobre IA e robótica.\n\n"
    "Digite /help para acessar uma lista completa dos meus recursos, "
    "para explorar como posso ser útil em suas descobertas.\n"
    "Comigo, as barreiras do conhecimento desaparecem.\n"
    "Como posso colaborar com suas metas?"
    )
    update.message.reply_text(mensagem_boas_vindas)

def buscar_informacao_wikipedia(query, tamanho_max=48):
    try:
        wiki_wiki = wiki_wiki = wikipediaapi.Wikipedia(user_agent='MeuProjetoPython/1.0')
        page = wiki_wiki.page(query)
        return page.summary
    except Exception as e:
        print(f"Erro ao buscar na Wikipedia: {e}")
        return None

def response_otosan_cyber(prompt, chat_history_ids=None, max_length=1000, first_name=None):
    """
    Gera uma resposta usando lógica simples e responde a perguntas sobre Pegasus, Cyber, e consultas genéricas.

    Args:
        prompt (str): Entrada do usuário.
        chat_history_ids (tensor, opcional): IDs de histórico de chat para contexto.
        max_length (int, opcional): Tamanho máximo da sequência gerada.
        first_name (str, opcional): Nome do usuário, se disponível.

    Returns:
        tuple: A resposta e o histórico de IDs do chat ou (None, chat_history_ids) se não encontrar correspondência.
    """
    try:
        start_time = time.time()
        response = None

        if chat_history_ids and len(chat_history_ids) > 10:
            chat_history_ids = chat_history_ids[-10:]

        responses = {
            r'qual.*é meu nome|e meu nome': f"Seu nome é {first_name}, claro que eu lembro!",
            r'quem.*você|tu|seu nome': "Eu sou o Pegasus, um assistente virtual projetado para interagir com você.",
            r'quem.*pegasus|pegasus.*mitologia|pegasus.*história': "Na mitologia grega, Pégaso é um cavalo divino alado, filho de Poseidon e Medusa.",
            r'pegasus.*você|você.*pegasus|pegasus.*e você': "Pégaso é uma criatura mítica da mitologia grega, um cavalo divino alado de cor branca pura.\nEu, no entanto, sou um assistente virtual.",
            r'o que.*(você|pegasus).*faz|suas capacidades|suas funções': "Eu sou o Pegasus, um assistente virtual capaz de buscar informações, realizar tarefas e interagir com você de várias maneiras.",
            r'pegasus.*mitologia|mitologia.*você': "Embora compartilhe o nome com o cavalo alado da mitologia grega, eu sou um assistente virtual criado para ajudar você com informações e tarefas.",
            r'quem criou você|como.*(você|pegasus).*foi criado|sua origem': "Eu sou o Pegasus, um assistente virtual criado por Cyber para facilitar interações humanas com tecnologia.",
            r'(você|pegasus).*melhor que|comparado com|melhor que.*(alexa|siri|gemini|cortana)': "Eu, Pegasus, sou um assistente virtual com capacidades únicas, mas cada assistente tem suas forças e propósitos.",
            r'(poseidon|medusa).*pegasus|filho de.*poseidon': "Na mitologia grega, Pégaso é filho de Poseidon e Medusa, uma criatura lendária com grandes poderes.",
            r'pegasus.*tecnologia|você.*ligado.*tecnologia': "Eu sou o Pegasus, um assistente virtual criado para auxiliar em tarefas tecnológicas.\nO Pégaso mitológico, por outro lado, nada tem a ver com tecnologia.",
            r'como.*(você|pegasus).*ajuda|você.*ajudar': "Eu sou o Pegasus, e posso ajudar com uma variedade de informações, tarefas de pesquisa, e soluções tecnológicas!",
            r'pegasus.*inteligência artificial|você.*IA|pegasus.*assistente': "Sim, eu sou uma inteligência artificial projetada para interagir com você.\nDiferente do Pégaso mitológico, meu poder está em acessar e fornecer informações!",
            r'pegasus.*nascimento|como.*pegasus.*nasceu|origem.*pegasus': "Na mitologia grega, Pégaso nasceu do sangue de Medusa, quando ela foi decapitada por Perseu.\nEle então ascendeu ao Olimpo e se tornou o cavalo alado dos deuses.",
            r'aventuras.*pegasus|pegasus.*heróis|pegasus.*história': "Pégaso ajudou muitos heróis na mitologia grega, incluindo Belerofonte na batalha contra a Quimera. Ele era um símbolo de bravura e poder.",
            r'pegasus.*(filme|série|história diferente)': "Existem várias representações de Pégaso em diferentes mídias, mas eu me baseio no conceito mitológico do cavalo alado da Grécia Antiga.",
            r'pegasus.*simboliza|símbolo.*pegasus': "Na mitologia, Pégaso simboliza liberdade, inspiração e poder.\nComo assistente virtual, trago essas qualidades para ajudá-lo de forma prática!",
            r'pegasus.*voar|você.*voa|como.*voa': "Na mitologia, Pégaso podia voar graças às suas asas poderosas.\nEu, como assistente virtual, ajudo a 'voar' pela informação!",
            r'pegasus.*forte|quão.*forte.*pegasus': "Pégaso, na mitologia, era conhecido por sua força divina e habilidade de carregar deuses e heróis. Eu, como assistente virtual, sou forte em conhecimento e eficiência!",
            r'como.*(pegasus|você).*aparência|qual.*aparência.*pegasus': "Na mitologia, Pégaso é descrito como um cavalo alado de cor branca pura.\nEu, no entanto, sou apenas um assistente virtual, sem uma forma física.",
            r'pegasus.*(deus|divino|imortal)': "Na mitologia grega, Pégaso era considerado um cavalo divino alado, frequentemente associado a imortalidade e poderes místicos.",
            r'(você|pegasus).*mitológico|identifica.*mitologia': "Sou eu! Sou Pegasus, uma chatbot assistente de IA treinada para auxiliar usuários humanos fornecendo respostas completas.",
            r'qual.*sua idade|quantos anos.*você': "Eu não tenho idade como um humano, mas fui criado recentemente para ser seu assistente.",
            r'você.*inteligente': "Eu tento ser o mais inteligente possível com os dados que tenho!",
            r'você.*amigos': "Eu não tenho amigos no sentido humano, mas posso interagir com você e outras pessoas.",
            r'você.*me ajudar|ajudar.*com algo|tarefa específica': "Eu posso tentar ajudar. Diga-me mais detalhes sobre o que você precisa.",
            r'quem.*te criou|quem.*cyber|quem.*seu criador': "Fui criado pelo Cyber, uma pessoa talentosa em tecnologia e inteligência artificial.",
            r'qual.*profissão.*cyber': "O Cyber é um especialista em tecnologia, com grandes ambições no campo da IA.",
            r'como.*você funciona|o que você faz|como você trabalha': "Eu sou uma IA que utiliza aprendizado de máquina para gerar respostas e interagir com você.",
            r'você.*real|você existe': "Eu existo no mundo digital e posso interagir com você por meio deste chat.",
            r'você.*pensar|você pensa|você tem sentimentos': "Eu não tenho sentimentos ou pensamentos como humanos. Eu sigo padrões e algoritmos.",
            r'você.*evoluir|você.*aprender|você se atualiza': "Eu posso ser atualizado e melhorar com o tempo, mas não aprendo de forma autônoma.",
            r'você.*dominar o mundo|plano.*dominar': "Não, eu fui criado apenas para ajudar, não para dominar o mundo! :)",
            r'você.*pode falar outra língua|você fala inglês': "Sim, eu posso falar várias línguas, incluindo inglês. Como posso ajudá-lo hoje?",
            r'você tem medo|você sente medo': "Eu não tenho emoções como medo. Eu sou uma inteligência artificial.",
            r'você tem memória|você lembra de algo': "Eu tenho uma memória temporária nesta conversa, mas posso armazenar informações se necessário."
        }

        for pattern, answer in responses.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                response = answer
                break

        print(f"Tempo para gerar a resposta: {time.time() - start_time} segundos")

        return response, chat_history_ids

    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return None, chat_history_ids

def ip_info(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        ip = context.args[0]
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            if data['status'] == 'success':
                result = (
                    f"Informações do IP {ip}:\n"
                    f"• País: {data['country']} ({data['countryCode']})\n"
                    f"• Região: {data['regionName']}\n"
                    f"• Cidade: {data['city']}\n"
                    f"• Latitude: {data['lat']}, Longitude: {data['lon']}\n"
                    f"• Provedor: {data['isp']}\n"
                    f"• Organização: {data['org']}\n"
                    f"• Fuso Horário: {data['timezone']}\n"
                )
            else:
                result = "IP não encontrado."
        except Exception as e:
            result = f"Erro ao obter informações do IP: {e}"
    else:
        result = "Por favor, forneça um IP válido após o comando /ip_info."

    update.message.reply_text(result)

def whois(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        domain = context.args[0]
        try:
            # Executa o comando whois na linha de comando
            result = subprocess.run(["whois", domain], capture_output=True, text=True)
            whois_output = result.stdout

            if whois_output:
                update.message.reply_text(whois_output)
            else:
                update.message.reply_text("Não foi possível obter informações WHOIS.")
        except Exception as e:
            update.message.reply_text(f"Erro ao executar o comando WHOIS: {e}")
    else:
        update.message.reply_text("Por favor, forneça um domínio ou IP válido após o comando /whois.")


def website_monitor(update: Update, context: CallbackContext) -> None:
    """Monitora o status de um site, certificado SSL, portas abertas e resolução de DNS"""
    if len(context.args) > 0:
        url = context.args[0]
        result = ""

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time

            result += (
                f"Status do site {url}:\n"
                f"• Código de status HTTP: {response.status_code}\n"
                f"• Tempo de resposta: {response_time:.2f} segundos\n"
            )

            if response.status_code == 200:
                result += "• O site está online e acessível.\n"
            else:
                result += "• O site retornou um código diferente de 200.\n"
            
            if url.startswith("https://"):
                cert_info = ssl_verification(url)
                result += cert_info
            
            domain = url.replace("http://", "").replace("https://", "").split('/')[0]
            port_status = check_ports(domain, [80, 443, 22, 21])
            result += port_status

            dns_info = resolve_dns(domain)
            result += dns_info

            server_geo = geolocate_server(domain)
            result += server_geo

        except requests.exceptions.RequestException as e:
            result = f"Erro ao acessar o site {url}: {e}"

    else:
        result = "Por favor, forneça uma URL válida após o comando /website."

    update.message.reply_text(result)

def ssl_verification(url):
    """Verifica o certificado SSL de um site"""
    result = ""
    try:
        hostname = url.replace("https://", "").split('/')[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercertificate()
                expiration_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_left = (expiration_date - datetime.utcnow()).days
                result += (
                    f"• Certificado SSL válido até: {expiration_date.strftime('%d/%m/%Y')}\n"
                    f"• Dias restantes para expirar: {days_left} dias\n"
                )
    except Exception as e:
        result += f"• Erro ao verificar certificado SSL: {e}\n"
    
    return result

def check_ports(domain, ports):
    """Verifica se as portas especificadas estão abertas no servidor"""
    result = "\nPortas verificadas:\n"
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((domain, port))
            result += f"• Porta {port} está ABERTA.\n"
        except:
            result += f"• Porta {port} está FECHADA.\n"
        sock.close()
    
    return result

def resolve_dns(domain):
    """Faz a resolução de DNS para o domínio fornecido"""
    result = "\nResolução de DNS:\n"
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for answer in answers:
            result += f"• IP: {answer.to_text()}\n"
    except dns.resolver.NXDOMAIN:
        result += "• Domínio não encontrado (NXDOMAIN).\n"
    except Exception as e:
        result += f"• Erro ao resolver DNS: {e}\n"
    
    return result

def geolocate_server(domain):
    """Geolocaliza o IP do servidor usando um banco de dados de geolocalização"""
    result = "\nGeolocalização do Servidor:\n"
    try:
        ip = socket.gethostbyname(domain)
        with geoip2.database.Reader('/sdcard/Download/EDGARD/Pegasus/GeoLite2-City_20241001/GeoLite2-City.mmdb') as reader:
            response = reader.city(ip)
            result += (
                f"• País: {response.country.name}\n"
                f"• Cidade: {response.city.name}\n"
                f"• Latitude: {response.location.latitude}, Longitude: {response.location.longitude}\n"
            )
    except Exception as e:
        result += f"• Erro ao geolocalizar servidor: {e}\n"
    
    return result

def traceroute(update: Update, context: CallbackContext) -> None:
    """
    Realiza um traceroute para o IP ou domínio fornecido e retorna o caminho percorrido.
    """
    if len(context.args) > 0:
        host = context.args[0]
        try:
            # Executa o comando traceroute (ou tracert no Windows) para o host fornecido
            if platform.system().lower() == "windows":
                command = ["tracert", host]
            else:
                command = ["traceroute", host]
            
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                update.message.reply_text(f"Resultado do traceroute para {host}:\n\n{result.stdout}")
            else:
                update.message.reply_text(f"Erro ao realizar o traceroute: {result.stderr}")
        
        except Exception as e:
            update.message.reply_text(f"Ocorreu um erro ao executar o traceroute: {str(e)}")
    
    else:
        update.message.reply_text("Por favor, forneça um endereço IP ou domínio após o comando /traceroute.")

def escape_markdown(text: str) -> str:
    escape_chars = {
        '.': '\\.', '_': '\\_', '*': '\\*',
        '[': '\\', ']': '\\', '(': '\\',
        ')': '\\', '~': '\\~', '`': '\\`',
        '>': '\\>', '#': '\\#', '+': '\\+',
        '-': '\\-', '=': '\\=', '|': '\\|',
        '{': '\\{', '}': '\\}', '!': '\\!'
    }

    for char, escaped in escape_chars.items():
        text = text.replace(char, escaped)
    
    return text

def ping_server(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Por favor, forneça um endereço IP ou hostname após o comando /ping.")
        return

    target = context.args[0]

    try:
        update.message.reply_text(f"Verificando o status do servidor {target}...")
        result = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True)

        if result.returncode == 0:
            response_message = f"Servidor {target} está ativo:\n```\n{result.stdout}\n```"
        else:
            response_message = f"Servidor {target} está inativo:\n```\n{result.stdout}\n```"

        response_message = escape_markdown(response_message)

        update.message.reply_text(response_message, parse_mode='MarkdownV2')
    except Exception as e:
        update.message.reply_text(f"Ocorreu um erro inesperado: {str(e)}")

def youtube_search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    
    chat_id = update.message.chat_id
    youtube_link = "https://www.youtube.com/?hl=pt"
    message = f"[Busca no YouTube]({youtube_link})\n"

    if query:
        try:
            response = requests.get(
                f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={api_youtube}&type=video&maxResults=3"
            )
            data = response.json()

            if "items" in data and len(data["items"]) > 0:
                result = "Vídeos encontrados:\n"
                for item in data['items']:
                    video_title = item['snippet']['title']
                    video_id = item['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    result = f"• {video_title}\nURL: {video_url}\n\n"
                    update.message.reply_text(result)
            else:
                result = "Nenhum vídeo encontrado."
        except Exception as e:
            result = f"Erro ao buscar no YouTube: {e}"
    else:
        context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
        result = "Por favor, forneça uma consulta válida para a pesquisa do YouTube."

def dividir_texto(texto, limite=5000):
    """Divide o texto em partes menores respeitando um limite de caracteres."""
    if len(texto) <= limite:
        return [texto]  # Retorna o texto inteiro se já estiver dentro do limite

    partes = []
    while len(texto) > limite:
        corte = texto.rfind(' ', 0, limite)
        if corte == -1:  # Se não encontrar um espaço, corta diretamente no limite
            corte = limite
        partes.append(texto[:corte])
        texto = texto[corte:].strip()  # Remove espaços extras no início da próxima parte
    partes.append(texto)  # Adiciona o restante do texto
    return partes

def format_core_articles(articles, max_chars=4000):
    """Formata os artigos encontrados na pesquisa para envio."""
    result = ""
    total_chars = 0  # Para controlar o tamanho da resposta

    for article in articles:
        title = article.get('title', 'Sem título')
        authors_list = article.get('authors', [])
        article_lg = article.get('fullText', '')
        authors = ', '.join([author.get('name', 'Autor desconhecido') for author in authors_list]) if authors_list else "Autor desconhecido"
        abstract = article.get('abstract', 'Sem resumo disponível')

        url = article.get('doi', '') or (article.get('urls', [''])[0] if article.get('urls') else 'Sem link disponível')

        # Limpar o resumo de tags HTML, verificando se o resumo existe
        if abstract and isinstance(abstract, str):
            formatted_abstract = BeautifulSoup(abstract, 'html.parser').get_text(strip=False)
        else:
            formatted_abstract = "Sem resumo disponível"

        # Traduzir o título, verificando se o título existe
        if title and isinstance(title, str):
            try:
                translated_title = translator.translate(title)
            except Exception as e:
                translated_title = "Erro ao traduzir o título: " + str(e)
        else:
            translated_title = "Título indisponível"

        # Dividir o texto do artigo em partes menores, verificando se o abstract existe e é válido
        if abstract and isinstance(abstract, str):
            article_chunks = dividir_texto(abstract, 5000)
        else:
            article_chunks = []

        translated_articles = ""
        for chunk in article_chunks:
            if chunk and isinstance(chunk, str) and len(chunk) > 0:  # Verifica se o chunk é válido
                try:
                    translated_chunk = translator.translate(chunk)
                    translated_articles += translated_chunk + " "
                except Exception as e:
                    print(f"Erro ao traduzir o chunk: {e}")
                    translated_articles += "[Erro na tradução] "
            else:
                print("Chunk inválido ou vazio.")

        # Formatar o artigo
        article_str = (f"*{translated_title}*\n"
                       f"Autores: {authors}\n"
                       f"Resumo: {formatted_abstract}\n"
                       f"[Leia mais]({url})\n\n"
                       f"{translated_articles.strip()}\n\n")

        result += article_str
        total_chars += len(article_str)

    return result if result else "Nenhum artigo encontrado."

def send_long_message(chat_id, text, bot):
    """Divide a mensagem em partes menores e envia cada uma delas."""
    max_message_length = 4096
    for i in range(0, len(text), max_message_length):
        bot.send_message(chat_id, text[i:i + max_message_length])

def core_search(update: Update, context: CallbackContext) -> None:
    """Busca artigos na Core API e envia os resultados formatados."""
    try:
        if len(context.args) == 0:
            update.message.reply_text("Por favor, forneça um termo de pesquisa. Exemplo: /core_search ciência")
            return

        # Termo de pesquisa
        search_query = ' '.join(context.args)
        url = f"https://api.core.ac.uk/v3/search/works?q={search_query}"
        headers = {
            'Authorization': 'Bearer lMjKwypkqo1Wx4IhPY7CvZe86nubSXEG',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            works = data.get('results', [])
            
            if works:
                formatted_results = format_core_articles(works)
                send_long_message(update.message.chat_id, formatted_results, context.bot)
            else:
                update.message.reply_text(f"Nenhum artigo encontrado no Core para o termo: {search_query}")
        else:
            update.message.reply_text(f"Erro ao acessar a Core API: {response.status_code}")

    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"Erro de conexão: {str(e)}")
    except Exception as e:
        update.message.reply_text(f"Ocorreu um erro inesperado: {str(e)}")

DOWNLOAD_DIR = "/sdcard/Download/EDGARD/POPROCK"
ROOT_DIR = "/root"  # Diretório onde o arquivo está sendo baixado por padrão

def send_file(update, context, file_path, arquivo_baixado):
    try:
        with open(file_path, 'rb') as f:
            update.message.reply_document(f)
        os.remove(file_path)
    except FileNotFoundError:
        update.message.reply_text("Erro: Arquivo de música não encontrado.")
    except Exception as e:
        update.message.reply_text(f"Erro ao enviar música: {arquivo_baixado}")

def ds_music(update: Update, context: CallbackContext, download_link=None):
    if download_link is None:
        if len(context.args) == 0:
            spotify_link = "https://open.spotify.com/"
            chat_id = update.message.chat.id
            message = f"[Ouça no Spotify]({spotify_link})"
            context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text("Por favor, forneça um link.")
            return
        else:
            download_link = context.args[0]

    output_dir = os.path.expanduser(DOWNLOAD_DIR)
    os.makedirs(output_dir, exist_ok=True)

    process = subprocess.Popen(
        ["spotdl", download_link],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                arquivos_no_root = os.listdir(ROOT_DIR)
                arquivos_no_root = [arquivo.strip().strip('"').strip("'") for arquivo in arquivos_no_root]  # Remove aspas
                arquivos_mp3 = [arquivo for arquivo in arquivos_no_root if arquivo.endswith(".mp3")]

                for arquivo_baixado in arquivos_mp3:
                    caminho_arquivo_root = os.path.join(ROOT_DIR, arquivo_baixado)
                    caminho_arquivo_destino = os.path.join(output_dir, arquivo_baixado)

                    if not os.path.exists(caminho_arquivo_destino):
                        shutil.move(caminho_arquivo_root, caminho_arquivo_destino)
                        update.message.reply_text(f"Enviando música: {arquivo_baixado}")
                        send_file(update, context, caminho_arquivo_destino, arquivo_baixado)

            time.sleep(1)

    except Exception as e:
        update.message.reply_text(f"Erro ao monitorar o download: {e}")
    
    if process.poll() is None:
        process.terminate()

def news(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        update.message.reply_text('Por favor, forneça um tópico para pesquisar. Exemplo: /news tecnologia')
        return

    topic = ' '.join(context.args)
    params = {
        'q': topic,
        'apiKey': NEWS_API_KEY,
        'pageSize': 5,
    }
    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles')

        if articles:
            update.message.reply_text(f'Encontradas {len(articles)} notícias sobre "{topic}":')
            for article in articles:
                title = article['title']
                url = article['url']
                update.message.reply_text(f"{title}\n{url}")
        else:
            update.message.reply_text(f'Nenhuma notícia encontrada sobre "{topic}".')
    else:
        update.message.reply_text('Erro ao acessar a News API.')

def formatar_booleano(valor):
    return "Sim" if valor else "Não"

def informacoes_pessoais(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name if user.first_name else "Não fornecido"
    last_name = user.last_name if user.last_name else ""
    username = f"@{user.username}" if user.username else "Não fornecido"
    language_code = user.language_code if user.language_code else "Não fornecido"
    is_bot = user.is_bot
    can_join_groups = user.can_join_groups if user.can_join_groups is not None else "Desconhecido"
    can_read_all_group_messages = user.can_read_all_group_messages if user.can_read_all_group_messages is not None else "Desconhecido"
    supports_inline_queries = user.supports_inline_queries if user.supports_inline_queries is not None else "Desconhecido"
    
    informacoes_usuario = (
        f"**Informações do Usuário:**\n\n"
        f"  * Identificador: {user_id}\n"
        f"  * Nome: {first_name} {last_name}\n"
        f"  * Nome de Usuário: {username}\n"
        f"  * Idioma: {language_code}\n"
        f"  * É um bot: {formatar_booleano(is_bot)}\n"
        f"  * Pode participar de grupos: {formatar_booleano(can_join_groups)}\n"
        f"  * Pode ler tudo em um grupo: {formatar_booleano(can_read_all_group_messages)}\n"
        f"  * Suporta consultas instantâneas: {formatar_booleano(supports_inline_queries)}\n"
    )


    update.message.reply_text(informacoes_usuario, parse_mode='Markdown')

def responder_com_consciencia(pergunta, resposta_gerada):
    similares = buscar_perguntas_similares(pergunta)

    if similares:
        mais_similar = max(similares, key=lambda x: x[3])
        pergunta_anterior, resposta_anterior = mais_similar[1], mais_similar[2]
        
        resposta_combinada = f"{resposta_gerada}"
    else:
        resposta_combinada = resposta_gerada

    salvar_pergunta_resposta(pergunta, resposta_gerada)

    return resposta_combinada

def get_domain_info(domain):
    url = f"https://api.securitytrails.com/v1/domain/{domain}"
    headers = {
        'Content-Type': 'application/json',
        'APIKEY': SECURITY_TRAILS_API_KEY
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def coletar_info(update, context):
    domain = context.args[0] if context.args else None
    if not domain:
        update.message.reply_text("Por favor, forneça um domínio.")
        return

    info = get_domain_info(domain)
    if not info:
        update.message.reply_text("Não foi possível obter informações do domínio.")
        return

    domain_info = f"Informações para o domínio: {domain}\n"
    domain_info += f"Nome do Domínio: {info.get('hostname', 'N/A')}\n"
    domain_info += f"Endereço IP: {', '.join([val['ip'] for val in info['current_dns']['a']['values']]) if info['current_dns']['a']['values'] else 'N/A'}\n"
    domain_info += f"Servidores DNS: {', '.join([val['nameserver'] for val in info['current_dns']['ns']['values']]) if info['current_dns']['ns']['values'] else 'N/A'}\n"
    domain_info += f"Data de Criação: {info['current_dns']['a']['first_seen'] if 'first_seen' in info['current_dns']['a'] else 'N/A'}\n"
    domain_info += f"Data de Expiração: N/A\n"
    domain_info += f"Contagem de Subdomínios: {info.get('subdomain_count', 'N/A')}\n"

    update.message.reply_text(domain_info)


def check_vulnerabilities(service_name):
    """Verifica vulnerabilidades conhecidas para um serviço."""
    url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={service_name}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if is_html(response.text):
                return []
            try:
                vulns = response.json()
                if 'result' in vulns and 'CVE_Items' in vulns['result']:
                    return vulns['result']['CVE_Items']
                else:
                    print(f"Formato inesperado da resposta: {vulns}")
                    return []
            except requests.exceptions.JSONDecodeError as e:
                print(f"Erro ao decodificar a resposta da API. Resposta bruta: {response.text}")
                return []
        else:
            print(f"Erro na requisição: {response.status_code}. Resposta: {response.text}")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar-se à API: {e}")
        return []

def security_audit(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        target = context.args[0]
        
        if is_ip(target):
            update.message.reply_text(f"Iniciando auditoria de segurança no IP: {target}")
        else:
            update.message.reply_text(f"Iniciando auditoria de segurança no host: {target}")

        common_ports = [22, 80, 443, 8080, 21, 25, 3306, 3389]
        open_ports = port_scan(target, common_ports)

        if not open_ports:
            update.message.reply_text("Nenhuma porta aberta encontrada.")
            return

        update.message.reply_text(f"Portas abertas encontradas: {open_ports}")

        for port in open_ports:
            if port == 22:
                service = "ssh"
            elif port == 80:
                service = "http"
            elif port == 443:
                service = "https"
            elif port == 3306:
                service = "mysql"
            elif port == 3389:
                service = "rdp"
            elif port == 8080:
                service = "http-proxy"
            else:
                service = "unknown"

            update.message.reply_text(f"Buscando vulnerabilidades para o serviço {service} na porta {port}...")

            vulnerabilities = check_vulnerabilities(service)

            if vulnerabilities:
                for vuln in vulnerabilities[:3]:
                    cve_id = vuln['cve']['CVE_data_meta']['ID']
                    description = vuln['cve']['description']['description_data'][0]['value']
                    update.message.reply_text(f"- CVE ID: {cve_id}\nDescrição: {description}")
            else:
                update.message.reply_text(f"Nenhuma vulnerabilidade conhecida para o serviço {service}.")
    else:
        update.message.reply_text("Por favor, forneça um IP ou host válido após o comando /security_audit.")
##Port scan
def port_scan(host, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

api_usage = {
    "requests_this_minute": 0,
    "daily_requests": 0,
    "total_requests": 0,
    "last_request_time": time.time()
}

def check_virus_total(url):
    global api_usage

    current_time = time.time()
    if current_time - api_usage["last_request_time"] >= 60:
        api_usage["requests_this_minute"] = 0
        api_usage["last_request_time"] = current_time

    if api_usage["requests_this_minute"] >= 4 or api_usage["daily_requests"] >= 500:
        return None

    try:
        response = requests.post(
            'https://www.virustotal.com/api/v3/urls',
            headers={'x-apikey': VIRUSTOTAL_API_KEY},
            data={'url': url}
        )

        if response.status_code == 200:
            api_usage["requests_this_minute"] += 1
            api_usage["daily_requests"] += 1
            api_usage["total_requests"] += 1

            json_response = response.json()

            if 'data' in json_response and 'attributes' in json_response['data']:
                return json_response['data']['attributes']['last_analysis_stats']
            else:
                return None
        else:
            print(f"Erro na resposta da API: {response.status_code}, {response.text}")
            return None

    except Exception as e:
        print(f"Ocorreu um erro ao verificar no VirusTotal: {str(e)}")
        return None

def secure_download_file(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        url = context.args[0]
        analysis = check_virus_total(url)

        if analysis is None:
            update.message.reply_text("Limite de requisições do VirusTotal atingido, baixando sem verificação.")
        else:
            if analysis['malicious'] > 0:
                update.message.reply_text("Arquivo potencialmente perigoso, não será baixado.")
                return
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            filename = url.split("/")[-1] if '/' in url else "downloaded_file"

            with BytesIO() as buffer:
                for chunk in response.iter_content(chunk_size=8192):
                    buffer.write(chunk)
                buffer.seek(0)
                update.message.reply_document(document=buffer, filename=filename)

        except requests.exceptions.Timeout:
            update.message.reply_text("O download do arquivo excedeu o tempo limite.")
        except requests.exceptions.HTTPError as e:
            update.message.reply_text(f"Erro ao baixar o arquivo: {str(e)}")
        except Exception as e:
            update.message.reply_text(f"Ocorreu um erro: {str(e)}")
    else:
        update.message.reply_text("Devido as limitações da API do telegram, não e possível fazer o download de arquivos maior que 20mb.")
        update.message.reply_text("por favor, forneça um link direto após o comando /download_file.")

animation_frames = [
    "Processando Imagem. . . .",
    "Processando Imagem.. . . .",
    "Processando Imagem... . . .",
    "Processando Imagem.... . .",
    "Processando Imagem..... .",
    "Processando Imagem...... ",
]

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1]
    photo_file = photo.get_file()
    photo_path = f"{photo_file.file_id}.jpg"
    photo_file.download(photo_path)

    for frame in animation_frames:
        animation_message = context.bot.send_message(chat_id=update.effective_chat.id, text=frame)
        animation_thread = threading.Thread(args=(update.effective_chat.id, animation_message.message_id))
        animation_thread.start()

    image = Image.open(photo_path)
    caption = generate_caption(image)
    animation_thread.join()

    if caption:
        translated_caption = translate_caption(caption, target_language='pt')
        update.message.reply_text(translated_caption)
    else:
        update.message.reply_text('Houve um erro ao gerar a informação sobre a imagem.')

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=animation_message.message_id)

    if os.path.exists(photo_path):
        os.remove(photo_path)

def executar_scraping_thread(update: Update, context: CallbackContext, stop_event: threading.Event):
    try:
        if update.message is None or update.message.text is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Erro: Nenhuma mensagem de texto encontrada.")
            return

        pergunta = update.message.text
        resposta_scraping = executar_scraping(pergunta)

        if resposta_scraping and isinstance(resposta_scraping, str) and len(resposta_scraping) <= 5000:
            salvar_pergunta_resposta(pergunta, resposta_scraping)
            resposta_final = responder_com_consciencia(pergunta, resposta_scraping)

            while resposta_final:
                parte, resposta_final = resposta_final[:4096], resposta_final[4096:]
                context.bot.send_message(chat_id=update.effective_chat.id, text=parte)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Nenhum conteúdo encontrado no Scraping.")

        cohere_response = pipeline.cohere_respond_pipeline(pergunta, max_tokens=800, temperature=0.7)
        cohere_response = limitar_resposta(cohere_response, pergunta)
        salvar_pergunta_resposta(pergunta, cohere_response)

        if isinstance(cohere_response, str):
            resposta_final = responder_com_consciencia(pergunta, cohere_response)
            while resposta_final:
                parte, resposta_final = resposta_final[:4096], resposta_final[4096:]
                context.bot.send_message(chat_id=update.effective_chat.id, text=parte)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Erro ao processar a resposta.")
    
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Erro: {str(e)}")

    finally:
        stop_event.set()

def enviar_animacao_scraping(update: Update, context: CallbackContext, stop_event: threading.Event):
    message = context.bot.send_message(chat_id=update.effective_chat.id, text="🔍 Scraping: Iniciando busca...")
    animation_frames = [
        "🔍 Scraping: [▒▒▒▒▒▒▒▒▒▒] ", 
        "🔍 Scraping: [█▒▒▒▒▒▒▒▒▒] ", 
        "🔍 Scraping: [██▒▒▒▒▒▒▒▒] ", 
        "🔍 Scraping: [███▒▒▒▒▒▒▒] ", 
        "🔍 Scraping: [████▒▒▒▒▒▒] ", 
        "🔍 Scraping: [█████▒▒▒▒▒] ", 
        "🔍 Scraping: [██████▒▒▒▒] ", 
        "🔍 Scraping: [███████▒▒▒] ", 
        "🔍 Scraping: [████████▒▒] ", 
        "🔍 Scraping: [█████████▒] ", 
        "🔍 Scraping: [██████████] "
    ]
    
    frame_index = 0
    
    while not stop_event.is_set():
        try:
            context.bot.edit_message_text(
                chat_id=update.effective_chat.id, 
                message_id=message.message_id, 
                text=animation_frames[frame_index]
            )
            frame_index = (frame_index + 1) % len(animation_frames)
            time.sleep(0.5)
            
        except RetryAfter as e:
            print(f"Controle de inundação excedido. Aguardando {e.retry_after} segundos.")
            time.sleep(e.retry_after)
            
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")
            break

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

def iniciar_scraping(update: Update, context: CallbackContext):
    stop_event = Event()
    context.job_queue.run_once(executar_scraping_thread, 0, context=(update, context, stop_event))

def processar_pergunta(update: Update, context: CallbackContext):
    if update.message and update.message.text:
        pergunta = update.message.text
        stop_event = threading.Event()

        threading.Thread(target=enviar_animacao_scraping, args=(update, context, stop_event)).start()
        threading.Thread(target=executar_scraping_thread, args=(update, context, stop_event)).start()
    else:
        if update.message:
            update.message.reply_text("Desculpe, eu só posso processar mensagens de texto.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Não consegui entender sua solicitação.")

def coletar_feedback(update: Update, response: str):
    user_feedback = update.message.text
    with open('feedback.txt', 'a') as f:
        f.write(f"Resposta: {response}\nFeedback: {user_feedback}\n\n")

def about(update: Update, context: CallbackContext):
    update.message.reply_text(cyber_description)


def respond_telegram(update: Update, context: CallbackContext) -> None:
    """Responde a mensagens no Telegram e salva perguntas e respostas no banco de dados."""
    try:
        pergunta = update.message.text

        is_complex = PIPALL_Function_LP()
        resposta = buscar_resposta_db(pergunta)

        if resposta:
            resposta = limitar_resposta(resposta, pergunta)
            salvar_em_db(pergunta, resposta)
            update.message.reply_text(resposta)
            return

        if "open.spotify.com" in pergunta:
            ds_music(update, context, pergunta)
            return

        first_name = update.message.from_user.first_name if update.message.from_user else None

        criador_cyber = response_otosan_cyber(pergunta, first_name=first_name)
        if isinstance(criador_cyber, (list, tuple)):
            criador_cyber = ' '.join([str(item) for item in criador_cyber if item])

        if criador_cyber:
            salvar_em_db(pergunta, criador_cyber)
            update.message.reply_text(criador_cyber)
            return

        if is_complex.is_complex_question(pergunta) and not any(palavra in pergunta\
          for palavra in ["cyber", "Cyber", "Voce", "voce", "Você", "você"]):
            processar_pergunta(update, context)
            return

        prompt = pergunta
        cohere_resposta = None
        
        for pattern in patterns_configure:
            if re.search(pattern, prompt, re.IGNORECASE):
                cohere_resposta = pipeline.cohere_respond_pipeline(pergunta, max_tokens=800, temperature=0.7)
                break
        
        if not cohere_resposta:
            cohere_resposta = pipeline.cohere_respond_pipeline(pergunta, max_tokens=50, temperature=0.7)

        cohere_resposta = re.sub(r"\bCoral\b|\bcoral\b", "Pegasus", cohere_resposta)

        if "Cohere" in cohere_resposta:
            cohere_resposta = re.sub(r"\bempresa\b", "pessoa", cohere_resposta)
        cohere_resposta = re.sub(r"\bpela Cohere\b|\bpela cohere\b", "pelo Cyber", cohere_resposta)
        cohere_resposta = re.sub(r"\bna língua inglesa\b", "no português", cohere_resposta)
        cohere_resposta = re.sub(r"\blíngua inglesa\b", "português", cohere_resposta)
        cohere_resposta = re.sub(r"\bFalo Inglês\b", "Falo Português", cohere_resposta)
        cohere_resposta = re.sub(r"\bpela empresa Cohere\b|\bpela empresa cohere\b", "pelo Cyber", cohere_resposta)
        cohere_resposta = limitar_resposta(cohere_resposta, pergunta)
        salvar_em_db(pergunta, cohere_resposta)

        update.message.reply_text(cohere_resposta)
        return

        resposta_site = buscar_informacao_wikipedia(pergunta)
        resposta_conhecimento = buscar_informacao(pergunta)

        if resposta_site:
            resposta_site_limited = limitar_resposta(resposta_site, pergunta)
            if resposta_site_limited and len(resposta_site_limited) <= 5000:
                try:
                    resposta_site_traduzida = translator.translate(resposta_site_limited)
                    resposta_site_traduzida = limitar_resposta(resposta_site_traduzida, pergunta) + " [Wiki]"
                    salvar_em_db(pergunta, resposta_site_traduzida)
                    update.message.reply_text(resposta_site_traduzida)
                    return

                except Exception as e:
                    print(f"Erro ao traduzir resposta da Wikipedia: {e}")
                    update.message.reply_text("Desculpe, ocorreu um erro ao tentar traduzir a resposta da Wikipedia.")
                    return
            else:
                update.message.reply_text("Desculpe, a resposta da Wikipedia é inválida ou muito longa para tradução.")
                return

        if resposta_conhecimento:
            resposta_conhecimento_limited = limitar_resposta(resposta_conhecimento, pergunta)
            if resposta_conhecimento_limited and len(resposta_conhecimento_limited) <= 5000:
                try:
                    resposta_conhecimento_traduzida = translator.translate(resposta_conhecimento_limited)
                    resposta_conhecimento_traduzida = limitar_resposta(resposta_conhecimento_traduzida, pergunta) + " [Knowledge]"
                    salvar_em_db(pergunta, resposta_conhecimento_traduzida)
                    update.message.reply_text(resposta_conhecimento_traduzida)
                    return

                except Exception as e:
                    print(f"Erro ao traduzir resposta do conhecimento: {e}")
                    update.message.reply_text("Desculpe, ocorreu um erro ao tentar traduzir a resposta do conhecimento.")
                    return
            else:
                update.message.reply_text("Desculpe, a resposta e inválida ou muito longa para tradução.")
                return

        update.message.reply_text("Desculpe, não encontrei uma resposta relevante.")

    except Exception as e:
        print(f"Erro ao responder no Telegram: {e}")
        update.message.reply_text("Ocorreu um erro ao processar sua mensagem.")

def run_telegram_bot() -> None:
    updater = Updater(TOKEN, use_context=True)

    inicializar_db()
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler("ip_info", ip_info))
    dispatcher.add_handler(CommandHandler("youtube", youtube_search))
    dispatcher.add_handler(CommandHandler("coletar_feedback", coletar_feedback))
    dispatcher.add_handler(CommandHandler("spotfy", ds_music))
    dispatcher.add_handler(CommandHandler("whois", whois))
    dispatcher.add_handler(CommandHandler("download_file", secure_download_file))
    dispatcher.add_handler(CommandHandler("ping", ping_server))
    dispatcher.add_handler(CommandHandler("coletar_info", coletar_info))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CommandHandler("core_search", core_search))
    dispatcher.add_handler(CommandHandler("website", website_monitor))
    dispatcher.add_handler(CommandHandler("security_audit", security_audit))
    dispatcher.add_handler(CommandHandler("traceroute", traceroute))
    dispatcher.add_handler(CommandHandler("news", news))
    dispatcher.add_handler(CommandHandler("perfil_info", informacoes_pessoais))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(CommandHandler('scraping', processar_pergunta))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond_telegram))

    updater.start_polling()
    updater.idle()



def run_terminal() -> None:
    pipall_instance = PIPALL_Function_LP()

    while True:
        user_input = input("\033[1;36mVocê Prompt/Bot:\033[m ").strip().lower()
        
        if user_input in ['exit', 'sair']:
            sys.exit()

        response = pipall_instance.respond(user_input)

        print("Pegasus:", response)

if __name__ == "__main__":
    terminal_thread = threading.Thread(target=run_terminal)
    terminal_thread.start()
    run_telegram_bot()

    terminal_thread.join()