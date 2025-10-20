# utils/validacoes.py

import re

def validar_email(email: str) -> bool:
    """Verifica se o formato do e-mail é válido."""
    # Regex básica para validação de e-mail
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.match(regex, email, re.IGNORECASE) is not None

def validar_senha(senha: str) -> bool:
    """Verifica se a senha atende aos requisitos mínimos (ex: > 6 caracteres)."""
    return len(senha) >= 6

def validar_quantidade(quantidade: int) -> bool:
    """Verifica se a quantidade é positiva."""
    return quantidade > 0

def validar_dados_pagamento(dados: dict) -> bool:
    """Simula a validação de dados de pagamento (ex: número e validade do cartão)."""
    if 'numero' not in dados or 'validade' not in dados:
        return False
    # Simulação de validação de 16 dígitos
    return len(dados['numero']) == 16 and dados['validade'] # Apenas verifica se a chave existe
