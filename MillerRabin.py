## Implementation of the Miller-Rabin primality test, which returns a
## probabilistic guess of whether an integer n is prime or not, and accuracy
## depends on a parameter k which is given as an input to the test.

import random
from ModularExponentiation import square_and_multiply as modexp

def prepare(integer):

    if integer < 2:
        return 'Invalid input.'

    ## Writes integer - 1 as (2**r) * d where d is odd.
    r = 0
    d = integer - 1

    while d % 2 == 0:
        r += 1
        d = d / 2

    return (r, d)

def test1(a, r_d, integer):

    ## Tests for given element a mod n whether a**d = 1.
    ## Note that we assume integer - 1 = (2 ** r) * d

    d = r_d[1]
    
    return modexp(a, d, integer) == 1

def test2(a, r_d, integer):

    ## Tests for given element a mod n whether a ** (2s * d) = pm 1
    ## for some s between 0 and r - 1

    r, d = r_d[0], r_d[1]

    for s in range(0, r):

        exponent = (2 ** s) * d
        output = modexp(a, exponent, integer)

        if output == 1 or output == integer - 1:
            return True

    return False

def witness(a, r_d, integer):

    ## Returns true if a is a witness to compositeness of integer.
    if test1(a, r_d, integer) == False:
        if test2(a, r_d, integer) == False:
            return True
    return False


def miller_rabin(integer, k):

    ## Returns true if integer is likely a prime.

    r_d = prepare(integer)
    witnesses = random.sample(range(2, integer), k)

    for a in witnesses:

        ## If a is a witness then we know for a fact integer is composite.
        if witness(a, r_d, integer):
            return False
        
    ## If we have run this test k times without finding a witness
    ## we guess that integer is prime.
    return True




        
    

