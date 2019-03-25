import ../reconhecedor.automato


def analiseLexica(automato: automato, entrada: str):
    for i in enumerate(entrada):
        saida = automato.test(entrada)

        # Se o automato retornar falso, um erro foi encontrado
        # Parar a análise e avisar o problema
        if saida[0] is False:
            return (False, f'Erro na coluna {coluna_atual + saida[2]}'


    
