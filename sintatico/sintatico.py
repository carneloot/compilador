def logFunc(function):
    def wrapper(self):
        print(f'Enter <{function.__name__}>')

        resultado = function(self)

        print(f'Exit <{function.__name__}>')

        return resultado

    return wrapper

class AnalisadorDescendente():

    def __init__(self, tokens):
        self.tokens = tokens
        self.currentToken = 0

    def lerTerminal(self, terminal):
        if self.tokens[self.currentToken][0] == terminal:
            self.currentToken += 1
            print(f'Li "{terminal}"')
            return True
        return False

    def run(self):
        self.program()

    # Funcoes de nao terminais

    @logFunc
    def program(self):

        if self.lerTerminal('program'):
            self.identificador()

            self.lerTerminal(';')

            self.bloco()

    @logFunc
    def identificador(self):
        pass

    @logFunc
    def bloco(self):
        pass


