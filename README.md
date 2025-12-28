# 🏦 Sistema Bancário em Python (CLI) — Atualização 3.0

Este projeto implementa um **sistema bancário em Python executado via terminal (CLI)**, evoluído de um exercício básico para um **sistema modular, auditável e extensível**, incorporando conceitos intermediários e avançados da linguagem.

A versão atual amplia o foco em **rastreabilidade, organização de dados e boas práticas**, aproximando o projeto de um cenário real de aplicação financeira.

---

## 🎯 Objetivo do Projeto

Simular um sistema bancário que permita:

- Cadastro e listagem de usuários
- Criação de contas correntes
- Depósitos e saques com regras de negócio
- Registro estruturado de transações
- Geração de relatórios com generators
- Iteração personalizada sobre transações
- **Registro automático e persistente de logs em arquivo**

---

## 🧠 Conceitos Trabalhados

O projeto exercita, de forma integrada, os seguintes conceitos:

### Fundamentos
- Funções e modularização
- Listas e dicionários
- Controle de fluxo (`while`, `if/elif/else`)
- Retorno e atualização de estado

### Conceitos Intermediários e Avançados
- Assinaturas avançadas de funções:
  - Argumentos somente posicionais (`/`)
  - Argumentos somente nomeados (`*`)
  - Combinação de ambos
- Decorators
- Generators (`yield`)
- Iteradores personalizados (`__iter__`, `__next__`)
- Manipulação de data e hora (`datetime`)
- Separação clara entre:
  - Orquestração (menu)
  - Regra de negócio (funções)
  - Persistência em memória (listas)
  - Auditoria (logs)

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

---

### 📋 Listagem de Usuários
- Lista todos os usuários cadastrados
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
- Implementada com **parâmetros somente posicionais**

---

### 💸 Saque
- Possui regras de negócio:
  - Saldo suficiente
  - Limite máximo por saque
  - Quantidade máxima de saques
- Atualiza saldo e contador de saques
- Registra a transação
- Implementada com **parâmetros somente nomeados**

---

### 📄 Extrato
- Exibe todas as transações registradas
- Mostra data, tipo e valor de cada movimentação
- Exibe o saldo final
- Implementada com **parâmetros mistos (posicional + nomeado)**

---

## 🧾 Registro de Transações (Modelo Estruturado)

As transações são armazenadas como uma **lista de dicionários**, permitindo filtragem, geração de relatórios e iteração:

```python
{
  "tipo": "depósito" | "saque",
  "valor": float,
  "data_hora": "YYYY-MM-DD HH:MM:SS"
}
```

---

## 🧩 Decorator de Log (Auditoria)

O sistema utiliza um **decorator de log** aplicado às principais funções do sistema.

### O decorator registra automaticamente:
- Data e hora da execução
- Nome da função chamada (tipo da operação)
- Persistência das informações em arquivo

### 📄 Arquivo de Log
- Nome do arquivo: `log.txt`
- Cada chamada de função gera uma nova linha
- Logs são **anexados ao final do arquivo**
- Permite auditoria, análise posterior e rastreabilidade completa

Esse mecanismo simula **logs reais de sistemas financeiros**, indo além da simples impressão em console.

---

## 🔁 Gerador de Relatórios (Generator)

O sistema inclui um generator que:

- Itera sobre as transações com `yield`
- Permite filtrar por tipo:
  - Todos
  - Depósitos
  - Saques
- Gera as transações sob demanda, sem criar listas intermediárias
- Ideal para grandes volumes de dados

---

## 📦 Iterador Personalizado

Foi implementado um iterador personalizado que:

- Utiliza `__iter__` e `__next__`
- Suporta filtro por tipo de transação
- Implementa paginação (quantidade fixa de transações por vez)
- Simula leitura incremental de dados
- Controla o fluxo de exibição no terminal

---

## 🧩 Estrutura do Código

- O `while True` atua apenas como **orquestrador do menu**
- Toda a lógica de negócio está encapsulada em funções
- O estado do sistema é mantido em memória por:
  - `saldo`
  - `extrato` (lista de transações)
  - `numero_saques`
  - `usuarios`
  - `contas`
- Logs são persistidos externamente em arquivo

---

## ▶️ Como Executar

1. Certifique-se de ter o **Python 3.8+** instalado
2. Clone o repositório
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```
4. Utilize o menu interativo no terminal

---

## 📌 Observação Final

Este projeto foi desenvolvido com **finalidade didática**, mas seguindo **padrões reais de organização, rastreabilidade e auditoria de sistemas**.

Ele serve como base sólida para:
- Estudos de Python intermediário/avançado
- Projetos de portfólio
- Evoluções futuras (persistência em banco de dados, POO completa, testes, etc.)
