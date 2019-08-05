class MainNode:
    def __init__(self):
        self._type = 'MAIN'
        self.proc_func_list = []
        self.command_list = []
        self.syntax_table = []

    def addCommand(self, command):
        self.command_list.append(command)

class AttrNode:
    def __init__(self, var_name, expression):
        self._type = 'ATTR'
        self.var_name = var_name
        self.expression = expression

class IfNode:
    def __init__(self, expression):
        self._type = 'IF'
        self.expression = expression
        self.then_commands = []
        self.else_commands = []

    def addThenCommand(self, command):
        self.then_commands.append(command)

    def addElseCommand(self, command):
        self.else_commands.append(command)

class WhileNode:
    def __init__(self, expression):
        self._type = 'WHILE'
        self.expression = expression
        self.command_list = []

    def addCommand(self, command):
        self.command_list.append(command)

class ReadNode:
    def __init__(self):
        self._type = 'READ'
        self.var_list = []

    def addVar(self, var):
        self.var_list.append(var)

class WriteNode:
    def __init__(self):
        self._type = 'WRITE'
        self.expression_list = []

    def addExpression(self, expression):
        self.expression_list.append(expression)

class ProcedureNode:
    def __init__(self):
        self._type = 'PROCEDURE'
        self.proc_func_list = []
        self.parameter_list = []
        self.command_list = []
        self.symbol_table = []

    def addCommand(self, command):
        self.command_list.append(command)

    def addParameter(self, parameter):
        self.parameter_list.append(parameter)

class FunctionNode:
    def __init__(self):
        self._type = 'FUNCTION'
        self.proc_func_list = []
        self.parameter_list = []
        self.command_list = []
        self.symbol_table = []

    def addCommand(self, command):
        self.command_list.append(command)

    def addParameter(self, parameter):
        self.parameter_list.append(parameter)

class ProcCallNode:
    def __init__(self, proc_name):
        self._type = 'PROC_CALL'
        self.proc_name = proc_name
        self.expression_list = []

    def addExpression(self, expression):
        self.expression_list.append(expression)


