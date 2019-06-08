def error():
    print('Erro!')

def lerToken(tokens, indice, token):
    # print('Verificando', tokens[indice], '==', token)
    if tokens[indice] == token:
        print('Li', token)
        return True
    return False

# F = 
#     'a' |
#     'b' |
#     ( '(', E, ')' )
# ;
def F(tokens, indiceProx):
    print('Enter F')
    if lerToken(tokens, indiceProx, 'a') or lerToken(tokens, indiceProx, 'b'):
        indiceProx += 1
    else:
        if lerToken(tokens, indiceProx, '('):
            indiceProx += 1

            indiceProx = E(tokens, indiceProx)

            if lerToken(tokens, indiceProx, ')'):
                indiceProx += 1
            else:
                error()

        else:
            error()

    print('Exit F')
    return indiceProx

# T = 
#     ( F, '*', T ) |
#     F   
# ;
def T(tokens, indiceProx):
    print('Enter T')
    indiceProx = F(tokens, indiceProx)

    if lerToken(tokens, indiceProx, '*'):
        indiceProx += 1
        indiceProx = T(tokens, indiceProx)

    print('Exit T')
    return indiceProx

# E = 
#     ( T, '+', E ) |
#     T
# ;
def E(tokens, indiceProx):
    print('Enter E')
    indiceProx = T(tokens, indiceProx)

    if lerToken(tokens, indiceProx, '+'):
        indiceProx += 1
        indiceProx = E(tokens, indiceProx)

    print('Exit E')
    return indiceProx

if __name__ == "__main__":
    tokens = [
        'a',
        '+',
        'b',
        'EOF',
    ]

    indiceProx = 0

    indiceProx = E(tokens, indiceProx)