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

    def match(self, terminal):
        if self.tokenAtual() == terminal:
            print(f'Li "{terminal}"')
        else:
            raise SyntaxError(f'Token esperado: \'{terminal}\'. Token lido: \'{self.tokenAtual()}\'')

        self.proximoToken()

    def tokenAtual(self):
        return self.tokens[self.currentToken][0]

    def proximoToken(self):
        self.currentToken += 1

    def matchTipo(self, tipo):
        if self.tipoAtual() == tipo:
            print(f'{tipo} \'{self.tokenAtual()}\'')
        else:
            raise SyntaxError(f'Tipo esperado: \'{tipo}\'. Tipo lido: \'{self.tipoAtual()}\'')

        self.proximoToken()

    def tipoAtual(self):
        return self.tokens[self.currentToken][1]

    def run(self):
        self.program()

    # Funcoes de nao terminais

    @logFunc
    def program(self):

        if self.tokenAtual() == 'program':
            self.match('program')

            self.identificador()

            self.match(';')

            self.bloco()

    @logFunc
    def identificador(self):
        self.matchTipo('ID')

    @logFunc
    def bloco(self):
        self.parteDeclaracaoVariavel()

        self.parteDeclaracaoSubRotinas()

        self.comandoComposto()

    @logFunc
    def parteDeclaracaoVariavel(self):
        if self.tokenAtual() == 'var':
            self.match('var')

            self.declaracaoVariavel()

            # while self.lerTerminal(';'):
            #     self.declaracaoVariavel()

            self.match(';')

    @logFunc
    def declaracaoVariavel(self):
        self.listaIdentificador()

        self.match(':')

        self.tipo()

    @logFunc
    def listaIdentificador(self):
        self.identificador()

        while self.tokenAtual() == ',':
            self.match(',')
            self.identificador()

    @logFunc
    def tipo(self):
        self.identificador()

    @logFunc
    def indice(self):
        self.numero()

        self.match('..')

        self.numero()
