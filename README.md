---

# 🏦 Sistema Bancário em Python (CLI) — Versão 4.0 (POO)

Este projeto implementa um **sistema bancário em Python executado via terminal (CLI)**, evoluído de um exercício básico para um **sistema totalmente orientado a objetos**, modular, auditável e extensível.

A versão atual aplica **Programação Orientada a Objetos (POO)** para modelar clientes, contas e transações, aproximando o projeto de um **cenário real de sistemas financeiros**.

---

## 🎯 Objetivo do Projeto

Simular um sistema bancário que permita:

* Cadastro e listagem de usuários
* Criação de contas correntes vinculadas a usuários
* Depósitos e saques com regras de negócio
* Registro estruturado de transações por conta
* Geração de relatórios com generators
* Iteração personalizada sobre transações
* **Registro automático e persistente de logs em arquivo**

---

## 🧠 Conceitos Trabalhados

O projeto exercita, de forma integrada, os seguintes conceitos da linguagem Python.

### Fundamentos

* Funções e modularização
* Controle de fluxo (`while`, `if/elif/else`)
* Estruturas de dados
* Entrada e saída via terminal (CLI)

### Conceitos Intermediários e Avançados

* **Programação Orientada a Objetos (POO)**

  * Classes
  * Encapsulamento
  * Herança
  * Composição
* Decorators
* Generators (`yield`)
* Iteradores personalizados (`__iter__`, `__next__`)
* Manipulação de data e hora (`datetime`)
* Separação clara entre:

  * Interface (menu)
  * Regras de negócio (classes)
  * Persistência em memória
  * Auditoria (logs)

---

## 🧩 Modelagem Orientada a Objetos

### Principais classes do sistema:

* **Cliente**
* **PessoaFisica**
* **Conta**
* **ContaCorrente**
* **Historico**
* **Transações (depósito e saque)**

Cada conta mantém:

* Saldo próprio
* Histórico independente de transações
* Regras de negócio encapsuladas

---

## ⚙️ Funcionalidades do Sistema

### 👤 Cadastro de Usuários

* Usuários são modelados como objetos (`PessoaFisica`)
* Cada usuário possui:

  * Nome
  * Data de nascimento
  * CPF (único)
  * Endereço
* O sistema impede o cadastro de CPFs duplicados

---

### 📋 Listagem de Usuários

* Lista todos os usuários cadastrados
* Exibe CPF, nome e data de nascimento
* Usuários são ordenados por CPF

---

### 💳 Criação de Conta Corrente

* Contas são modeladas como objetos (`ContaCorrente`)
* Cada conta possui:

  * Agência fixa `"0001"`
  * Número sequencial
  * Histórico próprio de transações
* Um usuário pode possuir **mais de uma conta**

---

### 💰 Depósito

* Aceita apenas valores positivos
* Atualiza o saldo da conta selecionada
* Registra automaticamente a transação no histórico

---

### 💸 Saque

* Possui regras de negócio:

  * Saldo suficiente
  * Limite máximo por saque
  * Quantidade máxima de saques
* Atualiza saldo e histórico
* Regras encapsuladas na classe `ContaCorrente`

---

### 📄 Extrato

* Exibe todas as transações da conta selecionada
* Mostra data, tipo e valor
* Exibe o saldo final da conta

---

## 🧾 Registro de Transações

As transações são armazenadas no histórico de cada conta em formato estruturado:

```python
{
  "tipo": "depósito" | "saque",
  "valor": float,
  "data_hora": "YYYY-MM-DD HH:MM:SS"
}
```

Esse modelo permite:

* Filtros
* Relatórios
* Iteração controlada
* Auditoria

---

## 🧩 Decorator de Log (Auditoria)

O sistema utiliza um **decorator de log** aplicado às principais operações.

### O decorator registra automaticamente:

* Data e hora da execução
* Nome da função chamada
* Argumentos e retorno
* Erros, quando ocorrem

### 📄 Arquivo de Log

* Nome: `log.txt`
* Registros anexados automaticamente
* Simula logs reais de sistemas financeiros

---

## 🔁 Gerador de Relatórios (Generator)

O sistema inclui um generator que:

* Percorre transações sob demanda
* Permite filtrar por:

  * Todas
  * Depósitos
  * Saques
* Evita criação de listas intermediárias
* Simula grandes volumes de dados

---

## 📦 Iterador Personalizado

Foi implementado um iterador que:

* Usa `__iter__` e `__next__`
* Suporta paginação
* Permite filtro por tipo de transação
* Controla a exibição incremental no terminal

---

## ▶️ Como Executar

1. Certifique-se de ter o **Python 3.8+** instalado
2. Clone o repositório
3. Execute o arquivo principal:

   ```bash
   python mini_sistema_bancario_desafio_dio.py
   ```
4. Utilize o menu interativo no terminal

---

## 📌 Observação Final

Este projeto foi desenvolvido com **finalidade didática**, mas seguindo **boas práticas reais de engenharia de software**.

Ele demonstra:

* Evolução de código procedural para POO
* Organização de responsabilidades
* Rastreabilidade e auditoria
* Uso consciente de recursos avançados da linguagem

Ideal para:

* Portfólio
* Estudos de Python intermediário/avançado
* Evoluções futuras (banco de dados, testes automatizados, APIs)

---
