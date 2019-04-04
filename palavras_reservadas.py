
# - Lê as palavras de um arquivo, coloca-as em um dicionário
#    e retorna-o.
# - Cada palavra no arquivo deve estar em uma linha, sem espaços
#    entre, antes ou mesmo depois de cada uma


def criar_palavras_reservadas(nome_arquivo: str):

    print("\nLOG:Iniciando leitura de palavras reservadas.")

    reservadas = open(nome_arquivo, "r")
    palavras = reservadas.readlines()

    palavras_reservadas = {}

    i = 0
    for palavra in palavras:
        palavras_reservadas[palavra] = i
        i = i + 1

    print("LOG:Palavras lidas com sucesso.\n")

    return palavras_reservadas
