import math
import SHA1
from Crypto.Cipher import AES
import random
import string

def binary_exponent(exponent):
    
    ''' Converts an exponent to binary in order to implement
        the square and multiply scheme'''
    bin_exp = bin(exponent)[2:]
    return bin_exp


def modular_times(a, b, modulus):

    a, b = a % modulus, b % modulus
    return (a * b) % modulus


def modular_square(a, modulus):

    return modular_times(a, a, modulus)


def get_multipliers(a, exponent, modulus):
    
    '''Exponent is given as a binary string.'''
    
    multiply_these = []
    multiplier = a
    for i in reversed(exponent):
        
        if i == '1':
            multiply_these.append(multiplier)
        multiplier = modular_square(multiplier, modulus)
        
    return multiply_these


def process_exponent(exponent, modulus):
    
    exponent = exponent % (modulus - 1)
    exponent = binary_exponent(exponent)
    return str(exponent)


def square_and_multiply(a, exponent, modulus):

    exponent = process_exponent(exponent, modulus)
    multiply_these = get_multipliers(a, exponent, modulus)
    output = 1
    for multiplier in multiply_these:
        output = modular_times(output, multiplier, modulus)
    return output

### Square and multiply requires about O(lg exponent) = O(lg modulus)
### modular multiplication operations, and we have to store O(lg modulus)
### multipliers. Contrast this with naively multiplying
### a and the previous power (exponent) times. This is vastly more efficient.



class Alice(object):

    '''For DH key generation Alice picks a prime p and a generator g of the
        multiplicative group, as well as an exponent a.'''

    def __init__(self):
        self.p = self.get_prime()
        self.g = self.get_generator()
        self.a = self.get_exponent()

    def get_prime(self):
        pass
    ''' Choosing a secure prime is involved and
        beyond the scope of this problem. Security
        depends in part on the smallest odd prime which
        divides p-1. In particular you want this smallest
        factor to be large.'''

    def get_generator(self):
        pass
    ''' As is finding a generator of the multiplicative group
        for a prime field.'''

    def get_exponent(self):
        pass

class Bob(object):

    def __init__(self):
        self.b = 1

    def get_exponent(self, p):
        pass


class DH_Key_Session:

    def __init__(self):
        self.Alice = Alice()
        self.Bob = Bob()
        self.p = self.Alice.p
        self.g = self.Alice.g
        self.a = self.Alice.a
        self.b = self.bob.get_exponent(p)
    
    def generate_key(self):
        
        exponent = modular_times(self.a, self.b, self.p)
        return square_and_multiply(self.g, exponent, self.p)

    def alice_to_bob(self):

        return (self.p, self.g, square_and_multiply(self.g, self.a, self.p))

    def bob_to_alice(self):

        return square_and_multiply(self.g, self.b, self.p)


def key_from_DH(number):

    iv = ''.append(chr(random.choice(string.ascii)) for x in range(16))
    sha1 = SHA1.SHA1()
    
    

################################################################
''' We now write out the exchange explicitly for the case given in the problem.'''

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff

g = 2

alice_key = random.randint(1, p-1)
bob_key = random.randint(1, p-1)

alice_message = square_and_multiply(g, alice_key, p)
bob_message = square_and_multiply(g, bob_key, p)
shared_secret = square_and_multiply(g, bob_key * alice_key, p)

print 'Alice sends to Bob the message', alice_message
print 'Bob sends to Alice the message', bob_message
print 'Their shared secret is', shared_secret
print 'Indeed, Alice thinks it is',square_and_multiply(
    bob_message, alice_key, p)
print 'Meanwhile, Bob thinks it is', square_and_multiply(
    alice_message, bob_key, p)


####################################################################
'''Here is how it would go with the man in the middle attack.'''

