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
    
    def getRotulo(self):
        return self._rotulo
    
    def getNumeroParametros(self):
        return self._numero_parametros
    
    def getVetorTipoPassagem(self):
        return self._tipo_passagem
    
    def setRotulo(self,rotulo):
        self._rotulo = rotulo
    
    def setNumeroParametros(self,numero_parametros):
        self._numero_parametros = numero_parametros    
    
    def setVetorTipoPassagem(self,tipo_passagem):
        self._tipo_passagem = tipo_passagem    


class FuncaoHash(IdentificadorHash):

    def __init__(self):
        super(FuncaoHash,self).__init__('funcao')
        self._rotulo = ''
        self._numero_parametros = 0
        self._tipo_passagem = []
        self._retorno = ''
    
    def getRotulo(self):
        return self._rotulo
    
    def getNumeroParametros(self):
        return self._numero_parametros
    
    def getVetorTipoPassagem(self):
        return self._tipo_passagem
    
    def getRetorno(self):
        return self._retorno
    
    def setRotulo(self,rotulo):
        self._rotulo = rotulo
    
    def setNumeroParametros(self,numero_parametros):
        self._numero_parametros = numero_parametros    
    
    def setVetorTipoPassagem(self,tipo_passagem):
        self._tipo_passagem = tipo_passagem    
    
    def setRetorno(self,retorno):
        self._retorno = retorno

class DistribuidorHash:

    def insereIdentificadorNaHash(self, tabela_identificadores, identificador, categoria, nível, tipo, deslocamento, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno):
        if (passagem and rotulo and n_parametros and retorno) is None: 
            variavel_simples = VariavelSimplesHash()
            variavel_simples.setIdentificador(identificador)
            variavel_simples.setCategoria(categoria)
            variavel_simples.setNivel(nivel)
            variavel_simples.setDeslocamento(deslocamento)

            tabela_identificadores.addItem(identificador, variavel_simples)
        elif(passagem is not None) and ((rotulo and n_parametros and retorno) is None):
            parametro_formal = ParametroFormalHash()
            parametro_formal.setIdentificador(identificador)
            parametro_formal.setCategoria(categoria)
            parametro_formal.setNivel(nivel)
            parametro_formal.setDeslocamento(deslocamento)
            parametro_formal.setPassagem(passagem)

            tabela_identificadores.addItem(identificador, parametro_formal)
        elif( (rotulo and n_parametros) is not None) and (tipo and deslocamento and retorno and passagem) is None):
            procedimento = ProcedimentoHash()
            procedimento.setIdentificador(identificador)
            procedimento.setCategoria(categoria)
            procedimento.setNivel(nivel)
            procedimento.setRotulo(rotulo)
            procedimento.setNumeroParametros(n_parametros)
            procedimento.setVetorTipoPassagem(vetor_parametros_passagem)

            tabela_identificadores.addItem(identificador, procedimento)
        elif(tipo and deslocamento and passagem is None) and ((retorno and rotulo and n_parametros) is not None):
            procedimento = ProcedimentoHash()
            procedimento.setIdentificador(identificador)
            procedimento.setCategoria(categoria)
            procedimento.setNivel(nivel)
            procedimento.setRotulo(rotulo)
            procedimento.setNumeroParametros(n_parametros)
            procedimento.setVetorTipoPassagem(vetor_parametros_passagem)

            tabela_identificadores.addItem(identificador, procedimento)