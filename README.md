# 🏦 Sistema Bancário em Python (CLI)

Este projeto implementa um **sistema bancário simples em Python**, executado via terminal (CLI), desenvolvido como exercício prático para consolidar conceitos fundamentais da linguagem e boas práticas de programação.

O foco principal do código é **organização, clareza e uso correto de funções**, indo além de um script procedural simples.

---

## 🎯 Objetivo do Projeto

Simular um sistema bancário básico que permita:
- Cadastro de usuários
- Criação de contas correntes
- Realização de depósitos
- Realização de saques com regras
- Visualização de extrato

Tudo isso utilizando **funções bem definidas**, controle de estado e regras explícitas de passagem de parâmetros.

---

## 🧠 Conceitos Trabalhados

Este projeto foi construído para exercitar:

- Funções em Python
- Separação de responsabilidades
- Uso de listas e dicionários
- Controle de fluxo (`while`, `if/elif/else`)
- Retorno e atualização de estado
- **Assinaturas avançadas de funções**:
  - Argumentos somente posicionais (`/`)
  - Argumentos somente nomeados (`*`)
  - Combinação de ambos

---

## ⚙️ Funcionalidades

### 👤 Cadastro de Usuários
- Usuários são armazenados em uma lista
- Cada usuário possui:
  - Nome
  - Data de nascimento
  - CPF (único)
  - Endereço
- Não é permitido cadastrar dois usuários com o mesmo CPF

### 💳 Criação de Conta Corrente
- Cada conta possui:
  - Agência fixa `"0001"`
  - Número da conta sequencial
  - Usuário vinculado
- Uma conta só pode ser criada se o CPF do usuário existir

### 💰 Depósito
- Aceita apenas valores positivos
- Atualiza o saldo
- Registra a operação no extrato
- Implementada com **parâmetros somente posicionais**

### 💸 Saque
- Possui regras:
  - Saldo suficiente
  - Limite máximo por saque
  - Quantidade máxima de saques
- Atualiza saldo, extrato e contador de saques
- Implementada com **parâmetros somente nomeados**

### 📄 Extrato
- Exibe todas as movimentações realizadas
- Mostra o saldo final
- Implementada com **parâmetros mistos (posicional + nomeado)**

---

## 🧩 Estrutura do Código

- O `while True` atua apenas como **orquestrador do menu**
- Toda a lógica de negócio está isolada em funções
- O estado do sistema é mantido por variáveis e listas globais:
  - `saldo`
  - `extrato`
  - `numero_saques`
  - `usuarios`
  - `contas`

---

## ▶️ Como Executar

1. Certifique-se de ter o Python 3.8+ instalado
2. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
