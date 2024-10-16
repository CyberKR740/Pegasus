import random
# Certifique-se de que os recursos do nltk estão instalados :
# Supondo que essas listas estão definidas corretamente :
from IAFGen_GConsole.verbos.agentes_verbais import verbos_agente
from IAFGen_GConsole.preposicoes.sobu_preposicoes import preposicoes
from IAFGen_GConsole.adjetivos.adjetivos_vision import adjetivos
from IAFGen_GConsole.substantivos.substantivo_imperio import substantivos
from IAFGen_GConsole.lugares.lugares_engoy import lugares_yum

def gerar_frase(lista_entrada):
    # Estruturas de frases sobre a imagem 
    estruturas = [
        "Uma imagem {adjetivo1} de {substantivo1} e {substantivo2}, que {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A representação {adjetivo1} de {substantivo1} e {substantivo2} mostra como {nome1} {verbo1} {substantivo2}, enquanto {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} de {substantivo1} e {substantivo2} é um exemplo de como {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Neste {adjetivo1} {substantivo1} e {substantivo2}, {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} retrata {substantivo1} e {substantivo2}, onde {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Com uma imagem {adjetivo1} de {substantivo1} e {substantivo2}, {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Esta imagem {adjetivo1} de {substantivo1} e {substantivo2} demonstra como {nome1} {verbo1} {substantivo2}, ao mesmo tempo que {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Uma imagem {adjetivo1} de {substantivo1} e {substantivo2} representa como {nome1} {verbo1} {substantivo2}, e {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Na imagem {adjetivo1} de {substantivo1} e {substantivo2}, {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} de {substantivo1} e {substantivo2} ilustra como {nome1} {verbo1} {substantivo2}, ao mesmo tempo que {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "O {substantivo1} e {substantivo2} {adjetivo1} retratados mostram que {nome1} {verbo1} {substantivo2}, enquanto {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} de {substantivo1} e {substantivo2} simboliza como {nome1} {verbo1} {substantivo2}, ao passo que {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Nesta imagem, {nome1} {verbo1} um {substantivo1} {adjetivo1} e {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} representa {substantivo1} e {substantivo2}, ilustrando como {nome1} {verbo1} {substantivo2}, enquanto {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Observando a imagem {adjetivo1} de {substantivo1} e {substantivo2}, podemos ver que {nome1} {verbo1} {substantivo2}, enquanto {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} que captura {substantivo1} e {substantivo2} revela como {nome1} {verbo1} {substantivo2}, ao mesmo tempo que {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Na imagem {adjetivo1}, observamos {substantivo1} e {substantivo2}, onde {nome1} {verbo1} {substantivo2}, {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} de {substantivo1} e {substantivo2} destaca como {nome1} {verbo1} {substantivo2}, enquanto {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "Esta imagem {adjetivo1} de {substantivo1} e {substantivo2} mostra que {nome1} {verbo1} {substantivo2}, ao passo que {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "A imagem {adjetivo1} que representa {substantivo1} e {substantivo2} é um exemplo de como {nome1} {verbo1} {substantivo2}, enquanto {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2} de {substantivo6}, {substantivo7} {substantivo8} e {substantivo9}.",
        "{nome1} {verbo1} {substantivo1} e {substantivo2}, enquanto a imagem {adjetivo1} {verbo2} {substantivo3} e {substantivo4} em uma {substantivo5} {adjetivo2}, {substantivo6} de {substantivo7} e {substantivo8}.",
        "{nome1} {verbo1} {substantivo1}, e através da imagem {adjetivo1}, observamos {substantivo2} e {substantivo3}, {verbo2} {substantivo4} e {substantivo5} em uma {substantivo6} {adjetivo2}.",
        "{substantivo1} e {substantivo2} são mostrados, e a imagem {adjetivo1} {verbo1} {substantivo3}, {verbo2} {substantivo4} e {substantivo5} com {substantivo6}, {adjetivo2} e {substantivo7}.",
        "Enquanto {nome1} {verbo1} {substantivo1}, a imagem {adjetivo1} {verbo2} {substantivo2} e {substantivo3}, criando uma {substantivo4} {adjetivo2} e {substantivo5}.",
        "{substantivo1} é capturado enquanto a imagem {adjetivo1} {verbo1} {substantivo2} e {substantivo3}, {substantivo4} de {adjetivo2} e {substantivo5} {verbo2} em uma {substantivo6}.",
        "{nome1} {verbo1} {substantivo1}, e na imagem {adjetivo1}, observamos {substantivo2} {verbo2} {substantivo3}, além de {substantivo4} e {substantivo5} {adjetivo2}.",
        "Com {substantivo1} e {substantivo2}, a imagem {adjetivo1} revela {nome1} {verbo1} {substantivo3}, enquanto {verbo2} {substantivo4} {substantivo5} e {substantivo6}.",
        "{substantivo1} {verbo1} {substantivo2}, e na imagem {adjetivo1}, {nome1} {verbo2} {substantivo3} e {substantivo4} dentro de {substantivo5} {adjetivo2}.",
        "Através de {substantivo1}, a imagem {adjetivo1} demonstra {substantivo2} e {substantivo3}, enquanto {nome1} {verbo1} {substantivo4} e {substantivo5} {verbo2}.",
        "Enquanto {nome1} {verbo1} {substantivo1}, a imagem {adjetivo1} captura {substantivo2}, {verbo2} {substantivo3} e {substantivo4}, {substantivo5} em uma {substantivo6} {adjetivo2}."
        # Adicione outras estruturas conforme necessário
    ]

    # Classificar palavras da lista de entrada
    
    verbos = verbos_agente
    lugares = lugares_yum

    # Garantir que há palavras suficientes
    if len(adjetivos) < 2:
        adjetivos.extend(adjetivos)  # Adiciona adjetivos duplicados como fallback
    if len(substantivos) < 9:
        substantivos.extend(substantivos)  # Adiciona substantivos duplicados como fallback

    # Seleciona aleatoriamente elementos da lista para a frase
    frase = random.choice(estruturas).format(
        adjetivo1=random.choice(adjetivos),
        substantivo1=random.choice(substantivos),
        substantivo2=random.choice(substantivos),
        nome1=random.choice(substantivos),
        verbo1=random.choice(verbos),
        preposição=random.choice(preposicoes),
        lugar1=random.choice(lugares),
        verbo2=random.choice(verbos),
        substantivo3=random.choice(substantivos),
        substantivo4=random.choice(substantivos),
        substantivo5=random.choice(substantivos),
        adjetivo2=random.choice(adjetivos),
        substantivo6=random.choice(substantivos),
        conectando=random.choice(verbos),
        substantivo7=random.choice(substantivos),
        substantivo8=random.choice(substantivos),
        substantivo9=random.choice(substantivos)
    )
    
    return frase