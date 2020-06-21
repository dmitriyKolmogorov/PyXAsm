# PyXAsm 0.0.1 (Beta)

This project will help you to learn Assembler and run its source using Python.

It is assumed that the user is a student who studies assembler and doesn't want to understand various syntaxes and compilers, because you can use this libary using CPython.

You should install GCC and add g++.exe compiler to PATH.

## asm.registers
To use register, import it from `asm.registers` and use in instructions.
For example, if you want to use `eax` register with `mov`, your source will be like:
```python
from asm.registers import eax
from asm.instructions import mov

f = Function([mov(eax, 1)])
```

If you want to get all available registers, import `Register` class `from asm.registers` and use class-method `available_registers`:
```python
from asm.registers import Register

print(Register.available_registers())
```

## asm.instructions
To use assembler's instruction, import it from `asm.instruction` and use it as function with arguments.
For example, if you want to use mov with `ax` and `bx` registers, your source will be like:
```python
from asm.registers import ax, bx

f = Function([mov(ax, 1),
              mov(bx, ax])
 ```
## asm.variable
To create variable with cpp type and set value for it import `Variable` class from `asm.variable`.
`Variable()` has two paramters:
  - dtype: type of variable.
  - value (default=None): value for variable. If you use this variable as input variable, set this parameter as `None`.

If you want to create variable with type 'int' and with value equal to 5, you source will be like:
```python
from asm.variable import Variable

a = Variable(dtype='int', value=5)
```

To get all available types use class-method Variable.available_types():
```python
from asm.variable import Variable

print(Variable.available_types())
```
 
## asm.function
Function is the main class of this package. To use it, import Function from `asm.function`. Also, `Function` gets list of instructions from `asm.instructions` as parameter.

To call it later use `Function.compile()`, that has 4 parameters:
  - input_vars : list with input_variables. They can't have a value.
  - local_vars: list with local variables for function.
  - output_var: Variable for output. If this parameter is None, function will always return `None` value.
  - delete_cpp : bool parameter. If True, `Function.compile()` will delete .cpp file.
```python
from asm.instuctions import mov, shl, shr
from asm.function import Function
from asm.registers import eax, ebx
from asm.variable import Variable

a = Variable(dtype='long int')
out = Variable(dtype='int', value=1)

f = Function([mov(eax, a),
              shl(eax, 4),
              shr(eax, 6),
              mov(out, eax)])

f.compile(input_vars=[a], output_var=out)

print(f(1))
print(f(356))
```

Check version_control.md to get all available instructions and types.
