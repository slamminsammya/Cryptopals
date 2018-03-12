import math

def binary_exponent(exponent):
    
    ''' Converts an exponent to binary in order to implement
        the square and multiply scheme'''
    bin_exp = bin(exponent)[2:]
    return bin_exp


def modular_times(a, b, modulus):

    ''' Returns a * b mod (modulus). Pre-processing reduces a and b
        in case they are not already between 0 and modulus.'''

    a, b = a % modulus, b % modulus
    return (a * b) % modulus


def modular_square(a, modulus):

    ''' Uses modular_times to multiply a by itself.'''

    return modular_times(a, a, modulus)


def get_multipliers(a, exponent, modulus):
    
    '''Exponent is given as a binary string. Given this, any bit that is
        one in the binary expansion corresponds to a power of a that we
        must store to be multiplied at the end. Function returns this list.'''
    
    multiply_these = []
    multiplier = a

    ''' We look at exponent from least to most significant bits, hence
        reversed(exponent).'''
    for i in reversed(exponent):
        
        if i == '1':
            multiply_these.append(multiplier)
        multiplier = modular_square(multiplier, modulus)
        
    return multiply_these


def process_exponent(exponent, modulus):

    ''' Pre-process the exponent so that it is in a valid range. Then convert
        it to binary string.'''
    
    exponent = exponent % (modulus - 1)
    exponent = binary_exponent(exponent)
    return str(exponent)

def modular_product(terms, modulus):

    ''' Given a list and a modulus, returns the product of all terms in a list.
    '''
    output = 1
    
    for term in terms:
        output = modular_times(output, term, modulus)

    return output

def square_and_multiply(a, exponent, modulus):

    ''' Puts it all together to perform efficient exponentiation in
        a finite group via square and multiply.'''

    exponent = process_exponent(exponent, modulus)
    multiply_these = get_multipliers(a, exponent, modulus)
    output = modular_product(multiply_these, modulus)
    
    return output

### Square and multiply requires about O(lg exponent) = O(lg modulus)
### modular multiplication operations, and we have to store O(lg modulus)
### multipliers. Contrast this with naively multiplying
### a and the previous power (exponent) times. This is vastly more efficient.


