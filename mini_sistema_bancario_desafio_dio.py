from datetime import datetime
from functools import wraps

def log_transacao(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tipo = func.__name__ 
    print(f"[LOG] {data_hora} | Transação: {tipo}")
    return func(*args, **kwargs)
  return wrapper

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

  def __next__(self):
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

  usuarios_ordenados = sorted(usuarios, key=lambda u: u["cpf"])

  for u in usuarios_ordenados:
    print(f'CPF: {u["cpf"]} | Nome {u["nome"]} | Nascimento: {u["data_nascimento"]}')

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
        if usuario["cpf"] == cpf:
            print("Já existe um usuário com esse CPF.")
            return

    usuario = {
      "nome": nome,
      "data_nascimento": data_nascimento,
      "cpf": cpf,
      "endereco": endereco
    }

    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

@log_transacao
def criar_conta_corrente(usuarios, contas, cpf):
  usuario_encontrado = None

  for usuario in usuarios:
    if usuario["cpf"] == cpf:
      usuario_encontrado = usuario
      break

  if not usuario_encontrado:
    print("Usuario não encontrado. Conta não criada")
    return

  numero_conta = len(contas) + 1

  conta = {
      "agencia": "0001",
      "numero_conta": numero_conta,
      "usuario": usuario_encontrado
  }

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
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES 
        )

    elif opcao == "l":
      listar_usuarios(usuarios)

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "d": 
      valor = float(input("Informe o valor do depósito:"))
      saldo, extrato = depositar(saldo, valor, extrato)

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
      for t in gerar_relatorio(extrato, tipo=tipo):
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

              iterador = IteradorTransacoes(extrato, tipo=tipo, page_size=page_size)

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
