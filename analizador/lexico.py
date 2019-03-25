from ../reconhecedor.automato import Automato


def analiseLexica(automato: Automato, entrada: str):
    coluna_atual = 0
    vetor_de_tokens = []
    vetor_de_tokens.append('inicio')
    tamanho_entrada = len(entrada)
    for i in enumerate(entrada):
        saida, label, posicao = automato.test(entrada)

        # Se o automato retornar falso, um erro foi encontrado
        # Parar a análise e avisar o problema
        if saida is False:
            return (False, f'Erro na coluna {coluna_atual + posicao} depois do {vetor_de_tokens[-1]}')
        else:
            token = entrada[:posicao]
            entrada = entrada[posicao:]
            vetor_de_tokens.append(token)
            # fim do token

        coluna_atual += posicao
    return(True, vetor_de_tokens)
