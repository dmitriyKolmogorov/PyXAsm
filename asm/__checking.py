# Each function in this module validates input for variables and converts it to the correct form

def check_int(number:int) -> int:
    '''
    This function raises exceptions if argument is not whole number or argument has not int or float type.
    '''
    
    # argument is not a number
    if not (isinstance(number, int) or isinstance(number, float)):
        raise TypeError('This variable is not number.')

    # argument is not a whole number
    if number % 1 != 0:
        raise TypeError('This number is not integer.')

    return int(number)


def check_int_arr(arr) -> list:
    '''
    This function raises exception if argument is not object with integers in it.
    '''

    for i in range(len(arr)):

        # current element is not a number
        if not (isinstance(arr[i], int) or isinstance(arr[i], float)):
            raise TypeError('Argument has number that has not an integer type.')

        # current element is not a whole number
        if arr[i] % 1 != 0:
            raise TypeError('Argument has number which type is not an integer number.')

        # converting current element to int type
        arr[i] = int(arr[i])

    # converting to list
    return list(arr)


def check_int_2d_arr(arr) -> list:
    '''
    This function raises exception if argument is not indexable object with indexable objects with integers.
    '''

    for i in range(len(arr)):
        for j in range(len(arr[i])):

            if not (isinstance(arr[i][j], int) or isinstance(arr[i][j], float)):
                raise TypeError('Argument has number that has not an integer type.')

            if arr[i][j] % 1 != 0:
                raise TypeError('Array has number which type is not an integer number.')

            arr[i][j] = int(arr[i][j])

    return list(arr)


def check_float(number:float) -> float:
    '''
    This function raises exception if argument is not number.
    '''

    if not (isinstance(number, int) or isinstance(number, float)):
        raise TypeError('This variable is not number.')

    return float(number)


def check_float_arr(arr) -> list:
    '''
    This function raises exception if argument has elements which type is not float.
    '''

    for i in range(len(arr)):
        if not (isinstance(arr[i], int) or isinstance(arr[i], float)):
            raise TypeError('This variable is not number.')

        arr[i] = float(arr[i])

    return list(arr)


def check_float_2d_arr(arr) -> list:
    '''
    This function raises exception if argument is not object with objects with float numbers.
    '''

    for i in range(len(arr)):
        for j in range(len(arr[i])):

            if not (isinstance(arr[i][j], int) or isinstance(arr[i][j], float)):
                raise TypeError('Argument has elements that has not an integer type.')

            arr[i][j] = float(arr[i][j])

    return list(arr) 


def check_char(symbol:str) -> None:
    '''
    This function raises exception if argument is not symbol.
    '''

    if not isinstance(symbol, str):
        raise TypeError('Argument is not string or char.')

        if len(symbol) > 1:
            raise TypeError('Argument is string, not char')

    return symbol


def check_char_arr(arr) -> list:
    '''
    This function raises exception if argument has elementss that are not char.
    '''

    for i in range(len(arr)):
        if not isinstance(arr[i], str):
            raise TypeError('Argument has elements that is not string or char.')

        if len(arr[i]) > 1:
            raise TypeError('Argument has elements that is string, not char')

    return list(arr)
