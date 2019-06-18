import tabelahash

class IdentificadorHash:

    def __init__(self, categoria: str):
        self._identificador = ''
        self._categoria = categoria
        self._nivel = 0 

    def getIdentificador(self):
        return self._identificador

    def getCategoria(self):
        return self._categoria

    def getNivel(self):
        return self._nivel

    def setIdentificador(self, identificador):
        self._identificador = identificador
    
    def setCategoria(self, categoria):
        self._categoria = categoria

    def setNivel(self, nivel):
        self._nivel = nivel
    
        
    

class VariavelSimplesHash(IdentificadorHash):
    def __init__(self):
        super(VariavelSimplesHash,self).__init__('variavelSimples')
        self._tipo = ''
        self._deslocamento = ''

    def getTipo(self):
        return self._tipo
    
    def getDeslocamento(self):
        return self._deslocamento
    
    def setTipo(self,tipo):
        self._tipo = tipo
    
    def setDeslocamento(self,deslocamento):
        self._deslocamento = deslocamento    

class ParametroFormalHash(IdentificadorHash):

    def __init__(self):
        super(ParametroFormalHash,self).__init__('parametroFormal')
        self._tipo = ''
        self._deslocamento = ''
        self._passagem = ''

    def getTipo(self):
        return self._tipo
    
    def getDeslocamento(self):
        return self._deslocamento
    
    def getPassagem(self):
        return self._passagem
    
    def setTipo(self,tipo):
        self._tipo = tipo
    
    def setDeslocamento(self,deslocamento):
        self._deslocamento = deslocamento    
    
    def setPassagem(self,passagem):
        self._passagem = passagem    

class ProcedimentoHash(IdentificadorHash):

    def __init__(self):
        super(ProcedimentoHash,self).__init__('procedimento')
        self._rotulo = ''
        self._numero_parametros = 0
        self._tipo_passagem = []

class FuncaoHash(IdentificadorHash):

    def __init__(self):
        super(FuncaoHash,self).__init__('funcao')
        self._rotulo = ''
        self._numero_parametros = 0
        self._tipo_passagem = []
        self._retorno = ''

class DistribuidorHash:

    def casoVarSimples(self, vetor_tokens, posicao_inicial, nivel):
        variavel_simples = VariavelSimplesHash()
        return variavel_simples

