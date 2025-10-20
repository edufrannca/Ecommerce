

# 🛒 E-Commerce Terminal  
### Uma loja virtual direto no seu terminal — simples, funcional e pronta para evoluir

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.x-lightgrey?logo=sqlite)
![CLI](https://img.shields.io/badge/Interface-CLI-brightgreen)
![License](https://img.shields.io/badge/License-MIT-purple)

> **Versão 1.0** — Um sistema de e-commerce completo rodando **exclusivamente no terminal**, construído com Python puro e SQLite. Ideal para entender os fundamentos de um marketplace antes de escalar para uma arquitetura web com Django.

---

## 🌟 Por Que Este Projeto?

Muitos iniciam projetos web com frameworks antes de compreender a lógica de negócio por trás. Este projeto inverte essa abordagem:  
✅ **Foco total na modelagem de domínio**  
✅ **Persistência real com SQLite**  
✅ **Arquitetura limpa e modular**  
✅ **Base sólida para migração futura para Django**

Ele é mais do que um “script de terminal” — é um **protótipo funcional** de um sistema de e-commerce, pronto para evoluir.

---

## 🧱 Arquitetura e Organização

O projeto segue uma estrutura limpa e escalável, inspirada em boas práticas de engenharia de software:

```
Ecommerce/
├── entities/          # Modelos de domínio (Cliente, Produto, Pedido)
├── services/          # Regras de negócio (criação, validação, cálculo)
├── utils/             # Banco de dados (SQLite), helpers e validações
├── main.py            # Interface CLI e fluxo principal
├── ecommerce.db       # Banco de dados persistente (SQLite)
└── README.md
```

Cada camada tem responsabilidades bem definidas:
- **Entities**: representam o núcleo do negócio.
- **Services**: orquestram operações e garantem consistência.
- **Utils**: abstraem detalhes técnicos como acesso ao banco.

---

## 🚀 Funcionalidades Implementadas

| Categoria         | Funcionalidades                                                                 |
|-------------------|----------------------------------------------------------------------------------|
| **Produtos**      | Cadastrar, listar, buscar por ID, excluir                                       |
| **Clientes**      | Cadastrar com nome e e-mail (validado), listar                                  |
| **Pedidos**       | Criar pedidos com múltiplos itens, associar a cliente, calcular total           |
| **Persistência**  | Todos os dados salvos em `ecommerce.db` (SQLite) — sobrevivem entre sessões     |
| **Validações**    | E-mails válidos, preços positivos, IDs existentes, campos obrigatórios          |
| **UX no Terminal**| Menu interativo, mensagens claras, tratamento de erros amigável                 |

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3.13 ou superior
- Nenhum pacote externo necessário (usa apenas bibliotecas padrão)

### Passo a passo
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ecommerce-terminal.git
cd ecommerce-terminal

# 2. Execute o sistema
python main.py
```

> 💡 **Dica**: O banco de dados (`ecommerce.db`) é criado automaticamente na primeira execução.

---

## 🗺️ Roadmap: Do Terminal ao Django

Este é apenas o **primeiro capítulo** do projeto. A visão de longo prazo inclui:

| Versão | Meta |
|--------|------|
| **v1.x** | Aprimorar CLI, adicionar relatórios, testes unitários |
| **v2.0** | **Migração para Django** — interface web, autenticação, admin |
| **v2.1** | Carrinho de compras, checkout, histórico de pedidos |
| **v3.0** | Integração com gateways de pagamento (simulada ou real) |
| **v3.1+**| API REST, Dockerização, CI/CD |

> O código atual foi projetado para facilitar essa transição — os modelos de domínio já estão prontos para serem mapeados para modelos Django.

---

## 📦 Tecnologias Utilizadas

- **Linguagem**: Python 3.13+
- **Banco de Dados**: SQLite (sem dependências externas)
- **Padrões**: Programação orientada a objetos, separação de camadas
- **Próxima etapa**: Django, Django ORM, HTML/CSS, Bootstrap

---

## 🤝 Contribuições

Encontrou um bug? Tem uma ideia para melhorar a UX do terminal? Abra uma **issue** ou envie um **pull request**!  
Contribuições são bem-vindas, especialmente em:
- Testes automatizados
- Internacionalização (i18n)
- Melhorias na navegação do menu

---

## 📜 Licença

Distribuído sob a licença **MIT**.  
Veja o arquivo [`LICENSE`](LICENSE) para mais informações.

---

## 🙌 Agradecimentos

Este projeto nasceu da vontade de **aprender fazendo** — sem atalhos, sem frameworks mágicos, só lógica, persistência e boas práticas.  
Se ele te ajudar a entender melhor como um e-commerce funciona por dentro, já valeu a pena.

---

> ✨ **Próxima parada: Django. Mas o terminal nunca será esquecido.**
