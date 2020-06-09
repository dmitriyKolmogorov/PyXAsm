import os

from asm.variables import Variable

class Function(object):
    '''
    The main class of package. This class creates .exe file from commands from asm.instructions and runs it.
    You need to have gcc.exe in PATH.
    '''

    def __init__(self, commands):

        self.__commands = commands

        # bool variable. we can not use Function.__call__() if this variable is False
        self.__is_compiled = False

    
    def __call__(self, *args):
        '''
        Magic __call__() method. Writes its arguments to buffer .txt, runs .exe file and reads result from buffer file.

        Returns tuple with values of output variables.

        !WARNING The order of arguments is important. If you compiled model like input_vars=[a, b], you must first indicate value of a and then value of b.
        '''

        # function is not compiled with Function.compile()
        if not self.__is_compiled:
            raise NotImplementedError('This function is not compiled. Use Function.compile() to fix it.')

        if len(args) != len(self.__input_vars):
            raise IndexError('Length of args is not equal to length of input variables.')

        # write input to buffer file
        with open(self.__buffer_file_name + '.txt', 'w') as f:
            for arg in args:
                f.write(str(arg) + '\n')

        # run .exe file
        os.system(f'{self.__buffer_file_name + ".exe"}')

        try:
            # reading result
            with open(self.__buffer_file_name + '.txt', 'r') as f:
                
                # reading result and converting to Python objects
                result = tuple(var._to_type()(string) for var, string in zip(self.__output_vars, f.read().split('\n')))
        finally:
            # delete buffer file
            os.remove(self.__buffer_file_name + '.txt')

        if len(result) == 0:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            return result

        
    def __build_asm(self) -> str:
        '''
        This method builds source for assembler-commands.
        commands has to be iterable object, which has functions from asm.instuctions
        Returns str type.
        '''

        # inline assembly
        source = '__asm(\n'

        # building source
        for command in self.__commands:
            source += '   ' + command()

        # delete this field
        del self.__commands

        return source

    
    def compile(self, input_vars=None, output_vars=None, local_vars=None) -> None:
        '''
        This method compiles function for later use.
        input_vars, output_vars and local_vars have to be indexable objects.
        Method builds source for .cpp file, compiles it and creates .exe file.
        '''

        if input_vars is None:
            input_vars = []

        if local_vars is None:
            local_vars = []

        if output_vars is None:
            output_vars = []

        # name for output text file
        self.__buffer_file_name = '1'

        # creating unique name of file
        while os.path.exists(self.__buffer_file_name + '.txt'):
            self.__buffer_file_name = '1' + self.__buffer_file_name

        # str variable for building cpp source
        source = str()

        # add headers and defining of main function
        source += '#include <stdio.h>\n#include <stdlib.h>\n#include <iostream>\n#include <fstream>\n#include <string>\n#include <vector>\n\n#define N 50\n\nusing namespace std;\n\n'

        # count for indexing in assembly insertion like %i
        count = 0

        # string with input variables for assembly insertion, like : "r" (c, d)
        input_row = ':'

        # string with output variables for assembly insertion, like : "+r" (c, d)
        output_row = ': '

        # validate output variables
        for var in output_vars:

            if not isinstance(var, Variable):
                raise TypeError('One of the output variables is not of type asm.variables.Variable')

            # set index for variable
            var._set_index(count) 

            # add defining of the variable to source
            source += var._to_str()

            # add cpp function
            exec(f'from __to_str import {var._to_str_func()}\nfunc = {var._to_str_func()}', globals())

            if func not in source:
                print(type(func))
                source += func + '\n'

            # add variable to output variables list
            output_row += '"=r"(' + var._name() + '),'

            count += 1

        # validate input variables
        for var in input_vars:

            if not isinstance(var, Variable):
                raise TypeError('One of the input variables is not of type asm.variable.Variable')

            if var.has_value():
                raise TypeError('Input variable can not have a value.')

            # add cpp function
            exec(f'from __from_str import {var._from_str_func()}\nfunc = {var._from_str_func()}', globals())

            if func not in source:
                source += func + '\n'

            # set index for variable
            var._set_index(count)

            # add variable to input variables list
            input_row += '"r"(' + var._name() + '),'

            count += 1

        self.__input_vars = input_vars
        del input_vars

        # same operation with "local" variables
        for var in local_vars:
            
            if not isinstance(var, Variable):
                raise TypeError('One of the local variables is not of type asm.variable.Variable')

            # set index for variable
            var._set_index(count)

            # add variable to input variables list
            input_row += '"r"(' + var._name() + '),'

            count += 1

        # add defining main function
        source += 'int main()\n{\nstring line;\n'

        # add reading buffer 
        source += f'ifstream buffer;\nbuffer.open("{self.__buffer_file_name + ".txt"}");\n\n'
            
        # add reading of input variables from command-line arguments
        for var in self.__input_vars:
            source += var._to_str_input()

        # add closing buffer file
        source += 'buffer.close();\n'

        for var in local_vars:
            # add defining of the variable to source
            source += var._to_str()

        self.__output_vars = output_vars
        del output_vars

        # get assembler source
        asm_source = self.__build_asm()

        # add row with output variables to assembly insertion
        asm_source += output_row[:-1] + '\n'
        del output_row
        del count

        # add row with input variables to assembly insertion
        asm_source += input_row[:-1] + '\n);\n'
        del input_row

        # add inline assembler to source
        source += asm_source

        # we already don't need this variable
        del asm_source

        # add opening buffer file
        source += '\nofstream f;\n'
        source += f'f.open("{self.__buffer_file_name + ".txt"}");\n'

        # add writing output to buffer file
        for var in self.__output_vars:
            source += 'f << ' + var._to_str_output() + ' + \'\\n\';\n'

        # add closing buffer file
        source += 'f.close();\n'

        # end of main function
        source += '}'

        # create .exe file 
        self.__create_exe(source)

        # now this function is compiled
        self.__is_compiled = True

    
    def __create_exe(self, source:str) -> None:
        '''
        This method compiles created .cpp file and deletes .cpp file.
        '''

        # write source to .cpp file
        with open(self.__buffer_file_name + '.cpp', 'w') as f:
            f.write(source)

        # compile .cpp file
        # with intel assembly syntax and CPP-11
        os.system(f'g++ -masm=intel -std=c++17  -o {self.__buffer_file_name}.exe {self.__buffer_file_name}.cpp') 

        # delete .cpp file
        # os.remove(self.__buffer_file_name + '.cpp')
