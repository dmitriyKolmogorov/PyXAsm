class ArgumentsNumberError(Exception):
    def __init__(self, text:str):
        super().__init__(self, text)


class ArgumentTypeError(Exception):
    def __init__(self, text:str):
        Exception.__init__(self, text)


class ArgumentValueError(Exception):
    def __init__(self, text:str):
        Exception.__init__(self, text)


class FunctionIsNotCompiledError(Exception):
    def __init__(self, text:str):
        Exception.__init__(self, text)

    
class VariableDoesNotExistError(Exception):
    def __init__(self, text:str):
        Exception.__init__(self, text)


class CompilationError(Exception):
    def __init__(self, text:str):
        Exception.__init__(self, text)