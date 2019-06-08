def logFunc(function):
    def wrapper(self):
        print(f'Enter <{function.__name__}>')

        resultado = function(self)

        print(f'Exit <{function.__name__}>')

        return resultado

    return wrapper

class AnalisadorDescendente():

    def __init__(self, tokens):
        self.tokens = tokens
        self.currentToken = 0

    def lerTerminal(self, terminal):
        if self.tokens[self.currentToken][0] == terminal:
            self.currentToken += 1
            print(f'Li "{terminal}"')
            return True
        return False

    def run(self):
        self.program()

    def erro(self):
        print('Erro')

    # Funcoes de nao terminais

    @logFunc
    def program(self):

        if self.lerTerminal('program'):
            self.identificador()

            self.lerTerminal(';')

            self.bloco()

    @logFunc
    def identificador(self):
        if self.tokens[self.currentToken][1] == 'ID':
            print(f'ID \'{self.tokens[self.currentToken][0]}\'')
            self.currentToken += 1
        else:
            self.erro()

    @logFunc
    def bloco(self):
        self.parteDeclaracaoVariavel()

        self.parteDeclaracaoSubRotinas()

        self.comandoComposto()

    @logFunc
    def parteDeclaracaoVariavel(self):
        if self.lerTerminal('var'):

            self.declaracaoVariavel()

            # while self.lerTerminal(';'):
            #     self.declaracaoVariavel()

            self.lerTerminal(';')

    @logFunc
    def declaracaoVariavel(self):
        self.listaIdentificador()

        if self.lerTerminal(':'):
            self.tipo()
        else:
            self.erro()

    @logFunc
    def listaIdentificador(self):
        self.identificador()

        while self.lerTerminal(','):
            self.identificador()

    @logFunc
    def tipo(self):
        if self.lerTerminal('array'):
            self.indice()

            while self.lerTerminal(','):
                self.indice()

            if self.lerTerminal('of'):
                self.tipo()

            else:
                self.erro()

        else:
            self.identificador()

    @logFunc
    def indice(self):
        self.numero()

        if self.lerTerminal('..'):
            self.numero()

        else:
            self.erro()

    @logFunc
    def parteDeclaracaoSubRotinas(self):
        pass

    @logFunc
    def comandoComposto(self):
        pass

    @logFunc
    def expressao(self):
        self.expressaoSimples()
        if self.tokenAtual() == '=':
            self.match('=')
            self.expressaoSimples()

        elif self.tokenAtual() == '<>':
            self.match('<>')
            self.expressaoSimples()

        elif self.tokenAtual() == '<':
            self.match('<')
            self.expressaoSimples()

        elif self.tokenAtual() == '<=':
            self.match('<=')
            self.expressaoSimples()
        
        elif self.tokenAtual() == '>=':
            self.match('>=')
            self.expressaoSimples()
        
        elif self.tokenAtual() == '>':
            self.match('>')
            self.expressaoSimples()
    
    @logFunc
    def expressaoSimples(self):
        
        if self.tokenAtual() == '+':
            self.match('+')
        elif self.tokenAtual() == '-':
            self.match('-')
        
        self.termo()

        if self.tokenAtual() == '+':
            self.match('+')
            self.expressao_simples()
        elif self.tokenAtual() == '-':
            self.match('-')
            self.expressao_simples()
        elif self.tokenAtual() == 'or':
            self.match('or')
            self.expressao_simples()

    @logFunc
    def termo(self):
        self.fator()

        if self.tokenAtual() == '*':
            self.match('*')
            self.termo()

        elif self.tokenAtual() == 'div':
            self.match('div')
            self.termo()

        elif self.tokenAtual() == 'and':
            self.match('and')
            self.termo()
    
    @logFunc
    def fator():

        if self.tipoAtual() == 'ID/Reservada':
            self.identificador()
            # Duas coisas podem acontecer
            # Colchetes
            if self.tokenAtual() == '[':
                self.match('[')
                self.expressao()

                while self.tokenAtual() == ',':
                    self.match(',')
                    self.expressao()
                self.match(']')

            # Parênteses
            elif self.tokenAtual() == '(':
                self.match('(')
                self.expressao()

                while self.tokenAtual() == ',':
                    self.match(',')
                    self.expressao()
                self.match(')')


        elif self.tipoAtual() == 'Real' or self.tipoAtual() == 'Inteiro':
            self.numero()
        
        elif self.tokenAtual() == '(':
            self.match('(')
            self.expressao()
            self.match(')')


        self.match('not')
        self.fator()
        
