# main.py

import os
from services.db_connector import init_db
from services.usuario_service import criar_usuario, autenticar_usuario
from services.produto_service import criar_produto, listar_produtos
from services.pedido_service import adicionar_ao_carrinho, finalizar_compra, CARRINHOS_SESSAO

# --- 0. Configuração Inicial ---
print("--- Inicializando o Sistema E-commerce ---")
# Garantir que o DB e as tabelas existam
init_db()

# --- 1. População Inicial (Admin e Produtos) ---

# Criar Usuário Administrador
print("\n[SETUP] Criando Administrador e Cliente...")
admin = criar_usuario("Admin Master", "admin@ecommerce.com", "admin123", "administrador")
cliente = criar_usuario("Maria Cliente", "maria@teste.com", "senha123", "cliente")

if admin and cliente:
    print(f"-> Admin ID: {admin.id}, Cliente ID: {cliente.id}")

# Gerenciar Produtos (CRUD - CREATE)
print("\n[ADMIN] Gerenciando Produtos (CREATE)...")
p1 = criar_produto("Laptop Pro", "Notebook de alta performance", 4500.00, 10)
p2 = criar_produto("Mouse Sem Fio", "Mouse ergonômico", 150.00, 50)
p3 = criar_produto("Monitor 27'", "Monitor 4K", 1800.00, 5)

if p1 and p2:
    print(f"-> Produtos criados: {p1.nome}, {p2.nome}")

# --- 2. Simulação de Caso de Uso: Cliente ---

# Navegar Produtos
print("\n[CLIENTE] Navegando Produtos...")
produtos_disponiveis = listar_produtos()
print(f"-> Total de produtos em estoque: {len(produtos_disponiveis)}")
# for p in produtos_disponiveis:
#     print(f"   - {p.nome} (R${p.preco:.2f})")

# Adicionar ao Carrinho
print("\n[CLIENTE] Adicionando ao Carrinho...")
# p1 (Laptop)
adicionar_ao_carrinho(cliente.id, p1.id, 1)
# p2 (Mouse)
adicionar_ao_carrinho(cliente.id, p2.id, 2)

print(f"-> Carrinho atual do cliente {cliente.id}: {CARRINHOS_SESSAO.get(cliente.id)}")

# Autenticar Usuário (Necessário para Finalizar Compra)
print("\n[CLIENTE] Autenticando...")
usuario_autenticado = autenticar_usuario(cliente.email, "senha123")
if usuario_autenticado:
    print(f"-> Usuário {usuario_autenticado.nome} autenticado com sucesso.")

# --- 3. Simulação de Caso de Uso: Finalizar Compra (com atores externos) ---

# Dados de pagamento simulados (Simulação de sucesso)
dados_pgto_sucesso = {'numero': '1234567890123456', 'validade': True, 'cvv': '123'}

print("\n[CLIENTE] Finalizando Compra (Chamando: Processar Pgto, Gerar NF, Enviar)...")
resultado_compra = finalizar_compra(cliente.id, dados_pgto_sucesso)

if isinstance(resultado_compra, dict) and 'error' in resultado_compra:
    print(f"!!! Falha na compra: {resultado_compra['error']} !!!")
else:
    print("\n--- RESUMO DA COMPRA ---")
    print(f"✅ Pedido Finalizado com Sucesso! ID: {resultado_compra.id}")
    print(f"Status: **{resultado_compra.status}**")
    print(f"Valor Total: R${resultado_compra.valor_total:.2f}")
    print(f"Rastreio (Transportadora): {resultado_compra.codigo_rastreio}")

    # Acompanhar Pedido (Cliente)
    print("\n[CLIENTE] Acompanhando Pedido...")
    # Em um sistema real, buscaríamos o pedido por ID para ver o status
    print(f"Status Atual do Pedido {resultado_compra.id}: {resultado_compra.status}")

# Simulação de Falha de Pagamento (EXTEND)
print("\n--- Simulação de Falha de Pagamento ---")
dados_pgto_falha = {'numero': '123', 'validade': False, 'cvv': '123'} # Dados inválidos
adicionar_ao_carrinho(cliente.id, p3.id, 1) # Adiciona item novamente
resultado_falha = finalizar_compra(cliente.id, dados_pgto_falha)

if isinstance(resultado_falha, dict) and 'error' in resultado_falha:
    print(f"!!! Falha esperada: {resultado_falha['error']} !!!")

# --- 4. Limpeza (Opcional) ---
# os.remove("ecommerce.db")
# print("\n[SETUP] Banco de dados removido.")
