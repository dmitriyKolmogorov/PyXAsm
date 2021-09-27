from _register import Register
from _variable import Variable
from _base_intruction import Label

def is_number(x:object) -> bool:
    '''
    Returns True if its argument is of type int or float.
    '''

    return isinstance(x, int) or isinstance(x, float)


def is_register(x:object) -> bool:
    '''
    Returns True if its argument is of type Register.
    '''

    return isinstance(x, Register)


def is_variable(x:object) -> bool:
    '''
    Returns True if its argument is of type Variable.
    '''

    return isinstance(x, Variable)


def is_label(x:object) -> bool:
    '''
    Returns True if its argument if of type Label.
    '''

    return isinstance(x, Label)
