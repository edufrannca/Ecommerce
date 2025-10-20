# services/pedido_service.py

from services.db_connector import get_db_connection
from entities.pedido import Pedido, ItemPedido
from services.produto_service import buscar_produto_por_id
from utils.validacoes import validar_quantidade, validar_dados_pagamento
import time # Para simular tempo de processamento

# Simulação de Carrinho em memória, pois não é uma Entidade persistente no DB
CARRINHOS_SESSAO = {} # {cliente_id: [{'produto_id': 1, 'qtd': 2}, ...]}

# --- Caso de Uso: Adicionar ao Carrinho ---
def adicionar_ao_carrinho(cliente_id: int, produto_id: int, quantidade: int) -> bool:
    """Adiciona um item ao carrinho em sessão."""
    if not validar_quantidade(quantidade):
        print("Validação falhou: Quantidade deve ser positiva.")
        return False

    produto = buscar_produto_por_id(produto_id)
    if not produto or produto.estoque < quantidade:
        print("Validação falhou: Produto não encontrado ou estoque insuficiente.")
        return False

    # Inicializa o carrinho se não existir
    if cliente_id not in CARRINHOS_SESSAO:
        CARRINHOS_SESSAO[cliente_id] = []

    # Lógica para adicionar ou atualizar item...
    CARRINHOS_SESSAO[cliente_id].append({
        'produto_id': produto.id,
        'qtd': quantidade,
        'preco': produto.preco,
        'nome': produto.nome
    })
    print(f"Produto {produto.nome} adicionado ao carrinho do cliente {cliente_id}.")
    return True

# --- Caso de Uso: Finalizar Compra (inclui Processar Pagamento, Gerar NF, Enviar) ---
def finalizar_compra(cliente_id: int, dados_pagamento: dict) -> Pedido | dict:
    """Orquestra o processo de compra: Finalizar -> Processar Pgto -> Gerar NF -> Enviar."""
    if cliente_id not in CARRINHOS_SESSAO or not CARRINHOS_SESSAO[cliente_id]:
        return {"error": "Carrinho vazio."}

    # 1. FINALIZAR COMPRA: Calcule o total e prepare os itens
    itens_carrinho = CARRINHOS_SESSAO[cliente_id]
    valor_total = sum(item['qtd'] * item['preco'] for item in itens_carrinho)

    print(f"Cliente {cliente_id} iniciando a finalização da compra. Total: R${valor_total:.2f}")

    # 2. PROCESSAR PAGAMENTO
    pedido_id = _processar_pagamento(cliente_id, valor_total, itens_carrinho, dados_pagamento)

    if isinstance(pedido_id, dict):
        return pedido_id # Falha no pagamento

    # 3. GERAR NOTA FISCAL (INCLUI: Enviar Produto)
    # A Geração da NF é um pré-requisito para o envio
    pedido_atualizado = _gerar_nota_fiscal(pedido_id)

    # 4. ENVIAR PRODUTO (Chamado dentro de Gerar NF)
    if pedido_atualizado.status == "ENVIADO":
        # Limpar o carrinho
        del CARRINHOS_SESSAO[cliente_id]
        return pedido_atualizado
    else:
        # Se falhou na NF/Envio (improvável após pgto), retornamos o erro
        return {"error": "Erro desconhecido na geração da NF ou envio."}

# --- Operação de Processamento de Pagamento ---
def _processar_pagamento(cliente_id: int, valor_total: float, itens: list, dados_pagamento: dict) -> int | dict:
    """Implementa Processar Pagamento (ponto de extensão para falha)."""
    print("\n[Módulo de Pagamento]: Processando...")
    time.sleep(1)

    if not validar_dados_pagamento(dados_pagamento):
        _notificar_falha_pagamento(cliente_id) # EXTEND: Notificar Falha de Pagamento
        return {"error": "Falha no pagamento: Dados inválidos."}

    # Simulação de aprovação
    pagamento_aprovado = True # Dados válidos = Pagamento aprovado na simulação

    if pagamento_aprovado:
        # Persiste o Pedido no DB com status inicial
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO pedidos (cliente_id, valor_total, status, nota_fiscal_gerada) VALUES (?, ?, ?, ?)",
            (cliente_id, valor_total, "PAGO", False)
        )
        pedido_id = cursor.lastrowid

        # Insere os itens do pedido
        for item in itens:
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, nome_produto, quantidade, preco_unitario) VALUES (?, ?, ?, ?, ?)",
                (pedido_id, item['produto_id'], item['nome'], item['qtd'], item['preco'])
            )
            # Atualiza estoque
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item['qtd'], item['produto_id'])
            )

        conn.commit()
        conn.close()
        print(f"[Módulo de Pagamento]: Pagamento Aprovado. Pedido ID: {pedido_id}")
        return pedido_id
    else:
        _notificar_falha_pagamento(cliente_id)
        return {"error": "Falha no pagamento: Recusado pela operadora."}

# --- Operação de Geração de Nota Fiscal ---
def _gerar_nota_fiscal(pedido_id: int) -> Pedido:
    """Implementa Gerar Nota Fiscal (INCLUI: Enviar Produto)."""
    print(f"\n[Módulo Fiscal]: Gerando Nota Fiscal para Pedido ID: {pedido_id}")
    time.sleep(1)

    # Simulação de NF
    nota_fiscal_sucesso = True

    if nota_fiscal_sucesso:
        # Atualiza o status no DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE pedidos SET nota_fiscal_gerada = TRUE WHERE id = ?", (pedido_id,))
        conn.commit()
        conn.close()
        print("[Módulo Fiscal]: Nota Fiscal Gerada com Sucesso.")

        # CHAMA O PRÓXIMO PASSO
        return _enviar_produto(pedido_id)
    else:
        # Lógica de erro de NF aqui...
        pass

# --- Operação de Envio de Produto ---
def _enviar_produto(pedido_id: int) -> Pedido:
    """Implementa Enviar Produto."""
    print(f"\n[Transportadora]: Iniciando Envio do Pedido ID: {pedido_id}")
    time.sleep(1)

    codigo_rastreio = f"BR{int(time.time())}" # Código de rastreio simulado

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ?, codigo_rastreio = ? WHERE id = ?",
        ("ENVIADO", codigo_rastreio, pedido_id)
    )
    conn.commit()

    # Recupera o pedido finalizado
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
    pedido_db = cursor.fetchone()
    conn.close()

    print(f"[Transportadora]: Pedido Enviado. Código: {codigo_rastreio}")

    # Retorna o objeto Pedido completo (para simplificação, não populamos os itens aqui)
    return Pedido(
        id=pedido_db['id'],
        cliente_id=pedido_db['cliente_id'],
        valor_total=pedido_db['valor_total'],
        status=pedido_db['status'],
        itens=[], # Omitido para simplificação da resposta
        codigo_rastreio=pedido_db['codigo_rastreio']
    )

# --- Operação de Notificação de Falha (EXTEND) ---
def _notificar_falha_pagamento(cliente_id: int):
    """Implementa Notificar Falha de Pagamento."""
    print(f"\n[SISTEMA]: Notificando Cliente {cliente_id} sobre a Falha de Pagamento por e-mail/SMS.")
