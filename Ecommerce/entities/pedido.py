# entities/pedido.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ItemPedido:
    produto_id: int
    nome_produto: str
    quantidade: int
    preco_unitario: float

@dataclass
class Pedido:
    id: int
    cliente_id: int
    itens: List[ItemPedido]
    valor_total: float
    status: str = "AGUARDANDO_PAGAMENTO" # Pode ser: PAGO, ENVIADO, ENTREGUE, CANCELADO
    codigo_rastreio: str = ""
    nota_fiscal_gerada: bool = False
