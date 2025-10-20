# services/db_connector.py

import sqlite3

DATABASE_NAME = "ecommerce.db"

def get_db_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

def init_db():
    """Inicializa as tabelas do banco de dados (CREATE, READ)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de Usuários (Inclui Cliente e Administrador)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            tipo TEXT NOT NULL -- 'cliente' ou 'administrador'
        )
    """)

    # Tabela de Produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    """)

    # Tabela de Pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            status TEXT NOT NULL,
            codigo_rastreio TEXT,
            nota_fiscal_gerada BOOLEAN,
            FOREIGN KEY (cliente_id) REFERENCES usuarios (id)
        )
    """)

    # Tabela de Itens do Pedido (Muitos para Muitos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            PRIMARY KEY (pedido_id, produto_id),
            FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    """)

    conn.commit()
    conn.close()

# Chamada para garantir que o DB e as tabelas existam
init_db()
