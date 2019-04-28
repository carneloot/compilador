
# - Lê as palavras de um arquivo, coloca-as em um dicionário
#    e retorna-o.
# - Cada palavra no arquivo deve estar em uma linha, sem espaços
#    entre, antes ou mesmo depois de cada uma


def criar_palavras_reservadas(nome_arquivo: str):
    reservadas = open(nome_arquivo, "r")
    palavras = reservadas.read()
    palavras = palavras.split('\n')

    palavras_reservadas = {}

    for palavra in palavras:
        palavras_reservadas[palavra] = palavra

    return palavras_reservadas