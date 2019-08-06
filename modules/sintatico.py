from modules.identificadorHash import *
from modules.distribuidorHash import DistribuidorHash
from modules.tabelahash import TabelaHash
import modules.ast as ast

class AnalisadorDescendente():

    def __init__(self, tokens, arqCodigo, tabela_ids):
        self.tokens = tokens
        self.arqCodigo = arqCodigo
        self.currentToken = 0
        self.tabela_ids = tabela_ids
        self.deslocamento = 0

        self.tree = ast.MainNode()

        self.scopeCommands = self.tree.command_list

    def match(self, terminal):
        if self.tokenAtual() == terminal:
            print(f'Li "{terminal}"')
            self.proximoToken()
            return terminal
        else:
            raise SyntaxError(f'{self.generateLink()} Token esperado: \'{terminal}\'. Token lido: \'{self.tokenAtual()}\'')
        return None

    def generateLink(self):
        tokenAtual = self.tokens[self.currentToken]
        return f'./{self.arqCodigo}:{tokenAtual.linha}:{tokenAtual.coluna}'

    def tokenAtual(self):
        return self.tokens[self.currentToken].token

    def proximoToken(self):
        self.currentToken += 1

    def matchTipo(self, tipo):
        if self.tipoAtual() == tipo:
            token = self.tokenAtual()
            print(f'{tipo} \'{self.tokenAtual()}\'')
            self.proximoToken()
            return token
        else:
            raise SyntaxError(f'{self.generateLink()} Tipo esperado: \'{tipo}\'. Tipo lido: \'{self.tipoAtual()}\'')
        return None

    def tipoAtual(self):
        return self.tokens[self.currentToken].tipo

    def run(self):
        return self.program()

    # Funcoes de nao terminais

    def program(self):
        # Vai manter controle do nível lexico
        nivel = 0

        self.match('program')

        self.identificador(True, self.tabela_ids, nivel, None, 'procedimento', None, None, '', 0, None, None, None)

        self.match(';')

        self.bloco(self.tabela_ids, nivel)

        self.match('.')

        return self.tree

    def identificador(self, addHash, hash_ids, nivel, deslocamento, categoria, tipo, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno, hash_filha):

        if addHash:
            DistribuidorHash.insereIdentificadorNaHash( hash_ids, self.tokenAtual(), categoria, nivel, tipo, deslocamento, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno, hash_filha)

        return ast.IdentifierNode(self.matchTipo('ID'))

    def numero(self):
        return ast.ConstNode('Numero', self.matchTipo('Numero'))

    def reservada(self):
        self.matchTipo('Reservada')

    def string(self):
        # Indices para remover as aspas
        return ast.ConstNode('String', self.matchTipo('String')[1:-1])

    def bloco(self, hash_ids, nivel):
        deslocamento_anterior = self.deslocamento
        self.deslocamento = 0
        self.parteDeclaracaoVariavel(hash_ids, nivel)


        while self.tokenAtual() == "procedure" or self.tokenAtual() == "function":
            self.deslocamento += 1
            self.parteDeclaracaoSubRotinas(hash_ids, nivel)

        self.comandoComposto()
        self.deslocamento = deslocamento_anterior

    def parteDeclaracaoVariavel(self, hash_ids, nivel):

        if self.tokenAtual() == 'var':
            self.match('var')

            self.declaracaoVariavel(hash_ids, nivel, True)

            while self.tipoAtual() == 'ID' \
                and self.tokenAtual() != 'function' and self.tokenAtual() != 'procedure':
                self.declaracaoVariavel(hash_ids, nivel, False)

    def declaracaoVariavel(self, hash_ids, nivel, isFirst):
        vetor_ids = []
        self.listaIdentificador(hash_ids, nivel, vetor_ids, None, is_parametro=False, is_first=isFirst)

        self.match(':')

        tipo = self.tokenAtual()

        self.tipo(nivel)

        # Editar identificadores, adicionando o tipo
        for identificador in vetor_ids:
            item = DistribuidorHash.getItemHash(hash_ids, identificador)
            item['valor'].setTipo(tipo)

        self.match(';')

    def listaIdentificador(self, hash_ids, nivel, vetor_ids, passagem, is_parametro=False, is_first=True):
        if is_parametro:
            if is_first:
                self.deslocamento = -3
            iteracao = -1
            categoria = 'parametro_formal'
        else:
            if is_first:
                self.deslocamento = 0
            iteracao = 1
            categoria = 'variavel_simples'

        vetor_ids.append(self.tokenAtual())

        self.identificador(True, hash_ids, nivel, self.deslocamento, categoria, None, passagem, None, None, None, None, None )
        self.deslocamento += iteracao

        while self.tokenAtual() == ',':
            self.match(',')
            vetor_ids.append(self.tokenAtual())
            self.identificador(True, hash_ids, nivel, self.deslocamento, categoria, None, passagem, None, None, None, None, None )
            self.deslocamento += iteracao

    def tipo(self, nivel):
        if self.tipoAtual() == 'ID':
            self.identificador(False, nivel, self.deslocamento, 'Palavra_tipo', self.tokenAtual, None, None, None, None, None, None, None)
        if self.tipoAtual() == 'Reservada':
            self.reservada()

    def indice(self):
        self.numero()

        self.match('..')

        self.numero()

    def parteDeclaracaoSubRotinas(self, hash_ids, nivel):
        if self.tokenAtual() == 'procedure':
            self.parteDeclaracaoProcedimento(hash_ids, nivel)

        elif self.tokenAtual() == 'function':
            self.parteDeclaracaoFuncao(hash_ids, nivel)

        self.match(';')

    def parteDeclaracaoProcedimento(self, hash_id, nivel):
        self.match('procedure')
        parametros = []
        nome_procedure = self.tokenAtual()
        hash_local = TabelaHash()
        self.identificador(True, hash_id, nivel, None, 'procedimento', None, None, '', 0, parametros, None, hash_local)

        if self.tokenAtual() == '(':
            self.parametrosFormais( hash_local, nivel + 1 , parametros)

        # Editar o procedimento com o numero de parametros
        item = DistribuidorHash.getItemHash(hash_id, nome_procedure)
        item['valor'].setNumeroParametros( len(parametros) )
        self.match(';')

        self.bloco(hash_local, nivel + 1)

    def parteDeclaracaoFuncao(self, hash_id, nivel):
        self.match('function')
        nome_funcao = self.tokenAtual()
        parametros = []
        hash_local = TabelaHash()
        # def identificador(self, addHash, hash_ids, nivel, deslocamento, categoria, tipo, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno, hash_filha):
        self.identificador(True, hash_id, nivel, None, 'procedimento', '', None, '', 0, parametros, '', hash_local)

        if self.tokenAtual() == '(':
            self.parametrosFormais(hash_local, nivel + 1, parametros)


        self.match(':')

        # Tipo de retorno:
        tipo = self.tokenAtual()
        self.identificador(False, None, None, None, None, None, None, None, None, None, None, None,)

        # Editar número de parametros, e tipo de retorno
        item = DistribuidorHash.getItemHash(hash_id, nome_funcao)
        item['valor'].setRetorno(tipo)
        item['valor'].setNumeroParametros(len(parametros))

        self.match(';')

        self.bloco(hash_local, nivel + 1)

    def expressao(self):
        expressionNode = self.expressaoSimples()

        if self.tokenAtual() == '=':
            expressionNode = ast.ExpressionNode(
                left=expressionNode,
                relation=self.match('='),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == '<>':
            expressionNode = ast.ExpressionNode(
                left=expressionNode,
                relation=self.match('<>'),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == '<':
            expressionNode = ast.ExpressionNode(
                left=expressionNode,
                relation=self.match('<'),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == '<=':
            expressionNode = ast.ExpressionNode(
                left=expressionNode,
                relation=self.match('<='),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == '>=':
            expressionNode = ast.ExpressionNode(
                left=expressionNode,
                relation=self.match('>='),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == '>':
            expressionNode = ast.ExpressionNode(
                left=expressionNode,
                relation=self.match('>'),
                right=self.expressaoSimples()
            )

        return expressionNode

    def expressaoSimples(self):

        beforeToken = None

        if self.tokenAtual() == '+':
            beforeToken = self.match('+')
        elif self.tokenAtual() == '-':
            beforeToken = self.match('-')

        result = self.termo()

        if beforeToken is not None:
            result = ast.ExpressionNode(
                relation=beforeToken,
                right=result
            )

        if self.tokenAtual() == '+':
            result = ast.ExpressionNode(
                left=result,
                relation=self.match('+'),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == '-':
            result = ast.ExpressionNode(
                left=result,
                relation=self.match('-'),
                right=self.expressaoSimples()
            )

        elif self.tokenAtual() == 'or':
            result = ast.ExpressionNode(
                left=result,
                relation=self.match('or'),
                right=self.expressaoSimples()
            )

        return result

    def termo(self):
        result = self.fator()

        if self.tokenAtual() == '*':
            result = ast.ExpressionNode(
                left=result,
                relation=self.match('*'),
                right=self.termo()
            )

        elif self.tokenAtual() == 'div':
            result = ast.ExpressionNode(
                left=result,
                relation=self.match('div'),
                right=self.termo()
            )

        elif self.tokenAtual() == 'and':
            result = ast.ExpressionNode(
                left=result,
                relation=self.match('and'),
                right=self.termo()
            )

        return result

    def fator(self):

        if self.tipoAtual() == 'ID':
            identificador = self.identificador(False, None, None, None, None, None, None, None, None, None, None, None )
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
                return self.chamadaProcedimento(identificador)

            return identificador

        elif self.tipoAtual() == 'Numero':
            return self.numero()

        elif self.tipoAtual() == 'String':
            return self.string()

        elif self.tokenAtual() == '(':
            self.match('(')
            expression = self.expressao()
            self.match(')')
            return expression
        else:
            return ast.ExpressionNode(
                relation=self.match('not'),
                right=self.fator()
            )

    def comandoComposto(self):
        self.match('begin')

        comando = self.comando()
        self.scopeCommands.append(comando)

        while self.tokenAtual() == ';':
            self.match(';')
            comando = self.comando()
            self.scopeCommands.append(comando)

        self.match('end')

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
            item = DistribuidorHash.getItemHash( hash_id, vetor_ids[i] )
            item['valor'].setDeslocamento( deslocamento )
            deslocamento -= 1
            i -= 1

        self.match(')')

    def secaoParametrosFormais(self, hash_id, nivel, is_first, vetor_ids):
        if self.tokenAtual() == 'procedure':
            self.match('procedure')
            self.listaIdentificador(hash_id, nivel, vetor_ids, False, is_parametro=True, is_first=is_first)

        else:
            passagem = False

            if self.tokenAtual() == 'function':
                self.match('function')
                passagem = None

            elif self.tokenAtual() == 'var':
                self.match('var')
                passagem = True


            vetor_local = []
            self.listaIdentificador(hash_id, nivel, vetor_local, passagem, is_parametro=True, is_first=False)

            self.match(':')

            # tipo

            tipo = self.tokenAtual()
            self.tipo(nivel)

            # Editar identificadores, adicionando o tipo
            for identificador in vetor_ids:
                item = DistribuidorHash.getItemHash(hash_id, identificador)
                item['valor'].setTipo(tipo)

            vetor_ids.extend(vetor_local)

            # self.identificador(False, None, None, None, None, None, None, None, None, None, None, None)

    def comando(self):
        return self.comandoSemRotulo()

    def comandoSemRotulo(self):
        if self.tokenAtual() == 'if':
            return self.comandoCondicional()

        elif self.tokenAtual() == 'while':
            return self.comandoRepetitivo()

        elif self.tokenAtual() == 'read':
            return self.funcaoRead()

        elif self.tokenAtual() == 'write':
            return self.funcaoWrite()

        elif self.tokenAtual() == 'begin':
            self.comandoComposto()
            return None

        else:
            identificador = self.identificador(False, None, None, None, None, None, None, None, None, None, None, None )

            if self.tokenAtual() == ':=':
                return self.atribuicao(identificador)
            else:
                return self.chamadaProcedimento()

    def comandoCondicional(self):
        self.match('if')

        ifNode = ast.IfNode(self.expressao())

        self.match('then')

        oldScope = self.scopeCommands
        self.scopeCommands = ifNode.then_commands

        comando = self.comandoSemRotulo()
        if comando is not None:
            ifNode.addThenCommand(comando)

        self.scopeCommands = oldScope

        if self.tokenAtual() == 'else':
            self.match('else')

            self.scopeCommands = ifNode.else_commands

            comando = self.comandoSemRotulo()
            if comando is not None:
                ifNode.addElseCommand(comando)

            self.scopeCommands = oldScope

        return ifNode

    def comandoRepetitivo(self):
        self.match('while')

        expression = self.expressao()

        whileNode = ast.WhileNode(expression)

        self.match('do')

        oldScope = self.scopeCommands
        self.scopeCommands = whileNode.command_list

        comando = self.comandoSemRotulo()
        if comando is not None:
            whileNode.addCommand(comando)

        self.scopeCommands = oldScope
        return whileNode

    def funcaoRead(self):
        self.match('read')

        self.match('(')

        readNode = ast.ReadNode()

        identificador = self.identificador(False, None, None, None, None, None, None, None, None, None, None, None )

        readNode.addVar(identificador)

        self.match(')')

        return readNode

    def funcaoWrite(self):
        self.match('write')

        self.match('(')

        writeNode = ast.WriteNode()

        writeNode.expression_list = self.listaExpressao()

        self.match(')')

        return writeNode

    def atribuicao(self, identificador):
        self.match(':=')

        expression = self.expressao()

        return ast.AttrNode(identificador, expression)

    def chamadaProcedimento(self, id):
        if self.tokenAtual() == '(':
            self.match('(')

            procCallNode = ast.ProcCallNode(id)

            procCallNode.expression_list = self.listaExpressao()

            self.match(')')

            return procCallNode

        return None

    def listaExpressao(self):
        expressionList = []

        expressionList.append(self.expressao())

        while self.tokenAtual() == ',':
            self.match(',')
            expressionList.append(self.expressao())

        return expressionList
