import language_tool_python
import difflib  # Para calcular a semelhança entre as palavras

# Inicializa o LanguageTool para o português brasileiro
tool = language_tool_python.LanguageTool('pt-BR')

# Correções manuais para palavras específicas
correcoes_manualmente = {
    'exemple': 'exemplo',
}

# Função para calcular a distância de Levenshtein entre duas palavras
def distancia_levenshtein(palavra1, palavra2):
    return difflib.SequenceMatcher(None, palavra1, palavra2).ratio()

def verificar_texto(texto):
    if isinstance(texto, bytes):
        texto = texto.decode('utf-8', 'replace')
    
    resultados = tool.check(texto)
    correcoes = {}

    for erro in resultados:
        palavra = erro.context[erro.offset: erro.offset + erro.errorLength]
        correcoes[palavra] = {
            'status': 'incorreta',
            'sugestoes': erro.replacements if erro.replacements else ['Nenhuma sugestão disponível']
        }

    return correcoes

def corrigir_texto(texto, limite_gravidade=0.8):
    # Corrige o texto inteiro de uma só vez
    if isinstance(texto, bytes):
        texto = texto.decode('utf-8', 'replace')

    # Verifica e corrige o texto
    resultados = tool.check(texto)
    texto_corrigido = texto

    for erro in resultados:
        if erro.replacements:
            # Escolhe a primeira sugestão
            sugestao = erro.replacements[0]
            similaridade = distancia_levenshtein(erro.context[erro.offset: erro.offset + erro.errorLength], sugestao)

            # Corrige apenas se a similaridade for baixa
            if similaridade < limite_gravidade:
                texto_corrigido = texto_corrigido.replace(erro.context[erro.offset: erro.offset + erro.errorLength], sugestao)

    return texto_corrigido

# Exemplo de uso
#texto = "Por Se você está procurando carros baratos para comprar, então vai querer saber disso."
#print("Texto original:", texto)
#print("Texto corrigido:", corrigir_texto(texto))