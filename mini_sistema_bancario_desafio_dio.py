from datetime import datetime
from functools import wraps

LOG_FILE = "log.txt"
MAX_LEN = 250

def _short(value, max_len=MAX_LEN):
  """Converte o valor para string curta (para não poluir o log)."""
  text = repr(value)
  if len(text) > max_len:
    return text[:max_len] + "...(truncado)"
  return text

def log_transacao(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
      resultado = func(*args, **kwargs)
      status = "OK"
      erro = ""
    except Exception as exc:
      resultado = None
      status = "ERRO"
      erro = f"{type(exc).__name__}: {exc}"

      linha_log = (
       f"{data_hora} | status={status} | func={func.__name__} | "
       f"args={_short(args)} | kwargs={_short(kwargs)} | erro={_short(erro)}"
      )
      with open(LOG_FILE, "a", encoding="utf-8") as arq:
        arq.write(linha_log + "\n")

      raise

    linha_log = (
       f"{data_hora} | status={status} | func={func.__name__} | "
       f"args={_short(args)} | kwargs={_short(kwargs)} | return={_short(resultado)}"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as arq:
      arq.write(linha_log + "\n")

    return resultado
  return wrapper

class Historico:
  def __init__(self):
    self.__transacoes = []

  @property
  def transacoes(self):
    return self.__transacoes

  def adicionar_transacao(self, transacao):
    self.__transacoes.append(transacao)

class Conta:
  def __init__(self):
    self.__saldo = 0.0
    self.__historico = Historico()

  @property
  def saldo(self):
    return self.__saldo

  @property
  def historico(self):
    return self.__historico

  def depositar(self, valor):
    if valor <= 0:
      print("Opração falhou! O valor informado é inválido")
      return False

    self.__saldo += valor

    transacao = {
        "tipo": "depósito",
        "valor": valor,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    self.__historico.adicionar_transacao(transacao)
    return True

  def sacar(self, valor):
    if valor <= 0:
      print("Operação falhou! O valor informado é inválido.")
      return False

    if valor > self.__saldo:
      print("Operação falhou! Você não tem saldo suficiente.")
      return False

    self.__saldo -= valor

    transacao = {
        "tipo": "saque", # Changed to 'saque' for consistency
        "valor": valor,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    self.__historico.adicionar_transacao(transacao)
    return True

class ContaCorrente(Conta):
  def __init__(self, limite=500, limite_saques=3):
    super().__init__()
    self._limite = limite
    self._limite_saques = limite_saques

  def sacar(self, valor):
    # ContaCorrente specific checks
    if valor > self._limite:
      print("Operação falhou! O valor do saque excedeu o limite.")
      return False

    qtd_saques = 0
    for t in self.historico.transacoes:
        if t["tipo"] == "saque":
            qtd_saques += 1

    if qtd_saques >= self._limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return False

    # If specific checks pass, call the base class sacar method
    return super().sacar(valor)

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def cpf(self):
        return self._cpf


menu = """

[u] Criar Usuário
[l] Listar Usuários
[c] Criar conta corrente
[d] Depositar
[s] Sacar
[e] Extrato
[r] Relatório (gerador)
[i] Iterar Transações (iterador)
[q] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

usuarios = []
contas = []
conta_poo = ContaCorrente(limite=500, limite_saques=3)

class IteradorTransacoes:
  def __init__(self, transacoes, tipo=None, page_size=5):
    self.transacoes = transacoes
    self.tipo = tipo
    self.page_size = page_size
    self.__index = 0

    if tipo is None:
      self.filtradas = transacoes
    else:
      self.filtradas = [t for t in transacoes if t["tipo"] == tipo]

  def __iter__(self):
    return self

  def __next__ (self):
    if self.__index >= len(self.filtradas):
      raise StopIteration

    inicio = self.__index
    fim = min(self.__index + self.page_size, len(self.filtradas))
    pagina = self.filtradas[inicio:fim]
    self.__index = fim
    return pagina

def listar_usuarios(usuarios):
  print("\n================ LISTA DE USUÁRIOS ================")

  if not usuarios:
    print("Nenhum usuário cadastrado.")
    print("==================================================")
    return

  usuarios_ordenados = sorted(usuarios, key=lambda u: u.cpf)

  for u in usuarios_ordenados:
    print(
        f"CPF: {u.cpf} | Nome: {u.nome} | Nascimento: {u.data_nascimento}"
    )


  print("==================================================")

def gerar_relatorio(transacoes, tipo=None):
  """
  Gera transações uma a uma.
  tipo=None -> retorna todas
  tipo="saque" ou "depostio" -> filtra por tipo
  """

  for t in transacoes:
    if tipo is None or t["tipo"]  == tipo:
      yield t

@log_transacao
def criar_usuario(usuarios, nome, data_nascimento, cpf, endereco):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Já existe um usuário com esse CPF.")
            return

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    usuarios.append(cliente)
    print("Usuário criado com sucesso!")


@log_transacao
def criar_conta_corrente(usuarios, contas, cpf):
    cliente = None

    for usuario in usuarios:
        if usuario.cpf == cpf:
            cliente = usuario
            break

    if not cliente:
        print("Usuário não encontrado. Conta não criada.")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(limite=500, limite_saques=3)

    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("Conta corrente criada com sucesso!")


@log_transacao
def depositar(saldo, valor, extrato, /):
  if valor > 0:
    saldo += valor
    extrato.append({
      "tipo": "depósito",
      "valor": valor,
      "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    })
  else:
    print("Operação falhou! O valor informado é inválido.")

  return saldo, extrato

@log_transacao
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
  excedeu_saldo = valor > saldo
  excedeu_limite = valor > limite
  excedeu_saques = numero_saques >= limite_saques

  if excedeu_saldo:
    print("Operação falhou! Você não tem saldo suficiente.")

  elif excedeu_limite:
    print("Operação falhou! O valor do saque excedeu o limite.")

  elif excedeu_saques:
    print("Operação falhou! Número máximo de saques excedido.")

  elif valor > 0:
    saldo -= valor
    extrato.append({
        "tipo": "saque",
        "valor": valor,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    numero_saques += 1
  else:
    print("Operação falhou! O valor informado é inválido.")

  return saldo, extrato, numero_saques

@log_transacao
def exibir_extrato(saldo, /, *, extrato):
  print("\n==========================EXTRATO==========================")

  if not extrato:
    print("Não foram realizadas movimentações.")
  else:
    for transacao in extrato:
      tipo = transacao["tipo"].capitalize()
      valor = transacao["valor"]
      data_hora = transacao["data_hora"]
      print(f"{data_hora} - {tipo}: R$ {valor:.2f}")

  print(f"\nSaldo: R$ {saldo:.2f}")
  print("============================================================")

def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None

    try:
        numero = int(input("Informe o número da conta: "))
    except ValueError:
        print("Número inválido.")
        return None

    if 1 <= numero <= len(contas):
        return contas[numero - 1]

    print("Conta não encontrada.")
    return None

while True:

    opcao = input(menu)

    if opcao == "u":
      nome = input("Informe o nome do usuário: ")
      data_nascimento = input("Informe a data de nascimento do usuário (dd/mm/aaaa): ")
      cpf = input ("Informe o CPF do usuário (somente números): ")
      cpf = "".join([c for c in cpf if c.isdigit()])
      endereco = input("Informe o endereço do usuário: ")

      criar_usuario(usuarios, nome, data_nascimento, cpf, endereco)

    elif opcao == "c":
      cpf = input("Informe o CPF do usuário:")
      cpf = "".join([c for c in cpf if c.isdigit()])

      criar_conta_corrente(usuarios, contas, cpf)

    elif opcao == "s":
        conta = selecionar_conta(contas)
        if conta:
            valor = float(input("Informe o valor do saque: "))
            conta.sacar(valor)
            print("Saldo atual:", conta.saldo)

    elif opcao == "l":
      listar_usuarios(usuarios)

    elif opcao == "e":
        conta = selecionar_conta(contas)
        if conta:
            print("\n==========================EXTRATO==========================")
            transacoes = conta.historico.transacoes

            if not transacoes:
                print("Não foram realizadas movimentações.")
            else:
                for t in transacoes:
                    print(f'{t["data_hora"]} - {t["tipo"].capitalize()}: R$ {t["valor"]:.2f}')

            print(f"\nSaldo: R$ {conta.saldo:.2f}")
            print("============================================================")


    elif opcao == "d":
        conta = selecionar_conta(contas)
        if conta:
            valor = float(input("Informe o valor do depósito: "))
            conta.depositar(valor)
            print("Saldo atual:", conta.saldo)

    elif opcao == "r":
      filtro = input("Filtrar por tipo? [t] todos | [d] depósitos | [s] saques: ").lower()

      if filtro == "d":
        tipo = "depósito"
      elif filtro =="s":
        tipo = "saque"
      else:
        tipo = None

      print("\n================ RELATÓRIO (GERADOR) ================")
      encontrou = False
      for t in gerar_relatorio(conta.historico.transacoes, tipo=tipo):
        encontrou = True
        print(f'{t["data_hora"]} - {t["tipo"].capitalize()}: R$ {t["valor"]:.2f}')
      if not encontrou:
            print("Nenhuma transação encontrada para o filtro escolhido.")
      print("=============================================")

    elif opcao == "i":
              filtro = input("Filtrar por tipo? [t] todos | [d] depósitos | [s] saques: ").lower()

              if filtro == "d":
                tipo = "depósito"
              elif filtro == "s":
                tipo = "saque"
              else:
                tipo = None

              try:
                page_size = int(input("Quantas transações por página? (ex.: 5): "))
                if page_size <= 0:
                    page_size = 5
              except ValueError:
                page_size = 5

              iterador = IteradorTransacoes(conta.historico.transacoes, tipo=tipo, page_size=page_size)
              print("\n================ ITERADOR PERSONALIZADO ===================")
              houve_algo = False
              for pagina in iterador:
                houve_algo = True
                for t in pagina:
                    print(f'{t["data_hora"]} - {t["tipo"].capitalize()}: R$ {t["valor"]:.2f}')
                input("\nPressione ENTER para continuar...")
                print("------------------------------------------------------------------")
              if not houve_algo:
                  print("Nenhuma transação encontrada para o filtro escolhido.")
              print("==========================================================")


    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
