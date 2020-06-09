class Type(object):
    '''
    This class representes type for variables.
    
    Type class has next fields:
        | name - name of this type in CPP
        | to_str - name of CPP function, that converts object to string
        | from_str - name of CPP function, that converts string to CPP object
        | to_type - Python function (builtin or from asm.__convertations), that converts string to this type
        | check - Python function from asm.__checking, that controls user's input 
    '''

    def __init__(self, name:str, to_str:str, from_str:str, type_function, check_function):

        self.__name = name

        # to_str is name of CPP function, that converts object to string
        self.__to_str = to_str

        # from_str is name of CPP functions, that converts string to this type
        self.__from_str = from_str

        # type_function is function, that converts string to this type
        self.__type_function = type_function

        # check_function is function, that controls user's input
        self.__check_function = check_function


    def _to_type(self):
        return self.__type_function


    def _to_str(self) -> str:
        return self.__to_str


    def _from_str(self) -> str:
        return self.__from_str


    def _name(self) -> str:
        return self.__name

    
    def _check(self, value) -> None:
        '''Validates user\'s input for type of variable.'''
        return self.__check_function(value)