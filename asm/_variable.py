from copy import copy
from typing import Union
from ctypes import byref, POINTER as pointer

from _type import Type, Array
from _errors import ArgumentTypeError
from _typing import CArray, CValue, CArrayByRef, CValueByRef, CType, ArrayType

class Variable(object):

    def __init__(self, ctype:Union[Type, Array], value=None):

        # validate ctype argument
        if not (isinstance(ctype, Type) or isinstance(ctype, Array)):
            raise ArgumentTypeError(f'Unsuposed type of ctype argument (got {type(ctype)}, expected asm.Type or asm.Array).')

        # copy ArrayType to change its size
        if isinstance(ctype, Array):
            self.__ctype:Array = copy(ctype)
        else:
            self.__ctype:Type = ctype

        if value is not None:
            self.__value:Union[CValue, CArray] = self.__ctype._check_and_get_c_value(value)
            self.__has_value:bool = True
        else:
            self.__value:Union[CValue, CArray] = self.__ctype._get_default_value()
            self.__has_value:bool = False

        # name of variable is its id
        self.__name:str = 'a' + str(id(self))



    def __eq__(self, var:object) -> bool:
        '''
        Operator == is used in Function.compile().

        Returns True if name of two variables are equal.
        '''

        if not isinstance(var, Variable):
            raise ArgumentTypeError(f'Variable can be compared only with Variables, not with objects of type {type(var)}.')

        return self.__name == var.__name


    def _name(self) -> str:
        return self.__name


    def _get_type(self, is_pointer=False) -> Union[CType, ArrayType]:
        base_type:CType = self.__ctype._get_type()

        if is_pointer:
            return pointer(base_type)
        else:
            return base_type

    
    def __repr__(self) -> str:
        '''
        Returns representation of variable in Assembly insertion.

        Used in InstructionInstance.__call__().
        '''
        return f'%[{self.__name}]'


    def _definition(self, with_pointer:bool=False) -> str:
        '''
        Returns definition of variable as function argument by reference.  Used in Function.compile().

        For example, if var is defined as:
            var:Variable = Variable(c_int, 3)
        then this method will return:
            int * var
        '''
        return self.__ctype._get_variable_definition(self.__name, with_pointer=with_pointer)


    def has_value(self) -> bool:
        '''
        Returns True if current instance has value else False. Used in Function.compile()

        For example:
        >>> Variable(c_int, 3).has_value()
            True
        '''
        return self.__has_value


    def get_c_value(self, by_ref:bool=False) -> Union[CValue, CArray, CValueByRef, CArrayByRef]:
        '''
        Returns value builded using ctypes. Used in Function.compile().

        For example:
        >>> Variable(c_int, 5)
            c_int(5)
        '''

        return byref(self.__value) if by_ref else self.__value


    def _check_and_get_c_value(self, value:object) -> Union[CValue, CArray]:
        ''''
        Validates value for current instance and converts it to value builded using ctypes.
        '''
        return self.__ctype._check_and_get_c_value(value)