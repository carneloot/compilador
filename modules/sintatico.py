from identificadorHash import *
from tabelahash import TabelaHash
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

    def __init__(self, tokens, tabela_ids):
        self.tokens = tokens
        self.currentToken = 0
        self.tabela_ids = tabela_ids
        self.deslocamento = 0

    def match(self, terminal):
        global TAB_NUM
        if self.tokenAtual() == terminal:
            tabs = '\t' * TAB_NUM
            print(f'{tabs}Li "{terminal}"')
        else:
            raise SyntaxError(f'Token esperado: \'{terminal}\'. Token lido: \'{self.tokenAtual()}\'')

        self.proximoToken()

    def tokenAtual(self):
        return self.tokens[self.currentToken][0]

    def proximoToken(self):
        self.currentToken += 1

    def matchTipo(self, tipo):
        global TAB_NUM
        if self.tipoAtual() == tipo:
            tabs = '\t' * TAB_NUM
            print(f'{tabs}{tipo} \'{self.tokenAtual()}\'')
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

            # Vai manter controle do nível lexico
            nivel = 0

            self.match('program')

            self.identificador(self.hash_ids, nivel, None, 'procedimento', None, None, '', 0, None, None, None)

            self.match(';')

            self.bloco(hash_ids, nivel)

            self.match('.')

    @logFunc
    def identificador(self, addHash=True, hash_ids, nivel, deslocamento, categoria, tipo, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno, hash_filha):

        if addHash:
            insereIdentificadorNaHash( hash_ids, self.tokenAtual(), categoria, nivel, tipo, deslocamento, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno, hash_filha)

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
    def bloco(self, hash_ids, nivel):
        deslocamento_anterior = self.deslocamento
        self.deslocamento = 0
        self.parteDeclaracaoVariavel(hash_ids, nivel)
        

        while self.tokenAtual() == "procedure" or self.tokenAtual() == "function":
            self.deslocamento += 1
            self.parteDeclaracaoSubRotinas(hash_ids, nivel)

        self.comandoComposto()
        self.deslocamento = deslocamento_anterior

    @logFunc
    def parteDeclaracaoVariavel(self, hash_ids, nivel):
        
        if self.tokenAtual() == 'var':
            self.match('var')

            self.declaracaoVariavel(hash_ids, nivel, True)

            while self.tipoAtual() == 'ID' \
                and self.tokenAtual() != 'function' and self.tokenAtual() != 'procedure':
                self.declaracaoVariavel(hash_ids, nivel, False)
        
    @logFunc
    def declaracaoVariavel(self, hash_ids, nivel, isFirst):
        vetor_ids = []
        self.listaIdentificador(hash_ids, nivel, is_parametro=False, is_first=isFirst, vetor_ids, None)

        self.match(':')

        tipo = self.tokenAtual
        self.tipo(nivel)

        # Editar identificadores, adicionando o tipo
        for id in vetor_ids:
            item = getItemHash(hash_ids, id)
            item.setTipo(tipo)

        self.match(';')
        

    @logFunc
    def listaIdentificador(self, hash_ids, nivel, is_parametro=False, is_first=True, vetor_ids, passagem):
        if is_parametro:
            if is_first:
                self.deslocamento = -3
            iteracao = -1
            categoria = 'parametro formal'
        else:
            if is_first:
                self.deslocamento = 0
            iteracao = 1
            categoria = 'variavel simples'
        
        vetor_ids.append(self.tokenAtual())
        
        self.identificador(addHash=True, hash_ids, nivel, self.deslocamento, categoria, None, passagem, None, None, None )
        self.deslocamento += iteracao

        while self.tokenAtual() == ',':
            self.match(',')
            vetor_ids.append(self.tokenAtual())
            self.identificador(addHash=True, hash_ids, nivel, self.deslocamento, categoria, None, passagem, None, None, None )
            self.deslocamento += iteracao


    @logFunc
    def tipo(self, nivel):
        
        if self.tipoAtual() == 'ID':
            self.identificador(addHash=False, nivel, self.deslocamento, 'Palavra_tipo', self.tokenAtual, None, None, None, None, None)
        if self.tipoAtual() == 'Reservada':
            self.reservada()

    @logFunc
    def indice(self):
        self.numero()

        self.match('..')

        self.numero()

    @logFunc
    def parteDeclaracaoSubRotinas(self, hash_ids, nivel):
        if self.tokenAtual() == 'procedure':
            self.parteDeclaracaoProcedimento(hash_ids, nivel)

        elif self.tokenAtual() == 'function':
            self.parteDeclaracaoFuncao(hash_ids, nivel)

        self.match(';')

    @logFunc
    def parteDeclaracaoProcedimento(self, hash_id, nivel):
        self.match('procedure')
        parametros = []
        nome_procedure = self.tokenAtual()
        hash_local = TabelaHash()
        self.identificador(addHash=True, hash_id, nivel, None, 'procedimento', None, None, '', 0, parametros, None, hash_local)

        if self.tokenAtual() == '(':
            self.parametrosFormais( hash_local, nivel + 1 , parametros)

        # Editar o procedimento com o numero de parametros
        item = getItemHash(hash_id, nome_procedure)
        item.setNuneroParametros( len(parametros) )
        self.match(';')

        self.bloco(hash_local, nivel + 1)

    @logFunc
    def parteDeclaracaoFuncao(self, hash_id, nivel):
        self.match('function')
        nome_funcao = self.tokenAtual()
        parametros = []
        hash_local = TabelaHash
        self.identificador(addHash=True, hash_id, nivel, None, 'procedimento', '', None, '', 0, parametros, '', hash_local)

        if self.tokenAtual() == '(':
            self.parametrosFormais(hash_local, nivel + 1, parametros)

        
        self.match(':')

        # Tipo de retorno:
        tipo = self.tokenAtual()
        self.identificador(addHash=False, None, None, None, None, None, None, None, None, None, None, None,)

        # Editar número de parametros, e tipo de retorno
        item = getItemHash(hash_id, nome_funcao)
        item.setTipo(tipo)
        item.setNuneroParametros(len(parametros))



        self.match(';')

        self.bloco(hash_local, nivel + 1)

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
    def parametrosFormais(self, hash_id, nivel, vetor_ids ):
        self.match('(')

        self.secaoParametrosFormais(hash_id, nivel, True, vetor_ids)

        while self.tokenAtual() == ';':
            self.match(';')

            self.secaoParametrosFormais(hash_id, nivel, False, vetor_ids)

        # Arrumando deslocamento dos parametros
        i = len(vetor_ids) - 1
        deslocamento = -3
        while i > 0:
            item = getItemHash( hash_id, vetor_ids[i] )
            item.setDeslocamento( deslocamento )
            deslocamento -= 1
            i -= 1

        self.match(')')

    @logFunc
    def secaoParametrosFormais(self, hash_id, nivel, is_first, vetor_ids):
        

        if self.tokenAtual() == 'procedure':
            self.match('procedure')
            self.listaIdentificador(hash_id, nivel, is_parametro=True, is_first=is_first, vetor_ids, False )

        else:
            passagem = False

            if self.tokenAtual() == 'function':
                self.match('function')
                passagem = None

            elif self.tokenAtual() == 'var':
                self.match('var')
                passagem = True
                

            vetor_local = []
            self.listaIdentificador(hash_id, nivel, is_parametro=True, is_first=False, vetor_local, passagem)

            self.match(':')

            # tipo

            tipo = self.tokenAtual
            self.tipo(nivel)

            # Editar identificadores, adicionando o tipo
            for id in vetor_ids:
                item = getItemHash(hash_id, id)
                item.setTipo(tipo)

            vetor_ids.extend(vetor_local)

            self.identificador(addHash = False, None, None, None, None, None, None, None, None, None)

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
