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
            print('Vetor de tokens:' + vetor_de_token_info)
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
            print(f'Token "{token}" entrada "{entrada}"')
            vetor_de_token_info.append((token, label))
            # fim do token
        label_anterior = label
        coluna_atual += posicao
    return(True, vetor_de_token_info)
