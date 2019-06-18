TAB_NUM = 0

def logFunc(function):
    def wrapper(self):
        global TAB_NUM
        tabs = '\t' * TAB_NUM
        print(f'{tabs}Enter <{function.__name__}>')
        TAB_NUM += 1

        resultado = function(self)

        TAB_NUM -= 1
        print(f'{tabs}Exit <{function.__name__}>')

        return resultado

    return wrapper

class AnalisadorDescendente():

    def __init__(self, tokens, arqCodigo):
        self.tokens = tokens
        self.arqCodigo = arqCodigo
        self.currentToken = 0

    def match(self, terminal):
        global TAB_NUM
        if self.tokenAtual() == terminal:
            tabs = '\t' * TAB_NUM
            print(f'{tabs}Li "{terminal}"')
        else:
            raise SyntaxError(f'{self.generateLink()} Token esperado: \'{terminal}\'. Token lido: \'{self.tokenAtual()}\'')

        self.proximoToken()

    def generateLink(self):
        tokenAtual = self.tokens[self.currentToken]
        return f'./{self.arqCodigo}:{tokenAtual.linha}:{tokenAtual.coluna}'

    def tokenAtual(self):
        return self.tokens[self.currentToken].token

    def proximoToken(self):
        self.currentToken += 1

    def matchTipo(self, tipo):
        global TAB_NUM
        if self.tipoAtual() == tipo:
            tabs = '\t' * TAB_NUM
            print(f'{tabs}{tipo} \'{self.tokenAtual()}\'')
        else:
            raise SyntaxError(f'{self.generateLink()} Tipo esperado: \'{tipo}\'. Tipo lido: \'{self.tipoAtual()}\'')

        self.proximoToken()

    def tipoAtual(self):
        return self.tokens[self.currentToken].tipo

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

            self.match('.')

    @logFunc
    def identificador(self):
        self.matchTipo('ID')

    @logFunc
    def numero(self):
        self.matchTipo('Numero')

    @logFunc
    def reservada(self):
        self.matchTipo('Reservada')

    @logFunc
    def string(self):
        self.matchTipo('String')

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

            while self.tipoAtual() == 'ID' \
                and self.tokenAtual() != 'function' and self.tokenAtual() != 'procedure':
                self.declaracaoVariavel()

    @logFunc
    def declaracaoVariavel(self):
        self.listaIdentificador()

        self.match(':')

        self.tipo()

        self.match(';')

    @logFunc
    def listaIdentificador(self):
        self.identificador()

        while self.tokenAtual() == ',':
            self.match(',')
            self.identificador()

    @logFunc
    def tipo(self):
        if self.tipoAtual() == 'ID':
            self.identificador()
        elif self.tipoAtual() == 'Reservada':
            self.reservada()

    @logFunc
    def indice(self):
        self.numero()

        self.match('..')

        self.numero()

    @logFunc
    def parteDeclaracaoSubRotinas(self):
        if self.tokenAtual() == 'procedure':
            self.parteDeclaracaoProcedimento()

        elif self.tokenAtual() == 'function':
            self.parteDeclaracaoFuncao()

        self.match(';')

    @logFunc
    def parteDeclaracaoProcedimento(self):
        self.match('procedure')

        self.identificador()

        if self.tokenAtual() == '(':
            self.match('(')

            self.parametrosFormais()

        self.match(';')

        self.bloco()

    @logFunc
    def parteDeclaracaoFuncao(self):
        self.match('function')

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

        elif self.tipoAtual() == 'String':
            self.string()

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

        if self.tokenAtual() == 'procedure':
            self.match('procedure')

            self.listaIdentificador()

        else:
            if self.tokenAtual() == 'function':
                self.match('function')

            elif self.tokenAtual() == 'var':
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