# services/produto_service.py

from services.db_connector import get_db_connection
from entities.produto import Produto

# --- Caso de Uso: Navegar Produtos ---
def listar_produtos() -> list[Produto]:
    """Retorna todos os produtos disponíveis para navegação."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE estoque > 0")
    produtos_db = cursor.fetchall()
    conn.close()

    return [Produto(**dict(p)) for p in produtos_db]

def buscar_produto_por_id(produto_id: int) -> Produto | None:
    """Busca um produto específico (necessário para Adicionar ao Carrinho)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto_db = cursor.fetchone()
    conn.close()

    if produto_db:
        return Produto(**dict(produto_db))
    return None

# --- CRUD de Gerenciar Produtos (Admin) ---
def criar_produto(nome: str, descricao: str, preco: float, estoque: int) -> Produto | None:
    """Cria um novo produto (CREATE)."""
    if preco <= 0 or estoque < 0:
        print("Validação falhou: Preço ou estoque inválidos.")
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque) VALUES (?, ?, ?, ?)",
        (nome, descricao, preco, estoque)
    )
    conn.commit()
    produto_id = cursor.lastrowid
    conn.close()

    return Produto(produto_id, nome, descricao, preco, estoque)

# Implementar atualizar_produto e deletar_produto para CRUD completo...
