from .automato import Automato
from .palavras_reservadas import criar_palavras_reservadas


def analiseLexica(automato: Automato, nome_arq_codigo: str, nome_arq_palavras_reservadas: str):
    qtd_linhas = 0
    vetor_de_token_info = []

    palavras_reservadas = criar_palavras_reservadas(nome_arq_palavras_reservadas)

    with open(nome_arq_codigo, 'r') as arq:
        conteudo_arq = arq.read()
        conteudo_arq = conteudo_arq.split('\n')

        while(qtd_linhas < len(conteudo_arq)):
            linha = conteudo_arq[qtd_linhas]

            linha_correta, tokens_info = classificaTokens(automato, linha)
            
            if linha_correta is True:
                tokens_info.pop(0)
                for token_info in tokens_info:
                    vetor_de_token_info.append(token_info)    
            else:
                erro_resultado = tokens_info
                print(f'ERRO NA LINHA {qtd_linhas}')
                break

            qtd_linhas += 1
    vetor_de_token_info.pop()
    
    vetor_identificadores = []

    contador = 0
    while contador < len(vetor_de_token_info):
        #AQUI LIDAREMOS COM A CLASSIFICAÇÃO DOS TOKENS ENTRE IDENTIFICADORES E PALAVRAS RESERVADAS
        if(vetor_de_token_info[contador][1] == 'ID/Reservada'):

            token = vetor_de_token_info[contador][0]
            token_maiusculo = token.upper()

            if(token_maiusculo in palavras_reservadas):
                # checar se há forma melhor de alterar tupla
                vti = list(vetor_de_token_info)
                par_token_info = list(vti[contador])
                par_token_info[1] = 'Reservada'
                vti[contador] = tuple(par_token_info)
                vetor_de_token_info = tuple(vti)

            else:
                vti = list(vetor_de_token_info)
                par_token_info = list(vti[contador])
                par_token_info[1] = 'ID'
                vti[contador] = tuple(par_token_info)
                vetor_de_token_info = tuple(vti)

                vetor_identificadores.append(par_token_info[0])

            contador += 1
        else:
            contador += 1

    return (vetor_de_token_info, vetor_identificadores)


def classificaTokens(automato: Automato, entrada: str):
    entrada += ' '
    coluna_atual = 0

    vetor_de_token_info = []
    vetor_de_token_info.append(('inicio', 'inicio'))

    tamanho_entrada = len(entrada)
    label_anterior = 'inicio'
    while len(entrada) > 1:
        saida, label, posicao = automato.test(entrada)

        # Se o automato retornar falso, um erro foi encontrado:
        #   Parar a análise e avisar o problema
        if saida is False:
            return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_token_info[-1][0]}\'')
        else:
            # Ainda pode existir um erro:
            if (label_anterior == 'Inteiro') or (label_anterior == 'Real'):
                if (label != 'Espaco' and label != 'Simbolo especial' and label != 'Simbolo Composto'):
                    vetor_de_token_info.pop()
                    return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_token_info[-1][0]}\'')

            token = entrada[:posicao]
            entrada = entrada[posicao:]
            # print(f'Label "{label}"')
            # print(f'Token "{token}" entrada "{entrada}"')
            # print(f'Token "{token}"')
            if(label == 'Real') and (entrada[0] == ' '):  # CHECA SE HÁ UM ESPAÇO APÓS UM REAL OU SEJA, "3.3" OU "3."
                if entrada != ' ':  # CHECA SE NÃO É O FINAL DA STRING
                    if token[-1] == '.':  # CHECA SE ESTA NO FORMATO "2."
                        return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_token_info[-1][0]}\', identificado como um numero Real incompleto devido a existência de um ponto desnecessário')
            if (label == 'Real') and ((ord(entrada[0]) >= 65 and ord(entrada[0]) <= 90) or (ord(entrada[0]) >= 97 and ord(entrada[0]) <= 122)):
                # CHECA SE É "3.3A" OU "3.A"
                if token[-1] != '.':  # ERRO SE FOR "3.3A"
                    return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_token_info[-1][0]}\'')
                token = token.split('.', 1)
                token = token[0]
                label = 'Inteiro'
                vetor_de_token_info.append((token, label))
                token = '.'
                label = 'Simbolo especial'

            vetor_de_token_info.append((token, label))
            # fim do token
        label_anterior = label
        coluna_atual += posicao

    return(True, vetor_de_token_info)
