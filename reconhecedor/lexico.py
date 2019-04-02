from .automato import Automato


def analiseLexica(automato: Automato, entrada: str):
    entrada += ' '
    coluna_atual = 0
    vetor_de_tokens = []
    vetor_de_tokens.append('inicio')
    tamanho_entrada = len(entrada)
    label_anterior = 'inicio'
    while len(entrada) > 1:
        saida, label, posicao = automato.test(entrada)

        # Se o automato retornar falso, um erro foi encontrado
        # Parar a análise e avisar o problema
        if saida is False:
            print(vetor_de_tokens)
            return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_tokens[-1]}\'')
        else:
            if (label_anterior == 'Inteiro') or (label_anterior == 'Real'):
                if (label != 'Espaco' and label != 'Simbolo especial' and label != 'Simbolo Composto'):
                    vetor_de_tokens.pop()
                    print(vetor_de_tokens)
                    return (False, f'Erro na coluna {coluna_atual + posicao} depois do token:\'{vetor_de_tokens[-1]}\'')

            token = entrada[:posicao]
            entrada = entrada[posicao:]
            print(f'Token "{token}" entrada "{entrada}"')
            vetor_de_tokens.append(token)
            # fim do token
        label_anterior = label
        coluna_atual += posicao
    return(True, vetor_de_tokens)
