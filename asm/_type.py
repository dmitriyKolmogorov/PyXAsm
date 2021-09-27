from ctypes import (c_int,    
                    c_long,   
                    c_char,   
                    c_double, 
                    c_float,  
                    c_short,  
                    c_longlong,
                    c_uint,
                    c_ushort,
                    c_ulong,
                    c_ulonglong) 

from typing import Union, List, Tuple
from collections.abc import Iterable as IterableObject
import warnings

from _errors import ArgumentTypeError, ArgumentValueError
from _warns import TypeRangeWarning
from _typing import CArray, CType, CValue, ArrayType


class Type(object):
    '''
    This class representes C type.

    Methods defined here:
        __init__(typename:str)
            typename is name of C type.
            Availabel names for Type are short, int, long, double, float, long long, char,
                                         unsigned short, unsigned int, unsigned long, unsigned long long.

        ___check_value(value:object) -> None
            Checks is value is correct for given type.

        ___get_variable_definition(var_name:str, value:object=None, check_value:bool=True) -> str
            var_name is name of variable to be defined.
            value is value for variable.
            check_value is flag (method calls ___check_value(value) if value is not None and check_value is true).

            Returns string like '{_base_type_name} {var_name}'

    Fields defined here:
        _base_type_name:str - name of type of given class (like 'short', 'char' etc.).
        _ctype:object - type from ctypes (like c_short, c_char etc.)
    '''

    __types_dict:dict = {'short':              c_short,
                         'int':                c_int,
                         'long':               c_long,
                         'double':             c_double,
                         'float':              c_float,
                         'long long':          c_longlong,
                         'char':               c_char,
                         'unsigned short':     c_ushort,
                         'unsigned int':       c_uint,
                         'unsigned long':      c_ulong,
                         'unsigned long long': c_ulonglong}

    __int_rages = {'short':             (-32768, 32768),
                   'unsigned short':    (0, 65535),
                   'int':               (-2147483648, 2147483648),
                   'unsigned int':      (0, 4294967295),
                   'long':              (-2147483648, 2147483648),
                   'unsigned long':     (0, 4294967295),
                   'long long':         (-9223372036854775808, 9223372036854775808),
                   'unsigned long long':(0, 18446744073709551615)}


    def __init__(self, typename:str):

        if typename in Type.__types_dict:
            self._base_type_name:str = typename
            self._ctype:CType = Type.__types_dict[self._base_type_name]
        else:
            raise ArgumentValueError(f'Uknown name for C type: {name}.')


    def __str__(self) -> str:
        return f"Type(typename='{self._base_type_name}')"


    def _get_type(self) -> CType:
        return self._ctype


    def _get_default_value(self) -> CValue:
        '''
        Returns default value for given type.

        For example, default value of int type is equal to 0.
        '''

        return self._ctype()

    
    def _get_variable_definition(self, var_name:str, with_pointer:bool=False) -> str:
        '''
        Returns definition of variable as function argument by reference.  Used in Variable class.

        For example, if var is defined as:
            var:Variable = Variable(c_int, 3)
        then this method will return:
            int * var
        '''
        if with_pointer:
            return f'{self._base_type_name} * {var_name}' 
        else:
            return f'{self._base_type_name} {var_name}'


    def _check_value(self, value:object=None) -> None:
        '''
        Checks is value correct for given type. Used in Variable class.
        For whole types can raise warning, if value is not in range of given type.
        Can raise asm.ArgumentTypeError, if value is incorrect for given type.
        '''

        # try to convert value
        if value is not None:

            # check whole types
            if self._base_type_name in ('int', 
                                        'short', 
                                        'long', 
                                        'long long', 
                                        'unsigned short', 
                                        'unsigned int', 
                                        'unsigned long', 
                                        'unsigned long long'):

                # check type of python object
                if not isinstance(value, int):
                    raise ArgumentTypeError(f"Value is not of type '{self._base_type_name}' (unsuposed type {type(value)}, expected 'int').")  

                # check value range
                type_range:tuple = Type.__int_rages[self._base_type_name]

                if not (type_range[0] <= value and value <= type_range[1]):
                    warnings.warn(f"{value} is not in range of '{self._base_type_name}' ([{type_range[0]}, {type_range[1]}]).")

            # check float and double types
            elif self._base_type_name in ('float', 'double'):
                
                # check type
                if not (isinstance(value, float) or isinstance(value, int)):
                    raise ArgumentTypeError(f"Value is not of type '{self._base_type_name}' (unsuposed type {type(value)}, expected 'int' or 'float').")

            # check char type
            else:

                # check type
                if not isinstance(value, str):
                    raise ArgumentTypeError(f"Value is not of type '{self._base_type_name}' (unsuposed type {type(value)}, expected 'str').")

                # check len of Python string
                if len(value) != 1:
                    raise ArgumentTypeError(f"Can not convert Python string with lenght = {len(value)} to char (expected lenght = 1).")
        else:
            raise ArgumentTypeError(f'Can not convert object of type NoneType to {repr(self._base_type_name)}.')


    def _get_c_value(self, value:object) -> object:

        # WARNING! value is already validated in Type.get_variable_definition
        return self._ctype(value)


