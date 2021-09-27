from _errors import ArgumentValueError

# TODO: update bool methods
class Register(object):
    '''
    This class representes register in Assembly.

    __init__(self, name:str):
        name:str - name of register.

    is_segment(self) -> bool:
        returns True if current register is segment register.

    is_mmx(self) -> bool:
        returns True if current register is mmx register.
    '''
    
    __available_names:list = ['eax', 'ebx', 'edx', 'ecx',
                              'ebp', 'esp', 'esi', 'edi',
                              'ax', 'bx', 'dx', 'cx',
                              'ah', 'bh', 'dh', 'ch',
                              'al', 'al', 'dl', 'cl'
                              'esi', 'si', 'edi', 'di',
                              'esp', 'sp', 'ebp', 'bp'
                              'cs', 'ss', 'ds', 'fs', 'gs', 'es'
                              'mmx0', 'mmx1', 'mmx2', 'mmx3',
                              'mmx4', 'mmx5', 'mmx6', 'mmx7']


    def __init__(self, name:str):
        
        if name not in Register.__available_names:
            raise ArgumentValueError('Uknown name for register. Use Register.available_names() to get list of available names.')
        
        self.__name:str = name

    
    def __repr__(self) -> str:
        return self.__name


    def __str__(self) -> str:
        return f'Register(name=\'{self.__name}\')'


    def name(self) -> str:
        return self.__name


    def is_segment(self) -> bool:
        return self.__name.endswith('s')


    def is_mmx(self) -> bool:
        return self.__name.startswith('mmx')


    def is_accumulator(self) -> bool:
        return 'a' in self.__name


    def is_base(self) -> bool:
        return 'b' in self.__name


    def is_counter(self) -> bool:
        if self.__name != 'cs':
            return 'c' in self.__name

        return False


    def is_data(self) -> bool:
        return 'd' in self.__name


    def is_source_index(self) -> bool:
        return self.__name == 'esi' or self.__name == 'si'

    
    def is_destination_index(self) -> bool:
        return self.__name == 'edi' or self.__name == 'di'

    
    def is_stack_pointer(self) -> bool:
        return self.__name == 'esp' or self.__name == 'sp'

    
    def is_base_pointer(self) -> bool:
        return self.__name == 'ebp' or self__name == 'bp'

    
    @classmethod
    def available_names(cls):
        return Register.__available_names