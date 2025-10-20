# entities/cliente.py
from dataclasses import dataclass

@dataclass
class Cliente:
    id: int
    nome: str
    email: str
    senha_hash: str # Armazena o hash da senha
    tipo: str = "cliente"
