from modules.identificadorHash import *
from modules.tabelahash import TabelaHash

class DistribuidorHash:

    def insereIdentificadorNaHash(tabela_identificadores:TabelaHash, identificador, categoria, nivel, tipo, deslocamento, passagem, rotulo, n_parametros, vetor_parametros_passagem, retorno, hash_ids):
        if (passagem and rotulo and n_parametros and retorno) is None:
            print('----- Inserindo variável simples na hash -----')
            variavel_simples = VariavelSimplesHash()
            variavel_simples.setIdentificador(identificador)
            variavel_simples.setCategoria(categoria)
            variavel_simples.setNivel(nivel)
            variavel_simples.setDeslocamento(deslocamento)
            variavel_simples.setTipo(tipo)

            tabela_identificadores.addItem(identificador, variavel_simples)
        elif(passagem is not None) and ((rotulo and n_parametros and retorno) is None):
            print('----- Inserindo parametro formal na hash -----')
            parametro_formal = ParametroFormalHash()
            parametro_formal.setIdentificador(identificador)
            parametro_formal.setCategoria(categoria)
            parametro_formal.setNivel(nivel)
            parametro_formal.setDeslocamento(deslocamento)
            parametro_formal.setPassagem(passagem)
            
            tabela_identificadores.addItem(identificador, parametro_formal)
        elif ((rotulo and n_parametros) is not None) and (tipo and deslocamento and retorno and passagem) is None:
            print('----- Inserindo procedimento na hash -----')
            procedimento = ProcedimentoHash()
            procedimento.setIdentificador(identificador)
            procedimento.setCategoria(categoria)
            procedimento.setNivel(nivel)
            procedimento.setRotulo(rotulo)
            procedimento.setNumeroParametros(n_parametros)
            procedimento.setVetorTipoPassagem(vetor_parametros_passagem)
            procedimento.setHash(hash_ids)

            tabela_identificadores.addItem(identificador, procedimento)
        elif(tipo and deslocamento and passagem is None) and ((retorno and rotulo and n_parametros) is not None):
            print('----- Inserindo função na hash -----')
            procedimento = FuncaoHash()
            procedimento.setIdentificador(identificador)
            procedimento.setCategoria(categoria)
            procedimento.setNivel(nivel)
            procedimento.setRotulo(rotulo)
            procedimento.setNumeroParametros(n_parametros)
            procedimento.setVetorTipoPassagem(vetor_parametros_passagem)
            procedimento.setRetorno(tipo)
            procedimento.setHash(hash_ids)

            tabela_identificadores.addItem(identificador, procedimento)
        else:
            print('Atenção, não foi possível inserir o identificador ', identificador, ' na hash!')


    def getItemHash(tabela_identificadores, identificador):
        return tabela_identificadores.getItem(identificador)