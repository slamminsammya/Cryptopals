## Here we give a rough algorithm to generate pairs of RSA primes.
## This is not as secure as it should be, we just want a pair of
## 16 bit primes.

## Actual generation is quite a bit more involved since primes
## that are very smooth (small factors of p-1) or pairs close to eachother
## tend to not be so secure.

## 1) Pick random odd integer in a given range.
## 2) Test this integer for divisibility against some small primes.
## 3) Do Miller-Rabin primality test. If likely prime, we keep it. If not
##    repeat until we find a prime. Likely to


import random
from MillerRabin import miller_rabin

small_primes = [2, 3, 5, 7, 11, 13, 17]

def test_division(integer):

    for prime in small_primes:
        if integer % prime == 0:
            return False

    return True

def get_prime():

    while True:
        
        candidate = random.randint(2 ** 16, 2** 17)
        
        if test_division(candidate):
            if miller_rabin(candidate, 6):
                ## 6 iterations of Miller-Rabin is sufficient for confidence
                ## that the given candidate is prime.
                
                return candidate

def RSA_pair():

    ## Generates an RSA pair.
    return [get_prime(), get_prime()]
    
