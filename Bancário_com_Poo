from abc import ABC,abstractclassmethod,abstractproperty
abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self,endereço):
        self.emdereço = endereço
        self.contas = []
        
    def realizar_transaçao(self,conta, transaçao): 
        self.registrar(conta)
           
    def adicionar_conta(self, cota):
        self.contas.append(conta)
        
          
class pessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf endereço):
        super().__init__(endereço)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self. cpf= cpf
        

class contas:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "001"
        self._cliente = cliente 
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls,cliente.numero) 
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property  
    def numero(self):
        return self.numero 
    
    @property
    def agencia(self):
        return self._agencia 
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        saldo= self._saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\n === Operaçao falhou! Você nao tem saldo suficiente.@@@")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado e invalido.@@@")
            
        return False
    
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor 
            print("\n=== Deposito realizado com sucesso! ===")
            
        else:
            print("\n@@@ Operação falhou! O valor informado e inválido.@@@")
            return False
        
        return True
    
class contacorrente(contas):
    def __init__(self, numero, cliente,limite=500,limite_saques=3):
        super().__init__(numero, cliente)
        self.limite=limite 
        self.limite_saques = limite_saques
        
    def sacar(self,valor):
        numero_saques = len(
            [transaçao for transaçao in self.historico.transaçoes if transaçao ["tipo"] == Saque.__name__]
            
        )   
    
        excedeu_limite = valor > self.limite 
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print ("\n@@@ Operaçao falhou! O valor do saque excede o limite.@@@")
            
        elif excedeu_saques:
            print("\n@@@ Operaçao falhou! Numero maximo de saques excedido.@@@")
            
        else:
            return super().sacar(valor) 
        
        return False 
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.clinte.nome}
        """
            

class Historico:
    def __init__(self):
        self._transaçoes = []
        
    @property
    def transaçoes(self):
        return self.transaçoes
    
    def adicionar_transaçao( self, transaçao):
        self._transaçoes.append(
           
            {
                "tipo": transaçao.__class__.__name__,
                "valor": transaçao.valor, 
                "data": datetime.now().strtime
                (" %d-$m-%y"  %H:%M:%s),
            }
        )    
        

class transaçao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self,conta):
        pass

class Saques( transaçao ):
    def __init__(self,valor):
        self._valor = valor 
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transaçao = conta.sacar(self.valor)
        
        if sucesso_transaçao:
            conta.historico.adicionar_transaçao(self)
                
  
class Deposito( transaçao):
    def __init__(self,valor):
        self._valor= valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transaçao = conta.depositar(self.valor)
        
        if sucesso_transaçao:
            conta.historico.adicionar_transaçao(self)
                

    
