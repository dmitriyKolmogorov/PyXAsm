from abc import ABC
from copy import copy
from typing import Iterable, Union
from collections.abc import Iterable as IterableObject

from _variable import Variable
from _errors import ArgumentTypeError, \
                    ArgumentsNumberError
from _typing import function


class InstructionInstance(object):
    '''
    This class represented instruction with parameters like mov(eax, 4) or jmp label.

    __init__(self, name:str, args:tuple)
        Initialization in BaseInstruction.__call__().

    __args(self) -> tuple
        Returns tuple with its arguments.
    '''
    def __init__(self, name:str, args:Union[tuple, None]=None):
        
        self.__name:str = name

        if args is not None:
            self.__args:tuple = args
        else:
            self.__args:tuple = tuple()


    def _args(self) -> tuple:
        '''
        Returns instruction's arguments.
        '''
        return self.__args


    def _variables(self) -> tuple:
        '''
        Returns args that are instances of Variable class
        '''
        return (arg for arg in self.__args if isinstance(arg, Variable))


    def _labels(self) -> tuple:
        '''
        Returns args that are instances of Label class
        '''
        return (arg for arg in self.__args if isinstance(arg, Label))


    def _source(self) -> str:
        '''
        Returns string representation of instruction.

        Example:
            mov(eax, 2) -> "mov eax, 2;"
            jmp(label) ->  "jmp label;"
            cpuid() -> "cpuid;"

        Uses self._label_source().
        '''
        
        return '"' + self._label_source() + '"'


    def _label_source(self) -> str:
        '''
        Returns simplified string representation of instruction.

        Example:
            mov(eax, 2) -> mov eax, 2;
            jmp(label) -> jmp label;
            cpuid() -> cpuid;
        '''

        # len of self.__args is equal to 0, 1 or 2.
        if len(self.__args) == 0:
            return f'{self.__name};'
        elif len(self.__args) == 1:
            return f'{self.__name} {repr(self.__args[0])};'
        else:
            return f'{self.__name} {repr(self.__args[0])}, {repr(self.__args[1])};'


    def __str__(self) -> str:
        '''
        Returns description of instruction.
        '''

        # len of self.__args is equal to 0, 1 or 2.
        if len(self.__args) == 0:
            return f'InstructionInstance(name=\'{self.__name}\', arg1=None, arg2=None)'
        elif len(self.__args) == 1:
            return f'InstructionInstance(name=\'{self.__name}\', arg1={repr(self.__args[0])}, arg2=None)'
        else:
            return f'InstructionInstance(name=\'{self.__name}\', arg1={repr(self.__args[0])}, arg2={repr(self.__args[1])})'


# BaseInstruction class is an abstract class
class BaseInstruction(ABC):
    '''
    This class representes base class for instruction.
    
    __init__(self, name:str, validate_funcs=None):
        name - name of instruction. For example, to define mov instruction use mov = BaseInstruction('mov');
        validate_funcs (default:None) - bool functions to validate arguments from asm._validate_functions:
            for instruction with two arguments looks like [(arg1_func1, arg1_func2, ...), (arg2_func1, arg2_func2, ...)];
            for instruction with one argument looks like [arg_func1, arg_func2, ...];

    __call__(self, *args):
        args - arguments for instruction:
            for instruction with two arguments len(args) = 2;
            for instruction with one argument len(args) = 1;
            for instruction with no arguments len(args) = 0;

        Calls self.__validate(self).

    __validate(self, *args):
        Validates arguments using self.__validate_funcs.
        Algorithm for instruction with two arguments looks like:

            arg1_validated = arg2_validated = False;

            for (function in self.__validate_funcs[0])
                arg1_validated = arg1_validated | function(arg1)

            for (function in self.__validate_funcs[1])
                arg2_validated = arg2_validated  | function(arg2)

        Algorithm for instruction with one argument looks like:
            arg_validated = False

            for (function in self.__validate_funcs)
                arg_validated = arg2_validated | function(arg)
    '''
    def __init__(self, name:str, validate_funcs:Union[Iterable[function], None]=None):
        
        # this is no validation for validate_funcs since this class is private
        self._name:str = name

        if validate_funcs is not None:
            self._validate_funcs:List[function] = list(validate_funcs)
        else:
            self._validate_funcs:List[function] = list()


    def __call__(self, *args) -> InstructionInstance:
        self.__validate(args)

        return InstructionInstance(self._name, args)


    def __validate(self, args:tuple) -> None:
        pass


class InstructionWithTwoArguments(BaseInstruction):
    '''
    This class representes instruction with two arguments like mov or add.
    
    __init__(self, name:str, validate_funcs=None):
        name - name of instruction. For example, to define mov instruction use mov = InstructionWithTwoArguments('mov');
        validate_funcs (default:None) - bool functions to validate arguments from asm._validate_functions:
            looks like [(arg1_func1, arg1_func2, ...), (arg2_func1, arg2_func2, ...)];

    __call__(self, *args):
        args - arguments for instruction:
            for instruction with two arguments len(args) = 2;
            for instruction with one argument len(args) = 1;
            for instruction with no arguments len(args) = 0;

        Calls self.__validate(self).

    __validate(self, *args):
        Validates arguments using self.__validate_funcs.
        Algorithm looks like:

            arg1_validated = arg2_validated = False;

            for (function in self.__validate_funcs[0])
                arg1_validated = arg1_validated | function(arg1)

            for (function in self.__validate_funcs[1])
                arg2_validated = arg2_validated  | function(arg2)
    '''

    __num_of_args:int = 2


    def __init__(self, name:str, validate_funcs:Union[Iterable[function], None]=None):
        super().__init__(name, validate_funcs)

    
    def __repr__(self) ->str:
        return f'InstructionWithTwoArguments(name=\'{self._name}\')'


    def __validate(self, args:tuple) -> None:

        # validate num of arguments
        if len(args) != InstructionWithTwoArguments.__num_of_args:
            raise ArgumentsNumberError(f'{self._name}: invalid number of arguments (got {len(args)}, expected 2).')

        # self.__validate_funcs always has correct type - list<(tuple<function>, tuple<function>)>
        arg1_validated:bool = False
        arg2_validated:bool = False

        # validate first argument
        for val_func in self._validate_funcs[0]:
            arg1_validated |= val_func(args[0])

        # validate second argument
        for val_func in self._validate_funcs[1]:
            arg2_validated |= val_func(args[1])

        # error in first argument
        if not arg1_validated:
            raise ArgumentTypeError(f'{self._name}: unsupported type argument with index 0.')

        # error in second argument
        if not arg2_validated:
            raise ArgumentTypeError(f'{self._name}: unsuported type argument with index 1.')


