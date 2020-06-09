def mov(var1, var2):
    '''
    Function, that builds mov-command.
    Since mov is binary operation, mov() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"mov ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def AND(var1, var2):
    '''
    Function, that builds AND-command.
    Since AND is binary operation, AND() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"AND ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def OR(var1, var2):
    '''
    Function, that builds OR-command.
    Since OR is binary operation, OR() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"OR ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def xor(var1, var2):
    '''
    Function, that builds XOR-command.
    Since XOR is binary operation, xor() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"XOR ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def NOT(var1):
    '''
    Function, that builds not-command.
    Since inc is unary operation, NOT() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"NOT ' + str(var1) + ';"\n'

    return build_command


def shl(var1, var2):
    '''
    Function, that builds shl-command.
    Since shl is binary operation, shl() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"shl ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def shr(var1, var2):
    '''
    Function, that builds shr-command.
    Since shr is binary operation, shr() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"shr ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def sal(var1, var2):
    '''
    Function, that builds sal-command.
    Since sal is binary operation, sal() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"sal ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def sar(var1, var2):
    '''
    Function, that builds sar-command.
    Since sar is binary operation, sar() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"sar ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def xchg(var1, var2):
    '''
    Function, that builds xchg-command.
    Since xchg is binary operation, xchg() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"xchg ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def add(var1, var2):
    '''
    Function, that builds add-command.
    Since add is binary operation, add() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"add ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def adc(var1, var2):
    '''
    Function, that builds adc-command.
    Since adc is binary operation, adc() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"adc ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def sub(var1, var2):
    '''
    Function, that builds sub-command.
    Since sub is binary operation, sub() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"sub ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def sbb(var1, var2):
    '''
    Function, that builds sbb-command.
    Since sbb is binary operation, sbb() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"sbb ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def inc(var1):
    '''
    Function, that builds inc-command.
    Since inc is unary operation, inc() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"inc ' + str(var1) + ';"\n'

    return build_command


def dec(var1):
    '''
    Function, that builds dec-command.
    Since dec is unary operation, dec() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"dec ' + str(var1) + ';"\n'

    return build_command


def cbw():
    '''
    Function, that builds cbw-command.
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"cbw;"'

    return build_command


def cwd():
    '''
    Function, that builds cwd-command.
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"cwd;"'
    return build_command


def idiv(var1):
    '''
    Function, that builds idiv-command.
    Since idiv is unary operation, idiv() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"idiv ' + str(var1) + ';"\n'

    return build_command


def mul(var1):
    '''
    Function, that builds mul-command.
    Since mul is unary operation, mul() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"mul ' + str(var1) + ';"\n'

    return build_command


def div(var1):
    '''
    Function, that builds div-command.
    Since div is unary operation, div() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"div ' + str(var1) + ';"\n'

    return build_command


def bt(var1, var2):
    '''
    Function, that builds bt-command.
    Since bt is binary operation, bt() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"bt ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def bts(var1, var2):
    '''
    Function, that builds bts-command.
    Since bts is binary operation, bts() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"bts ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def btr(var1, var2):
    '''
    Function, that builds btr-command.
    Since btr is binary operation, btr() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"btr ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def btc(var1, var2):
    '''
    Function, that builds btc-command.
    Since btc is binary operation, btc() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"btc ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def bsf(var1, var2):
    '''
    Function, that builds bsf-command.
    Since bsf is binary operation, bsf() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"bsf ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def bsr(var1, var2):
    '''
    Function, that builds bsr-command.
    Since bsr is binary operation, bsr() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"bsr ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command


def jmp(var1):
    '''
    Function, that builds jmp-command.
    Since jmp is unary operation, jmp() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"jmp ' + str(var1) + ';"\n'

    return build_command


def je(var1):
    '''
    Function, that builds je-command.
    Since je is unary operation, je() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"je ' + str(var1) + ';"\n'

    return build_command


def jl(var1):
    '''
    Function, that builds jl-command.
    Since jl is unary operation, jl() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"jl ' + str(var1) + ';"\n'

    return build_command


def jg(var1):
    '''
    Function, that builds jg-command.
    Since jg is unary operation, jg() has one argument. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"jg ' + str(var1) + ';"\n'

    return build_command


def cmp(var1, var2):
    '''
    Function, that builds cmp-command.
    Since cmp is binary operation, cmp() has two arguments. 
    Return str type.
    '''
    def build_command() -> str:
        # построение команды    
        return '"cmp ' + str(var1) +  ', ' + str(var2) + ';"\n'

    return build_command