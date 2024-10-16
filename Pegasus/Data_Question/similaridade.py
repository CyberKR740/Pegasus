import sqlite3

def criar_tabela_db():
    conn = sqlite3.connect('mensagens.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

criar_tabela_db()

def salvar_pergunta_resposta(pergunta, resposta):
    conn = sqlite3.connect('mensagens.db')
    c = conn.cursor()
    
    # Inserir a pergunta e a resposta no banco
    c.execute('INSERT INTO historico (pergunta, resposta) VALUES (?, ?)', (pergunta, resposta))
    
    conn.commit()
    conn.close()

# Função para buscar perguntas/respostas similares
def buscar_perguntas_similares(pergunta, limiar=0.75):
    conn = sqlite3.connect('mensagens.db')
    c = conn.cursor()

    c.execute('SELECT id, pergunta, resposta FROM historico')
    historico = c.fetchall()
    
    conn.close()

    from fuzzywuzzy import fuzz
    similares = []
    for entrada in historico:
        id, pergunta_anterior, resposta_anterior = entrada
        similaridade = fuzz.ratio(pergunta.lower(), pergunta_anterior.lower()) / 100
        
        if similaridade >= limiar:
            similares.append((id, pergunta_anterior, resposta_anterior, similaridade))

    return similares