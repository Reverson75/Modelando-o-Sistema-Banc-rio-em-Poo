from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta(ABC):
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        if valor > saldo:
            print("\n=== Operação falhou! Você não tem saldo suficiente. ===")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n=== Operação falhou! O valor informado é inválido. ===")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n=== Operação falhou! O valor informado é inválido. ===")
            return False

    @abstractmethod
    def __str__(self):
        pass

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)])
        if valor > self.limite:
            print("\n=== Operação falhou! O valor do saque excede o limite. ===")
            return False
        elif numero_saques >= self.limite_saques:
            print("\n=== Operação falhou! Número máximo de saques excedido. ===")
            return False
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class ContaPoupanca(Conta):
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/P:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

import textwrap

class ContaBancaria:
    def __init__(self, saldo_inicial=0, limite_conta=0, limite_saque_diario=0):
        self.saldo = saldo_inicial
        self.limite_conta = limite_conta
        self.limite_saque_diario = limite_saque_diario
        self.saque_diario_atual = 0

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if valor <= self.limite_saque_diario - self.saque_diario_atual and valor <= self.saldo:
            self.saldo -= valor
            self.saque_diario_atual += valor
            return True
        else:
            return False

    def verificar_saldo(self):
        return self.saldo

    def definir_limite_conta(self, limite):
        self.limite_conta = limite

    def definir_limite_saque_diario(self, limite):
        self.limite_saque_diario = limite

    def resetar_saque_diario(self):
        self.saque_diario_atual = 0


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []

    def __str__(self):
        return f"Cliente: {self.nome} (CPF: {self.cpf})"


def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = {"tipo": "Depósito", "valor": valor}

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    conta.depositar(valor)
    conta.resetar_saque_diario()
    cliente.contas[0] = conta


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = {"tipo": "Saque", "valor": valor}

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    if conta.sacar(valor):
        cliente.contas[0] = conta
        print("\n@@@ Saque realizado com sucesso! @@@")
    else:
        print("\n@@@ Saque não permitido! @@@")
        print(f"Saldo atual: R$ {conta.verificar_saldo():.2f}")
        print(f"Limite de saque diário restante: R$ {conta.limite_saque_diario - conta.saque_diario_atual:.2f}")


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = []  # Adicione o histórico de transações à conta para usar aqui

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.verificar_saldo():.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    cliente = Cliente(nome=nome, cpf=cpf)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    limite_conta = float(input("Informe o limite da conta: "))
    limite_saque_diario = float(input("Informe o limite de saque diário: "))

    conta = ContaBancaria(saldo_inicial=0, limite_conta=limite_conta, limite_saque_diario=limite_saque_diario)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()


main()
