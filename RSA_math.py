## Here is the math needed to run RSA. In particular we need:
## 1) Extended Euclidean Algo.
## 2) An algorithm to factor a number.
## 3) The Euler totient function.
## 4) A function that computes multiplicative inverses in a cyclic group.

import math

def div(a, b):

    ## Returns q s.t. qa + r = b, with 0 <= r < a
    if a > b:
        a, b = b, a

    return b/a


def extended_gcd(a, b):
    ## Returns a dictionary with the relevant values.
    
    if a > b:
        a, b = b, a

    s = 0
    old_s = 1

    t = 1
    old_t = 0

    r = a
    old_r = b

    while r != 0:
        q = div(old_r, r)
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        
        

    output = {}
    output[a] = old_t
    output[b] = old_s
    output['gcd'] = old_r
    
    return output

def gcd(a,b):
    ## returns the gcd of a,b

    if a > b:
        a, b = b, a

    if a == 2:
        
        if int(str(b)[-1]) % 2 == 0:
            return 2
        else:
            return 1

    elif a == 3:
        
        digits = [int(x) for x in list(str(b))]
        if sum(x for x in digits) % 3 == 0:
            return 3
        else:
            return 1

    elif a == 5:

        if str(b)[-1] == '5' or str(b)[-1] == '0':
            return 5

        else:
            return 1

    else:

        while a > 0:
            a, b = b % a, a
            
        return b

##    return extended_gcd(a,b)['gcd']

##################################################################

## We now want to build an algorithm to factor a number. Nothing fancy here -
## we will build an algorithm to construct primes up to a given bound, and
## then test divide until a factor is found.

## First a basic sieve test of primality.

def sieve(data, number):
    ## Given data of a list and a number, it will set all values in list of
    ## index 2 * number, 3 * number, 4 * number, ...., to None.

    index = 2 * number
    
    while True:
        try:
            data[index] = None
            index += number
            
        except IndexError:
            return data


def next_prime(data, last_prime):
    ## Finds next prime in partially sieved set of integers, given the last one
    ## In case there are none left, it returns None.

    index = last_prime + 1
    
    try:
        integer = data[index]

    except IndexError:
        return None
    
    while integer == None:
        index += 1

        try:
            integer = data[index]
            
        except IndexError:
            break
                
    return integer


def prime_sieve(bound):
    ## Does a prime sieve up to the bound.

    integers = range(bound)
    prime = 2
    
    while prime != None:
        sieve(integers, prime)
        prime = next_prime(integers, prime)
                       
    return integers


def primes(bound):
    ## Gives a list of primes up to the bound.

    sieve = prime_sieve(bound)[2:]
    primes = [p for p in sieve if p != None]
    return primes

#############################################################################

## Now we do our dirty algorithm to extract a factor from a number.

def get_factor(number):

    if number < 0:
        number = -number

    bound = int(math.floor(math.sqrt(number))) + 1
    bound = max(bound, 4)
    prime_list = primes(bound)
    
    for prime in prime_list:
        if number % prime == 0:
            return prime
        
    return number


def factorize(number):
    
    ## Collects information about factorization of a number.
    if number < 0:
        number = -number
        
    data = factorization()
    
    while number > 1:
        factor = get_factor(number)
        data.add_factor(factor)
        number = number / factor

    return data


def factors(number):
    
    ## Returns list of prime factors without multiplicities.
    return factorize(number).prime_factors()


def factors_mult(number):
    
    ## Returns list of prime factors and multiplicities as tuples.
    return factorize(number).multiplicities()

  
class factorization(object):

    ## This class has a dictionary with prime factors of a given number with
    ## their multiplicities. It can give you a list whose elements are pairs
    ## (prime, multiplicity) in ascending order of prime size.

    def __init__(self):
        
        self.dictionary = {}

    def add_factor(self, prime):
        
        ## Increases mulitplicity of prime by one. Annoying normally since
        ## have to first check if key value is there.
        if prime in self.dictionary.keys():
            self.dictionary[prime] += 1

        else:
            self.dictionary[prime] = 1

    def prime_factors(self):
        
        return sorted(self.dictionary.keys())


    def multiplicities(self):
        
        return [(prime,
                 self.dictionary[prime]) for prime in self.prime_factors()]



###############################################################################

## Now a function that computes the totient function of a given integer.
## First factorizes and then uses formula for totient of a prime power.

def prime_totient(prime, power):
    
    return (prime - 1) * prime ** (power - 1)


def totient(number):
    
    factors = factors_mult(number)
    totients = [prime_totient(prime, power) for (prime, power) in factors]
    totient = 1

    for x in totients:
        totient = totient * x

    return totient


###############################################################################

## Compute the multiplicative inverse of a mod n, if possible. Raises value
## error if element is not invertible.

def modinv(a, n):

    data = extended_gcd(a, n)
    
    if data['gcd'] != 1:
        raise ValueError

    else:
        return data[a] % n
