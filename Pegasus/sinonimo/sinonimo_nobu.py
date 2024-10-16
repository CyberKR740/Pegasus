import re
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator

# Configurar o tradutor usando o deep_translator
translator = GoogleTranslator(source='en', target='pt')

def traduzir_para_ingles(pergunta):
    """Traduz uma palavra do português para o inglês e remove prefixos indesejados."""
    try:
        # Traduzir do português para o inglês
        traducao = GoogleTranslator(source='pt', target='en').translate(pergunta)
        
        if not traducao:  # Verificar se a tradução falhou
            print(f"Tradução falhou para a palavra: {pergunta}")
            return None

        # Remover prefixos indesejados
        prefixos = [
            'to', 'for', 'on', 'in', 'of', 'with', 'about',
            'and', 'or', 'but', 'that', 'how', 'what', 'this',
            'up', 'down', 'out', 'through', 'around', 'over'
        ]
        for prefixo in prefixos:
            traducao = traducao.replace(f'{prefixo} ', '').replace(f' {prefixo}', '')
        
        return traducao.strip()

    except Exception as e:
        return None

def gerar_sinonimos(pergunta):
    """Gera sinônimos de uma palavra em inglês usando o WordNet."""
    sinonimos = []
    try:
        for syn in wordnet.synsets(pergunta):
            for lemma in syn.lemmas():
                sinonimos.append(lemma.name())  # Nome do sinônimo
        return list(set(sinonimos))  # Remove duplicatas
    except Exception as e:
        print(f"Erro ao gerar sinônimos para '{pergunta}': {e}")
        return []

def traduzir_sinonimos(sinonimos):
    """Traduz uma lista de sinônimos do inglês para o português, individualmente."""
    sinonimos_traduzidos = []
    for sinonimo in sinonimos:
        try:
            sinonimo_formatado = re.sub(r"_+", " ", sinonimo)
            # Usando deep_translator que retorna uma string diretamente
            traducao = translator.translate(sinonimo_formatado)

            if traducao:
                sinonimos_traduzidos.append(traducao)
            else:
                print(f"Falha na tradução de '{sinonimo_formatado}', mantendo em inglês.")
                sinonimos_traduzidos.append(sinonimo_formatado)  # Fallback para manter o original
        except Exception as e:
            print(f"Erro ao traduzir '{sinonimo_formatado}': {e}")
            sinonimos_traduzidos.append(sinonimo_formatado)  # Fallback em caso de erro
    
    return sinonimos_traduzidos

def introducao_sinonimos(pergunta):
    """Gera sinônimos traduzidos de uma palavra em português."""
    palavra_en = traduzir_para_ingles(pergunta)
    
    if palavra_en:
        sinonimos_en = gerar_sinonimos(palavra_en)
        if sinonimos_en:
            sinonimos_pt = traduzir_sinonimos(sinonimos_en)
            return sinonimos_pt
        else:
            print(f"Nenhum sinônimo encontrado para '{palavra_en}'")
    else:
        print(f"Tradução falhou para '{pergunta}'")
    
    return []