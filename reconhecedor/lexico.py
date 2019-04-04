from .automato import Automato


def analiseLexica(automato: Automato, entrada: str):
    entrada += ' '
    coluna_atual = 0
    
    
    #vetor_de_token = (token, label)
    #print(vetor_de_token[0][1]) printa a label

    vetor_de_token_info = []
    vetor_de_token_info.append(('inicio', 'inicio'))

    # vetor_de_tokens = []
    # vetor_de_tokens.append('inicio')

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
                    print(vetor_de_token_info)
                    return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_token_info[-1][0]}\'')

            token = entrada[:posicao]
            entrada = entrada[posicao:]
            print(f'Label "{label}"')
            print(f'Token "{token}" entrada "{entrada}"')
            print(f'Token "{token[-1]}"')
            if(label == 'Real') and (entrada[0] == ' '):  # CHECA SE HÁ UM ESPAÇO APÓS UM REAL OU SEJA, "3.3" OU "3."
                if entrada != ' ':  # CHECA SE NÃO É O FINAL DA STRING
                    if token[-1] == '.':  # CHECA SE ESTA NO FORMATO "2."
                        return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_token_info[-1][0]}\'')
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
