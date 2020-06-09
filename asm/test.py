from asm.instuctions import mov, shl, shr
from asm.function import Function
from asm.registers import eax, ebx
from asm.variables import Variable

a = Variable(dtype='long int')
b = Variable(dtype='int[]', value=[1, 2, 3])

out = Variable(dtype='int')

f = Function([mov(eax, a),
              shl(eax, 4),
              shr(eax, 6),
              mov(out, eax)])

f.compile(input_vars=[a], local_vars=[b], output_vars=[out])

print(f(1))
print(f(356))