class InstructionWithOneArgument(BaseInstruction):
    '''
    This class representes base class for instruction.
    
    __init__(self, name:str, validate_funcs=None):
        name - name of instruction. For example, to define mov instruction use mov = BaseInstruction('mov');
        validate_funcs (default:None) - bool functions to validate arguments from asm._validate_functions:
            looks like [arg_func1, arg_func2, ...];

    __call__(self, *args) -> InstructionInstance:
        args - arguments for instruction:
            for instruction with two arguments len(args) = 2;
            for instruction with one argument len(args) = 1;
            for instruction with no arguments len(args) = 0;

        Calls self.__validate(self).

    __validate(self, *args) -> None:
        Validates arguments using self.__validate_funcs.

        Algorithm for instruction looks like:
            arg_validated = False

            for (function in self.__validate_funcs)
                arg_validated = arg2_validated | function(arg)

            return arg_validated
    '''


    __num_of_args = 1


    def __init__(self, name:str, validate_funcs:Union[Iterable[function], None]=None):
        super().__init__(name, validate_funcs)


    def __repr__(self) -> str:
        return f'InstructionWithOneArgument(name=\'{self._name}\')'


    def __validate(self, args:tuple) -> None:

        # validate num of arguments
        if len(args) != InstructionWithOneArgument.__num_of_args:
            raise ArgumentsNumberError(f'{self._name}: invalid number of argument (got {len(args)}, expected 1)')

        # self.__validate_funcs always has correct type - list<(tuple<function>, tuple<function>)>
        arg_validated:bool = False

        # validate argument
        for val_func in self._validate_funcs:
            arg_validated |= val_func(args[0])

        # error in arg
        if not arg_validated:
            raise ArgumentTypeError(f'{self._name}: unsupported type argument.')


class InstructionWithoutParameters(BaseInstruction):
    '''
    This class representes base class for instruction.
    
    __init__(self, name:str, validate_funcs=None):
        name - name of instruction. For example, to define mov instruction use mov = BaseInstruction('mov');
        validate_funcs (None)

    __call__(self, *args):
        args - arguments for instruction:
            for instruction with no arguments len(args) = 0;

        Calls self.__validate(self).

    __validate(self, *args):
        Checks true number of parameters.
    '''


    __num_of_args = 0


    def __init__(self, name:str, validate_funcs:Union[Iterable[function], None]=None):
        super().__init__(name, validate_funcs)


    def __repr__(self) -> str:
        return f'InstructionWithoutParameters(name=\'{self._name}\')'


    def __validate(self, args:tuple) -> None:

        if len(args) != InstructionWithoutParameters:
            raise ArgumentsNumberError(f'{self._name}: invalid number of arguments (got {len(args)}, expected 0).')


class Label(object):
    def __init__(self, instructions:Iterable[InstructionInstance]):

        # get unique name for label
        # for example: l124324234
        self.__name = 'label' + str(id(self))

        # try convert instructions argument to list
        if not isinstance(instructions, IterableObject):
            raise ArgumentTypeError('Initialization argument should be iterable.')

        # convert instructions argument to list
        instructions:list = list(instructions)

        # instructions argument is empty
        if len(instructions) == 0:
            raise ArgumentValueError('Initialization argument should be non-empty iterator.')

        # validate elements in instructions argument
        for i in range(len(instructions)):
            if not isinstance(instructions[i], InstructionInstance):
                raise ArgumentTypeError(f'Object with index {i} in initialization argument is not of type InstructionInstance.')

        self.__instructions:list = instructions
        self.__labels:tuple = (label for instruction in instructions for label in instruction._labels())


    def __eq__(self, var) -> bool:

        if not isinstance(var, Label):
            raise ArgumentTypeError(f'Label can be comparated only with Labels, not with objects of type {type(var)}.')

        return self.__name == var.__name


    def __repr__(self) -> str:
        return self.__name


    def __str__(self) -> str:
        output:str = 'Label(' + repr(self.__instructions[0]) + '\n'

        # indent is equal to 6 since string 'Label(' has 6 characters
        indent:int = 6

        for i in range(1, len(self.__instructions)):
            output += ' ' * indent + repr(self.__instructions[i]) + '\n'

        return output + ')'


    def _variables(self) -> tuple:
        return (var for instruction in self.__instructions  \
                    for var in instruction._variables())


    def _labels(self) -> tuple:
        return (var for instruction in self.__instructions  \
                    for var in instruction._labels())


    def _source(self) -> str:
        return  f'"{self.__name}:'  + \
                " ".join(instruction._label_source() for instruction in self.__instructions) + \
                '"'