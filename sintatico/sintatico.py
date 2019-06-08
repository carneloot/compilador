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

        while self.getToken() == "procedure" or self.getToken() == "function":
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
        if self.getToken() == 'procedure':
            self.match('procedure')

            self.parteDeclaracaoProcedimento()

        elif self.getToken() == 'function':
            self.match('function')

            self.parteDeclaracaoFuncao()

        if self.getToken() == ';':
            self.match(';')    
            self.bloco() 

        self.match(';')

    @logFunc
    def parteDeclaracaoProcedimento(self):
        self.identificador()

            if not self.getToken() == ';':
                self.match(';')

                self.parametrosFormais()
    @logFunc
    def parteDeclaracaoFuncao(self):
        self.identificador()

            if not self.getToken() == ':':
                self.match(':')

                self.parametrosFormais()

            self.identificador()

    @logFunc
    def comandoComposto(self):
        self.match('begin')

        self.comando()

        while self.getToken(';') == ';':
            self.match(';')
            self.comando()

        self.match('end')

    @logFunc
    def parametrosFormais(self):
        self.match('(')
        
        if self.getToken('var') == 'var':
            self.match('var')

        self.identificador()

        while self.getToken(',') == ',':
            self.match(',')
            self.identificador()

        self.match(':')

        self.identificador()

        self.match(')')

    @logFunc
    def comando(self):
        if self.tipoAtual() == 'Real' or self.tipoAtual() == 'Inteiro':
            self.numero()

            self.match(':')
        
        self.comandoSemRotulo()