class Array(object):
    '''
    This class representes C array type.

    Methods defined here:
        __init__(ctype:object, size=None)
            ctype is instance of asm.Type or asm.Array.
            size is size of given instance (size should be a whole number and be greater than zero).

        ___check_value(value:object) -> None
            Checks is value is correct for array.

        ___get_variable_definition(var_name:str, value:object=None, check_value:bool=True) -> str
            var_name is name of variable to be defined.
            value is value for variable.
            check_value is flag (method calls ___check_value(value)) if value is not None and check_value is true).

            Returns string like '{_base_type_name} {var_name}'

    Fields defined here:
        _size:tuple - size of array. Includes whole numbers or None values.
        _base_type:object - type from ctypes (like c_short, c_char etc.).
        _base_type_name - name of type of array (like 'short', 'char' etc.)
    '''

    def __init__(self, ctype:Union[Type, ArrayType], size=None):

        # check type of ctype argument
        if isinstance(ctype, Type):
            self._base_type:Type = ctype
            self._base_type_name:str = ctype._base_type_name
        elif isinstance(ctype, Array):
            self._base_type:Type = ctype._base_type
            self._base_type_name:str = ctype._base_type_name
        else:
            raise ArgumentTypeError(f"Unsupposed type of first argument (got {type(ctype)}, expected Type from asm.types or Array).")

        if size is not None:
            # check type of size argument
            if not isinstance(size, int):
                raise ArgumentTypeError(f"Unsupposed type of size argument (got {type(size)}, expected 'int').")

            # check value of size argument if size in integer
            if size < 1:
                raise ArgumentValueError(f"Invalid value of size argument (got {size}, expected size > 0).")

        # build size field
        if isinstance(ctype, Type):
            self._size:tuple = (size, )
        elif isinstance(ctype, Array):
            self._size:tuple = (size, *ctype._size)

    
    def __str__(self) -> str:
        return f"Array(basetype='{self._base_type_name}', size={self._size})"


    def _get_variable_definition(self, var_name:str, with_pointer:bool=False) -> str:
        '''
        Returns definition of variable with its size as function argument by reference.  Used in Variable class.

        For example, if arr is defined as:
            arr_type:Array = Array(Array(c_int, 3), 4)
            var:Variable = Variable(arr_type)
        then this method will return:
            int * var[4][3]
        '''

        if with_pointer:
            definition:str = f'{self._base_type_name} {var_name}'
        else:
            definition:str = f'{self._base_type_name} * {var_name}'

        for dim in self._size:
            definition += f'[{dim}]'

        return definition


    def _get_type(self) -> ArrayType:
        # get ctype type for value
        c_type_arr:Ctype = self._base_type._ctype

        for dim in total_size[::-1]:
            c_type_arr:ArrayType = c_type_arr * dim

        return c_type_arr


    def _get_default_value(self) -> CArray:
        '''
        Returns array with default value for given type.

        For example, default value of arr_type, which is defined as:
            arr_type:Array = Array(Array(c_int, 2), 3)
        is equal to:
            {{0, 0}, {0, 0}, {0, 0}}
        '''

        # get ctype type for value
        c_type_arr:Ctype = self._base_type._ctype

        for dim in self._size[::-1]:

            # dim is of type int or NoneType
            if dim is None:
                raise ArgumentTypeError(f'One of dimensions in array is uknown, can not get default value of type {str(self)}.')

            c_type_arr:Ctype = c_type_arr * dim

        return c_type_arr()



    def _check_and_get_c_value(self, value:object) -> CArray:
        '''
        This method checks is value valid for variable's type and returns value of ctypes array. Uses in Variable class.

        Changes self._size for definition of variable. For example, if arr_type defined in the following way:
            arr_type:Array = Array(Array(c_int, None), 2)
        and var defined as:
            var:Variable = Variable(arr_type, [[1, 2, 3, 4], [5, 6, 7, 8]])
        then size of type of var will be (4, 2) and this variable will be defined as int var[2][4]
        '''

        # validate value
        total_size:List[int] = list(self._size)

        # here total_size is changing and after
        # calling this method it has not NoneType values
        self.__validate_array(value, self._size, total_size)

        # get ctype type for value
        c_type_arr:Ctype = self._base_type._ctype

        for dim in total_size[::-1]:
            c_type_arr:ArrayType = c_type_arr * dim

        def to_tuple_recursive(obj:Union[IterableObject, object]) -> tuple:
            '''
            This function converts each iterable object to tuple of tuples of tuples... recursively.

            Example:
            arr:list = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
            >>> to_tuple_recursive(arr)
                ((1, 2, 3), (1, 2, 3), (1, 2, 3))
            '''
            if isinstance(obj, IterableObject):
                return tuple(to_tuple_recursive(elem) for elem in obj)
            else:
                return obj

        # convert value to tuple
        value:tuple = to_tuple_recursive(value)

        # get c_value
        return c_type_arr(*value)


    
    def __validate_array(self, value:object, size:Tuple[int], total_size:List[int], total_size_index:int=0) -> None:
        '''
        This method recursively validates array and changes total_size, if some value in given size is equal to None.

        Example, for:
            arr_type:Array = Array(Array(Array(int, 2), None), 3)
        total_size for:
            arr:list = [[[1, 2], [1, 2], [1, 2]], [[3, 4], [3, 4], [3, 4]], [[5, 6], [5, 6], [5, 6]]]
        will look like:
        (3, 3, 2)
        '''
        
        if not isinstance(value, IterableObject):
            raise ArgumentTypeError(f'Can not convert {repr(value)} to array.')
        else:
            value:List[object] = list(value)

        if self._size[0] is not None:
            if len(value) != size[0]:
                raise ArgumentTypeError(f'Can not convert {repr(value)} to {self._base_type_name} array (got lenght {len(value)}, expected {size[0]}).')

        # check 1d array
        if len(size) == 1:
            if size[0] is not None:
                if len(value) != size[0]:
                    raise ArgumentTypeError(f'Can not convert {repr(value)} to {self._base_type_name} array (got lenght {len(value)}, expected {size[0]}).')
            else:
                if len(value) != 0:
                    total_size[total_size_index]:int = len(value)
                else:
                    raise ArgumentTypeError(f'Can not convert empty list to {self._base_type_name}.')
                
            for final_element in value:
                self._base_type._check_value(final_element)

        # check n-dimensional array
        else:
            for i in range(len(value)):

                element:object = value[i]
                    
                if i == 0:
                    cur_lenght:int = len(element)
                    total_size[total_size_index]:int = len(value)
                else:
                    if len(element) != cur_lenght:
                        raise ArgumentTypeError(f'Can not convert {repr(element)} to {self._base_type_name} array (got lenght {len(element)}, expected {cur_lenght}).')
            
                self.__validate_array(element, size[1:], total_size, total_size_index + 1)

        # modify size of array
        self._size:tuple = tuple(total_size)