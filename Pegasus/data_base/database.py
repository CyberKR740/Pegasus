import sqlite3, os

DATABASE = 'historico_perguntas_respostas.db'


def inicializar_db():
    """Inicializa o banco de dados e cria a tabela se não existir."""
    if not os.path.exists(DATABASE):
        criar_tabela()

def buscar_resposta_db(pergunta):
    """Busca uma resposta no banco de dados para uma determinada pergunta."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT resposta FROM perguntas_respostas WHERE pergunta = ?', (pergunta,))
        
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None


def criar_tabela():
    """Cria a tabela de perguntas e respostas se não existir."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perguntas_respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL
        )
        ''')
        conn.commit()

def salvar_em_db(pergunta, resposta):
    """Salva uma pergunta e sua resposta no banco de dados."""
    pergunta = str(pergunta)  # Converte para string caso não seja
    resposta = str(resposta)  # Converte para string caso não seja

    if isinstance(resposta, tuple):
        resposta = ' '.join([str(item) for item in resposta])  # Concatena a tupla em uma string

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)', (pergunta, resposta))
        conn.commit()
