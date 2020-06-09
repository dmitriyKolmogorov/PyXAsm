class Register(object):
    '''
    This class representes register.

    You can create Register class instance by Register(name).
    Parameter 'name' has to be str and has to be in Register.names() 
    '''

    __names = ['ah', 'al', 'ax', 'eax', 'dh', 'dl', 'dx', 
               'edx', 'ch', 'cl', 'cx', 'ecx', 'bh', 'bl', 
               'bx', 'ebx', 'bp', 'ebp', 'si', 'esi', 'di', 
               'edi', 'sp', 'esp', 'mmx0', 'mmx1', 'mmx2', 
               'mmx3', 'mmx4', 'mmx5', 'mmx6', 'mmx7']


    def __init__(self, name:str) -> None:

        # if name is not available name for register
        if name in Register.__names:
            self.__name = name
        else:
            raise NameError(f'Register {name} is unknown. Use Register.names() to get all available names for registers.')


    def __str__(self) -> str:
        '''
        Returns name of register.
        '''
        return self.__name


    @classmethod
    def names(cls):
        '''
        Returns list with all available names for registers.
        '''
        return Register.__names


# define all registers
for reg in Register.names():
    exec(f'{reg} = Register("{reg}")')
