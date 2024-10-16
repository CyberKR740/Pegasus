import unicodedata



def remove_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

custom_stop_words = [
    'ainda', 'assim', 'até', 'bem', 'demais', 'então', 'mas', 'mais', 'menos', 'muito', 'nunca', 'pois',
    'porém', 'sempre', 'só', 'também', 'talvez', 'agora', 'antes', 'depois', 'hoje', 'já', 'nunca', 'sempre',
    'aqui', 'ali', 'lá', 'onde', 'aquele', 'aquela', 'aquilo', 'este', 'esta', 'isto', 'algum', 'nenhum', 'todo',
    'qualquer', 'outro', 'outra', 'outros', 'outras', 'cada', 'vários', 'poucos', 'alguns', 'nenhuns',
    'ah', 'ai', 'oh', 'eita', 'opa', 'puxa', 'mas', 'porém', 'logo', 'portanto', 'pois', 'que', 'se', 'como',
    'quando', 'onde', 'porque', 'porquanto', 'embora', 'contudo', 'entretanto', 'aliás', 'ademais',
    'isto é', 'ou seja', 'por exemplo', 'a saber', 'em suma', 'em resumo', 'em outras palavras',
    'brasil', 'rio', 'são paulo', 'joão', 'maria', 'artigo', 'parágrafo', 'inciso',
    'quais', 'qual', 'são', 'ser', 'que', 'isso', 'este', 'essa', 'esse', 'essa', 'isto', 'aquilo', 'aqui', 'ali',
    'lá', 'da', 'de', 'do', 'dos', 'das', 'um', 'uma', 'uns', 'umas', 'os', 'as', 'o', 'a', 'para', 'com', 'sem',
    'por', 'em', 'no', 'na', 'nos', 'nas', 'pelo', 'pela', 'pelos', 'pelas', 'e', 'ou', 'mas', 'então', 'porque',
    'se', 'quanto', 'onde', 'como', 'quem', 'ele', 'ela', 'eles', 'elas', 'você', 'vocês', 'nosso', 'nossa',
    'meu', 'minha', 'teu', 'tua', 'seu', 'sua', 'dele', 'dela', 'delas', 'dele', 'deles', 'sou', 'é', 'era',
    'foi', 'será', 'estou', 'está', 'estávamos', 'estiveram', 'tinha', 'havia', 'ter', 'tiveram', 'terão',
    'vamos', 'vão', 'seria', 'queria', 'vai', 'veja', 'ver', 'vou', 'também', 'já', 'ainda', 'até', 'muito', 'pouco'
]

custom_stop_words_normalized = [remove_acentos(word) for word in custom_stop_words]