# 🏦 Sistema Bancário em Python (CLI) — Atualização 2.0

Este projeto implementa um **sistema bancário em Python executado via terminal (CLI)**, evoluído a partir de um exercício básico para um **sistema modular e extensível**, incorporando conceitos intermediários e avançados da linguagem.

O projeto foi desenvolvido com foco em **boas práticas, clareza arquitetural e domínio de recursos do Python**, indo além de um script procedural simples.

---

## 🎯 Objetivo do Projeto

Simular um sistema bancário que permita:

- Cadastro e listagem de usuários
- Criação de contas correntes
- Depósitos e saques com regras de negócio
- Registro estruturado de transações
- Geração de relatórios com generators
- Iteração personalizada sobre transações
- Registro automático de logs via decorators

---

## 🧠 Conceitos Trabalhados

O projeto exercita, de forma integrada, os seguintes conceitos:

### Fundamentos
- Funções e modularização
- Listas e dicionários
- Controle de fluxo (`while`, `if/elif/else`)
- Retorno e atualização de estado

### Conceitos Intermediários e Avançados
- Assinaturas avançadas de funções
  - Argumentos somente posicionais (`/`)
  - Argumentos somente nomeados (`*`)
  - Combinação de ambos
- Decorators
- Generators (`yield`)
- Iteradores personalizados (`__iter__`, `__next__`)
- Separação clara entre:
  - Orquestração (menu)
  - Regra de negócio (funções)
  - Persistência em memória (listas)

---

## ⚙️ Funcionalidades do Sistema

### 👤 Cadastro de Usuários
- Usuários são armazenados em uma lista
- Cada usuário possui:
  - Nome
  - Data de nascimento
  - CPF (único)
  - Endereço
- O sistema impede o cadastro de CPFs duplicados

### 📋 Listagem de Usuários
- Permite listar todos os usuários cadastrados
- Exibe CPF (ordenado), nome e data de nascimento
- Facilita a identificação para criação de contas

---

### 💳 Criação de Conta Corrente
- Cada conta possui:
  - Agência fixa `"0001"`
  - Número da conta sequencial
  - Usuário vinculado via CPF
- Uma conta só pode ser criada se o usuário existir

---

### 💰 Depósito
- Aceita apenas valores positivos
- Atualiza o saldo
- Registra a transação de forma estruturada
- Implementada com parâmetros somente posicionais

---

### 💸 Saque
- Possui regras de negócio:
  - Saldo suficiente
  - Limite máximo por saque
  - Quantidade máxima de saques
- Atualiza saldo e contador
- Registra a transação
- Implementada com parâmetros somente nomeados

---

### 📄 Extrato
- Exibe todas as transações registradas
- Mostra data, tipo e valor de cada movimentação
- Exibe o saldo final
- Implementada com parâmetros mistos (posicional + nomeado)

---

## 🧾 Registro de Transações (Modelo Estruturado)

As transações são armazenadas como uma **lista de dicionários**, permitindo filtragem e iteração:

```python
{
  "tipo": "deposito" | "saque",
  "valor": float,
  "data_hora": "YYYY-MM-DD HH:MM:SS"
}
```
## 🧩 Decorator de Log

O sistema utiliza um decorator de log que registra automaticamente:

- Data e hora da execução
- Nome da função chamada (tipo da operação)

O decorator é aplicado às principais funções do sistema, garantindo rastreabilidade sem repetição de código.

## 🔁 Gerador de Relatórios (Generator)

O sistema inclui um generator que:

- Itera sobre as transações com `yield`
- Permite filtrar por tipo:
  - Todos
  - Depósitos
  - Saques
- Gera as transações sob demanda, sem criar listas intermediárias

## 📦 Iterador Personalizado

Foi implementado um iterador personalizado que:

- Utiliza `__iter__` e `__next__`
- Suporta filtro por tipo de transação
- Implementa paginação (quantidade fixa de transações por vez)
- Simula leitura incremental de dados

## 🧩 Estrutura do Código

- O `while True` atua apenas como orquestrador do menu
- Toda a lógica de negócio está encapsulada em funções
- O estado do sistema é mantido em memória por:
  - `saldo`
  - `extrato` (lista de transações)
  - `numero_saques`
  - `usuarios`
  - `contas`

## ▶️ Como Executar

1. Certifique-se de ter o Python 3.8+ instalado
2. Clone o repositório
3. Execute o arquivo principal
4. Utilize o menu interativo no terminal

## 📌 Observação Final

Este projeto foi desenvolvido com intenção didática, mas seguindo padrões reais de organização de código. Serve como base para estudos de Python intermediário e para futuras evoluções do sistema.
