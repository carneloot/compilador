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
    def numero(self):
        self.matchTipo('Numero')

    @logFunc
    def bloco(self):
        self.parteDeclaracaoVariavel()

        while self.tokenAtual() == "procedure" or self.tokenAtual() == "function":
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

    @logFunc
    def parteDeclaracaoSubRotinas(self):
        if self.tokenAtual() == 'procedure':
            self.match('procedure')

            self.parteDeclaracaoProcedimento()

        elif self.tokenAtual() == 'function':
            self.match('function')

            self.parteDeclaracaoFuncao()

        self.match(';')

    @logFunc
    def parteDeclaracaoProcedimento(self):
        self.identificador()

        if self.tokenAtual() == '(':
            self.match('(')

            self.parametrosFormais()

        self.match(';')

        self.bloco()

    @logFunc
    def parteDeclaracaoFuncao(self):
        self.identificador()

        if self.tokenAtual() == '(':
            self.parametrosFormais()

        self.match(':')

        self.identificador()

        self.match(';')

        self.bloco()

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
            self.expressaoSimples()
        elif self.tokenAtual() == '-':
            self.match('-')
            self.expressaoSimples()
        elif self.tokenAtual() == 'or':
            self.match('or')
            self.expressaoSimples()

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
    def fator(self):

        if self.tipoAtual() == 'ID':
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

        elif self.tipoAtual() == 'Numero':
            self.numero()

        elif self.tokenAtual() == '(':
            self.match('(')
            self.expressao()
            self.match(')')
        else:
            self.match('not')
            self.fator()

    @logFunc
    def comandoComposto(self):
        self.match('begin')

        self.comando()

        while self.tokenAtual() == ';':
            self.match(';')
            self.comando()

        self.match('end')

    @logFunc
    def parametrosFormais(self):
        self.match('(')

        self.secaoParametrosFormais()

        while self.tokenAtual() == ';':
            self.match(';')

            self.secaoParametrosFormais()

        self.match(')')

    @logFunc
    def secaoParametrosFormais(self):
        if self.tokenAtual() == 'var':
            self.match('var')

        self.listaIdentificador()

        self.match(':')

        self.identificador()

    @logFunc
    def comando(self):
        self.comandoSemRotulo()

    @logFunc
    def comandoSemRotulo(self):
        if self.tokenAtual() == 'if':
            self.comandoCondicional()

        elif self.tokenAtual() == 'while':
            self.comandoRepetitivo()

        elif self.tokenAtual() == 'read':
            self.funcaoRead()

        elif self.tokenAtual() == 'write':
            self.funcaoWrite()

        elif self.tokenAtual() == 'begin':
            self.comandoComposto()

        else:
            self.identificador()

            if self.tokenAtual() == ':=':
                self.atribuicao()
            else:
                self.chamadaProcedimento()

    @logFunc
    def comandoCondicional(self):
        self.match('if')

        self.expressao()

        self.match('then')

        self.comandoSemRotulo()

        if self.tokenAtual() == 'else':
            self.match('else')

            self.comandoSemRotulo()

    @logFunc
    def comandoRepetitivo(self):
        self.match('while')

        self.expressao()

        self.match('do')

        self.comandoSemRotulo()

    @logFunc
    def funcaoRead(self):
        self.match('read')

        self.match('(')

        self.identificador()

        self.match(')')

    @logFunc
    def funcaoWrite(self):
        self.match('write')

        self.match('(')

        self.listaExpressao()

        self.match(')')

    @logFunc
    def atribuicao(self):
        self.match(':=')

        self.expressao()

    @logFunc
    def chamadaProcedimento(self):
        if self.tokenAtual() == '(':
            self.match('(')

            self.listaExpressao()

            self.match('(')

    @logFunc
    def listaExpressao(self):
        self.expressao()

        while self.tokenAtual() == ',':
            self.match(',')
            self.expressao()
