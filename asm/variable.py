from asm.__type import Type
from asm.__checking import *
from asm.__convertations import *

# TODO: add types of char, char[], char[][] and 2d numeral arrays.

class Variable(object):
    '''
    This class representes variable.
    '''

    # available types
    __types = {'int':                   Type('int', 'num_to_str', 'str_to_num', int, check_int),
               'short int':             Type('short int', 'num_to_str', 'str_to_num', int, check_int),
               'unsigned short int':    Type('unsigned short int', 'str_to_num', 'str_to_un_short', int, check_int),
               'unsigned int':          Type('unsigned int', 'num_to_str', 'str_to_num', int, check_int),
               'long int':              Type('long int', 'num_to_str', 'str_to_num', int, check_int),
               'unsigned long int':     Type('unsigned long int', 'num_to_str', 'str_to_num', int, check_int),
               'long long int':         Type('long long int', 'num_to_str', 'str_to_num', int, check_int),
               'unsigned long long int':Type('unsigned long long int', 'num_to_str', 'str_to_num', int, check_int),
 
               # int array types
               'int[]':                     Type('int []', 'num_arr_to_str', 'str_to_int_arr', arr, check_int_arr),
               'short int[]':               Type('short int []', 'num_arr_to_str', 'str_to_short_int_arr', arr, check_int_arr),
               'unsiged short int[]':       Type('unsidned short int []', 'num_arr_to_str', 'str_to_un_short_int_arr', arr, check_int_arr),
               'unsigned int[]':            Type('unsigned int []', 'num_arr_to_str', 'str_to_un_int_arr', arr, check_int_arr),
               'long int[]':                Type('long int []', 'num_arr_to_str', 'str_to_long_int_arr', arr, check_int_arr),
               'unsigned long int[]':       Type('unsigned long int []', 'num_arr_to_str', 'str_to_us_long_int_arr', arr, check_int_arr),
               'long long int[]':           Type('long long int []', 'num_arr_to_str', 'str_to_long_long_int_arr', arr, check_int_arr),
               'unsigned long long int[]':  Type('unsigned long long int []', 'num_arr_to_str', 'str_to_un_long_long_int_arr', arr, check_int_arr),
  
               # float and double types
               'float':      Type('float', 'num_to_str', 'str_to_float', float, check_float),
               'double':     Type('double', 'num_to_str', 'str_to_double', float, check_float),
               'float[]':    Type('float []', 'num_arr_to_str', 'str_to_float_arr', arr, check_float_arr),
               'double[]':   Type('double []', 'num_arr_to_str', 'str_to_double_arr', arr, check_float_arr),
              }  


    def __init__(self, dtype:str, value=None):

        # check dtype argument
        if not isinstance(dtype, str):
            raise TypeError('Argument dtype is not str.')

        # unknown dtype
        if not dtype in Variable.__types:
            raise ValueError(f'Unknown type {dtype}. To get all available types, use Variable.available_types().')

        self.__type = Variable.__types[dtype]

        # check user's input for variable
        if value is not None:
            # this function raises exceptions, if value is wrong for dtype
            value = self.__type._check(value)

        self.__value = value

        # indexing with assembly like %i
        self.__index = None

    
    def __str__(self) -> str:
        '''
        String representation of variable for assembly insertion.
        '''
        if self.__index is not None:
            return f'%{self.__index}'
        else:
            ValueError('This variable has not index for assembly insertion.')

    
    def __repr__(self) -> str:
        return self.__str__()


    def _to_str(self) -> str:
        '''
        Returns string representation of defining variable in CPP.
        '''

        # copy dtype name to other variable
        type_name = self.__type._name()

        # TODO: rename string_representation variable

        # building defining of variable
        # if variable is array
        if type_name.endswith('[]'):

            # if variable is 2d array:
            if type_name.endswith('[][]'): 
                string_representation = f'{type_name[:-4]} a{self.__index}[N][N]'
            else:
                string_representation = f'{type_name[:-2]} a{self.__index}[N]'
        # if variable is not array
        else:
            string_representation = f'{type_name} a{self.__index}'

        # add value to string representation
        if self.has_value():
            # if variable is array
            if type_name.endswith('[]'):

                # if variable is 2d array:
                if type_name.endswith('[][]'):
                    value_string = '{ '

                    for set_ in self.__value[:-1]:
                        value_string += '{' + str(set_)[1:-1] + '}, '

                    value_string += '{' + str(self.__value[-1])[1:-1] + '} }\n'

                    # defining size of arr
                    value_string += f'int n1_a{self.__index} = {len(self.__value)};\n'
                    value_string += f'int n1_a{self.__index} = {len(self.__value[0])};\n'
                else:
                    # convert string representation of array from Python style to Cpp style
                    # Example: [1, 2, 3] -> {1, 2, 3}
                    value_string = '{' + str(self.__value)[1:-1] + '};\n'
                    value_string += f'int n_a{self.__index} = {len(self.__value)};\n'
            # if variable is not array
            else:

                # add ' for variable with char type
                if type_name == 'char':
                    value_string = "'" + str(self.__value) + "'"
                else:
                    value_string = str(self.__value) + ';\n'

            # add value's representation to string representation of variable
            string_representation += ' = ' + value_string
        else:
            string_representation += ';\n'

        return string_representation


    def _to_str_input(self) -> str:
        '''
        This method builds string representation of reading input variable from buffer file.
        '''

        # str variable for building command
        # TODO: change name of this variable
        reading_str = f'getline(buffer, line);\n'

        # if variable is array
        if self.__type._name().endswith('[]'):
            
            # if variable is 2d array
            if self.__type._name().endswith('[][]'):
                # string like 'int n1_a1; int n2_a1; int ** a1 = str_to_num_2d_arr<int>(a1, n1_a1, n2_a2);'
                reading_str += 'int n1_a' + self._name() + '; int n2_a' + self._name() + ';\n'
                reading_str += self.__type._name()[:-4] + ' ** a' + self._name()
                reading_str += ' = ' + self.__type._from_str() + '<' + self.__type._name()[::-4] + '>(line, n1_a' + self._name() + 'n2_a' + self._name() + ');\n' 
            # if variable is 1d array
            else:
                reading_str += 'int n_a' + self._name() + ';\n'
                reading_str += ' = ' + self.__type._from_str() + '<' + self.__type._name()[::-4] + '>(line, n1_a' + self._name() + ');\n'  
        # if variable is not array
        else:
            reading_str += self.__type._name() + ' ' + self._name() + ' = ' + self.__type._from_str() + '<' + self.__type._name() + '>(line);\n'

        return reading_str


    def _to_str_output(self):
        '''
        This method builds string representation of writing output variable to .txt file
        '''

        var_name = f'a{(self.__index)}'

        # variable is array
        if self.__type._name().endswith('[]'):
            # variable is 2d array
            if self.__type._name().endswith('[][]'):
                # string like num_arr_2d_to_str(a1, n1_a1, n2_a1);
                return f'{self.__type._to_str()}({var_name}, n1_{var_name}, n2_{var_name})'
            # variable is 1d array
            else:
                # string like num_arr_to_str(a1, n_a1);
                return f'{self.__type._to_str()}({var_name}, n_{var_name})'

        # string like num_to_arr(a1);
        return f'{self.__type._to_str()}({var_name})'

    
    def _from_str_func(self):
        '''
        Returns name of CPP function for converting string to CPP object.
        '''
        return self.__type._from_str()

    
    def _to_str_func(self):
        '''
        Returns name of CPP function for converting CPP object to its string representation.
        '''
        return self.__type._to_str()

    
    def _to_type(self):
        '''
        Returns function for converting string to Python object.
        '''
        return self.__type._to_type()


    def has_value(self) -> bool:
        '''
        This method returns True if this variable has value and False if this variable has not value.
        '''
        return self.__value is not None

    
    def _set_index(self, index:int) -> None:
        '''
        Sets index for variable in assembly insertion like %1.
        '''

        if index < 0:
            raise ValueError('')

        self.__index = index


    def _name(self) -> str:
        '''
        Returns string like 'a1' with variable's index for assembly insertion.
        '''
        return f'a{self.__index}' 

    
    @classmethod
    def available_types(cls) -> list:
        '''
        Returns list with all available types for variable.
        '''
        return list(Variable.__types.keys())