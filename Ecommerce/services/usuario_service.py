# services/usuario_service.py
import sqlite3
import hashlib
from services.db_connector import get_db_connection
from entities.cliente import Cliente
from utils.validacoes import validar_email, validar_senha

def _hash_senha(senha: str) -> str:
    """Gera o hash da senha para armazenamento seguro."""
    return hashlib.sha256(senha.encode()).hexdigest()

# --- Caso de Uso: Autenticar Usuário ---
def autenticar_usuario(email: str, senha: str) -> Cliente | None:
    """Verifica as credenciais do usuário."""
    if not validar_email(email):
        print("Validação falhou: Formato de e-mail inválido.")
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario_db = cursor.fetchone()
    conn.close()

    if not usuario_db:
        print("Autenticação falhou: Usuário não encontrado.")
        return None

    senha_hash_input = _hash_senha(senha)
    if usuario_db['senha_hash'] == senha_hash_input:
        # Retorna o objeto Cliente/Admin autenticado
        return Cliente(
            id=usuario_db['id'],
            nome=usuario_db['nome'],
            email=usuario_db['email'],
            senha_hash=usuario_db['senha_hash'],
            tipo=usuario_db['tipo']
        )
    else:
        print("Autenticação falhou: Senha incorreta.")
        return None

# --- CRUD de Gerenciar Usuários (Admin) ---
def criar_usuario(nome: str, email: str, senha: str, tipo: str = "cliente") -> Cliente | None:
    """Cria um novo usuário (usado por Admin para Gerenciar, ou Cliente para Cadastro)."""
    if not (validar_email(email) and validar_senha(senha)):
        print("Validação falhou: E-mail ou senha inválidos.")
        return None

    senha_hash = _hash_senha(senha)
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, tipo)
        )
        conn.commit()

        # Recupera o ID do último inserido
        usuario_id = cursor.lastrowid
        return Cliente(usuario_id, nome, email, senha_hash, tipo)
    except sqlite3.IntegrityError:
        print(f"Erro: E-mail {email} já está em uso.")
        return None
    finally:
        conn.close()

# Implementar atualizar_usuario e deletar_usuario para CRUD completo...
