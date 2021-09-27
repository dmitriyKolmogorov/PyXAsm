import os
from subprocess import run as run_command, PIPE
from copy import copy
from typing import Iterable, List, Union
from collections.abc import Iterable as IterableObject
from ctypes import cdll

from _errors import (ArgumentTypeError, 
                     FunctionIsNotCompiledError, 
                     ArgumentValueError, 
                     VariableDoesNotExistError,
                     CompilationError)

from _base_intruction import InstructionInstance, Label
from _variable import Variable
from _typing import SystemProcess, function, SharedLibrary, CType


# TODO: write documentation for methods and class
class Function(object):
    def __init__(self, instructions:List[InstructionInstance]):

        if not isinstance(instructions, IterableObject):
            raise ArgumentTypeError('Can not iter object with instructions.')
        else:
            instructions:List[InstructionInstance] = list(instructions)

        for i in range(len(instructions)):
            if not isinstance(instructions[i], InstructionInstance):
                raise ArgumentTypeError(f'Object with index {i} in list of instructions is not of type Instruction from asm.instructions.')

        self.__instructions:List[InstructionInstance] = instructions
        self.__is_compiled:bool = False


    # TODO: finish function call
    def __call__(self, *args) -> tuple:

        if not self.__is_compiled:
            raise FunctionIsNotCompiledError('Can not call this function since it was not compiled with Function.compile().')


    # TODO: finish full compiling
    def compile(self, input_vars:Union[Iterable[Variable], None]=None, 
                      local_vars:Union[Iterable[Variable], None]=None, 
                      output_vars:Union[Iterable[Variable], None]=None,
                      delete_source:bool=True):

        # convert input_vars argument to list of variables
        if input_vars is None:
            input_vars:List[Variable] = list()
        else:
            if not isinstance(input_vars, IterableObject):
                raise ArgumentTypeError('Can not iter input_vars argument.')
            else:
                input_vars:List[Variable] = list(input_vars)

        # convert local_vars argument to list of variables
        if local_vars is None:
            local_vars:List[Variable] = list()
        else:
            if not isinstance(local_vars, IterableObject):
                raise ArgumentTypeError('Can not iter local_vars argument.')
            else:
                local_vars:List[Variable] = list(local_vars)

        # convert output_vars argument to list of variables
        if output_vars is None:
            output_vars:List[Variable] = list()
        else:
            if not isinstance(output_vars, IterableObject):
                raise ArgumentTypeError('Can not iter output_vars argument.')

            output_vars:List[InstructionInstance] = list(output_vars)

        # roles is list of lists with values:
        #    'i' - matches that corresponding variable is input
        #    'o' - matches that corresponding variable is output
        # if list in roles is empty, it means that corresponding variable is local 
        roles:List[List[str]] = list()

        # all_variables is list of variables in assembly insertions
        all_variables:List[Variable] = list()

        for i in range(len(output_vars)):
            current_var:Variable = output_vars[i]

            # objects in output_vars should be of type Variable
            if not isinstance(output_vars[i], Variable):
                raise ArgumentTypeError(f'Object in output_vars with index {i} is not of type Variable.')

            # check for dublicates
            if current_var in all_variables:
                raise ArgumentValueError('Variable in output_vars with index {i} is already in output_vars.')
            else:
                # add variable to list of all variables and define its role as output (['o'])
                all_variables.append(current_var)
                roles.append(['o'])

        for i in range(len(input_vars)):
            current_var:Variable = input_vars[i]

            # objects in input_vars should be of type Variable
            if not isinstance(input_vars[i], Variable):
                raise ArgumentTypeError(f'Object in input_vars with index {i} is not of type Variable.')

            # check for dublicates:
            if input_vars.count(current_var) != 1:
                raise ArgumentValueError('Variable in input_vars with index {i} is already in input_vars.')

            # add role for variable or add variable and its 'input' role (['i'])
            if current_var in all_variables:
                roles[all_variables.index(current_var)].append('i')
            else:
                all_variables.append(current_var)
                roles.append(['i'])

        for i in range(len(local_vars)):
            current_var:Variable = local_vars[i]

            # object in local_vars should be of type Variable
            if not isinstance(current_var, Variable):
                raise ArgumentTypeError(f'Object in local_vars with index {i} is not of type Variable.')

            # check for dublicates
            if current_var in all_variables:
                raise ArgumentValueError(f'Variable in local_vars with index {i} is already in input, local or output variables.')
            else:
                # add variable and its 'local' role (empty list)
                all_variables.append(current_var)
                roles.append([])

        # check have input variables default value
        for i in range(len(input_vars)):
            if input_vars[i].has_value():
                raise ArgumentValueError(f'Input variable with index {i} has default value (input variable can not have value).')

        # list with labels from instructions
        labels:List[Label] = list()

        for i in range(len(self.__instructions)):
            instruction:InstructionInstance = self.__instructions[i]

            # check are instructions' variables in all_variables
            for instruction_var in instruction._variables():
                if instruction_var not in all_variables:
                    raise VariableDoesNotExistError(f'Instruction with index {i} has variable which is not input, local or output variable.')

            # check are all variables from labels in all_variables
            for label in instruction._labels():
                for label_var in label._variables():
                    if label_var not in all_variables:
                        raise ArgumentTypeError(f'Instruction with index {i} has label, which has instruction which is not input, local or output variable.')

                # build list of labels
                if label not in labels:
                    labels.append(label)

        # get source of function in C language
        source:str = self.__build_func_source(all_variables, 
                                              roles, 
                                              labels)

        # get number of input arguments
        self.__input_arguments_num:int = len(input_vars)

        # define filenames for source file and shared library
        source_filename:str = 'pyxasm_source_file.c'
        shared_lib_filename:str = 'pyxasm_shared_library.so'

        # compile source file to shared library
        self.__compile_source(source, 
                       source_filename, 
                       shared_lib_filename, 
                       delete_source=delete_source)

        # load function from shared library
        self.__main:function = self.__load_and_delete_lib(shared_lib_filename).main_function

        # preprocess function
        self.__main.argtypes:List[CType] = tuple(all_variables[i]._get_type(is_pointer=('o' in roles[i])) \
                                                 for i in range(len(all_variables)))

        self.__main.restype:Union[Ctype, None] = None


    def __build_func_source(self, all_variables:List[Variable], 
                                  roles:List[List[str]], 
                                  asm_labels:List[Label]) -> str:

        # build signature of function like void main(int a1, short a2)
        # remark: len of roles is equal to len of all_variables
        # for output variable .definition returns string like 'type * var_name'
        # for input and local variables .definition returns string like 'type var_name'
        source:str = 'void main_function(' + \
                     ', '.join([all_variables[i]._definition(with_pointer=('o' in roles[i])) \
                                for i in range(len(all_variables))]) + \
                     '){\n'

        # add assembly insertion to source
        source += self.__build_asm_source(all_variables, roles, asm_labels)

        # end building, function is ready
        source += '}'

        return source


    def __build_asm_source(self, all_variables:List[Variable], 
                                 roles:List[List[str]],
                                 labels:List[Label]) -> str:
        
        source:str = '__asm__(\n'

        # add source of instructions 
        for instruction in self.__instructions:
            source += instruction._source() + '\n'

        # add source of labels used in function
        for label in labels:
            source += label._source() + '\n'

        # jump to definition of variables
        # this line adds : because :"=r"(var) means output variable
        # to simplify building all variables in inline assembly are output
        source += ':'

        # add variables
        # alternative of this code snippet is
        # source += ','.join([f'[{all_variables[i]._name()}]"=r"('*' * ('o' in roles[i]) + {all_variables[i]._name()}) \
        #                     for i in range(len(all_variables))])
        source += ','.join([f'[{all_variables[i]._name()}]"=r"({all_variables[i]._name()})'  \
                            if 'o' not in roles[i]                                           \
                            else                                                             \
                            f'[{all_variables[i]._name()}]"=r"(*{all_variables[i]._name()})' \
                            for i in range(len(all_variables))])

        # finish assembly insertion
        source += '\n);'

        return source


    def __compile_source(self, source:str, 
                               source_filename:str, 
                               shared_lib_filename:str, 
                               delete_source:bool=True) -> None:

        # create .c file with source builded in __build_function_source()
        with open(source_filename, 'w') as c_file:
            c_file.write(source)

        # compile .c file to shared library (file with .so extension)
        command:List[str] = ['gcc', 
                             '-fPIC', 
                             '-shared', 
                             '-m32', 
                             '-masm=intel', 
                             '-o', 
                             shared_lib_filename, 
                             source_filename]

        result:SystemProcess = run_command(command, 
                                           stdout=PIPE, 
                                           cwd=os.getcwd(), 
                                           text=True,
                                           shell=True)

        # handle error while compiling
        # if returncode is equal to 0, file was compiled
        if result.returncode != 0:
            raise CompilationError(f'Compilation with gcc was unsuccessful. Error code: {result.returncode}. See details above.')

        # delete source file
        if delete_source:
            if os.path.exists(source_filename):
                os.remove(source_filename)

        
    def __load_and_delete_lib(self, shared_lib_filename:str) -> SharedLibrary:
        
        # load library with 1 function and get this function by main_function attribute
        lib:SharedLibrary = cdll.LoadLibrary(os.path.abspath(shared_lib_filename))

        # delete shared library
        #if os.path.exists(shared_lib_filename):
            #os.remove(shared_lib_filename)

        return lib

        
        
