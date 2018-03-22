import random
from ModularExponentiation import square_and_multiply as modexp
from RSA_primes import RSA_pair
from RSA_math import extended_gcd, totient, modinv, gcd


class RSA(object):


    def __init__(self):
        
        self.primes = self.get_primes()
        self.modulus = self.get_modulus()
        self.group_size = (self.primes[0] - 1) * (self.primes[1] - 1)
        self.public_key = self.public_key()
        self.private_key = self.private_key()
 

    def get_modulus(self):
        
        return self.primes[0] * self.primes[1]


    def get_primes(self):
        
        return RSA_pair()
    

    def public_key(self):

        ## Sticky point: Here we are looking at the group of exponents!
        ## As such they live modulo the size of the mult. group, which
        ## is itself phi(modulus). So the multiplicative group of
        ## exponents is size phi(phi(modulus)).
        public_key = 0
        while gcd(public_key, self.group_size) > 1:
            public_key = random.randint(3, self.group_size - 1)

        return public_key


    def private_key(self):

        return modinv(self.public_key, self.group_size)


    def string_to_number(self, string):
        
        string = string.encode('hex')
        string = int(string, 16)
        return string
    

    def number_to_string(self, number):
        
        number = '%x' % number
        number = number.decode('hex')
        return number


    def encrypt(self, string):
        
        string = self.string_to_number(string)
        encrypted = modexp(string, self.public_key, self.modulus)
        return encrypted


    def decrypt(self, number):
        
        decrypted = modexp(number, self.private_key, self.modulus)
        decrypted = self.number_to_string(decrypted)
        return decrypted

r = RSA()
a = 'h'
b = r.encrypt(a)
c = r.decrypt(b)

    
        
    
