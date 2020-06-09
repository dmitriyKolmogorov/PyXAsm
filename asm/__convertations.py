def char(value:str) -> str:
    '''This function checks if string has one symbol in it.'''

    if len(value) > 1:
        raise TypeError('Got string as argument, expected char.')

    return value


def arr(string:str) -> list:
    '''This function converts string to list.'''

    try:
        exec(f'l = {string}')
    except Exception:
        raise TypeError('Cannot convert to array.')

    return l