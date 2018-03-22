import random
from ModularExponentiation import square_and_multiply as modexp
from RSA_primes import RSA_pair
from RSA_math import extended_gcd, totient, modinv, gcd
from BlockParser import BlockParser
from Converter import Converter


class RSA(object):


    def __init__(self, padding = False):
        
        self.init_parameters()
        self.parser = BlockParser(8, padding)
        self.converter = Converter()
 

    def get_modulus(self):
        
        return self.primes[0] * self.primes[1]


    def get_primes(self):
        
        return RSA_pair()

    def init_parameters(self):

        self.primes = self.get_primes()
        self.modulus = self.get_modulus()
        self.group_size = (self.primes[0] - 1) * (self.primes[1] - 1)
        self.public_key = self.public_key()
        self.private_key = self.private_key()
    

    def public_key(self):

        ## Sticky point: Here we are looking at the group of exponents!
        ## As such they live modulo the size of the mult. group, which
        ## is itself phi(modulus). So the multiplicative group of
        ## exponents is size phi(phi(modulus)).'

        if gcd(3, self.group_size) == 1:
            return 3

        else:
            return 17


    def private_key(self):

        return modinv(self.public_key, self.group_size)
    

    def prepare_plaintext(self, string):

        blocks = self.parser.prepare_blocks(string)
        for i in range(len(blocks)):
            blocks[i] = self.converter.str_to_num(blocks[i])
            
        return blocks


    def process_decrypted(self, blocks):

        for i in range(len(blocks)):
            blocks[i] = self.converter.num_to_str(blocks[i])
            
        text = self.parser.process_blocks(blocks)
        return text


    def encrypt(self, string):
        
        blocks = self.prepare_plaintext(string)
        cipher_blocks = []
        
        for block in blocks:
            encrypted = modexp(block, self.public_key, self.modulus)
            cipher_blocks.append(encrypted)
            
        return cipher_blocks


    def decrypt(self, cipher_blocks):
        
        decrypted_blocks = []
        
        for block in cipher_blocks:
            number = modexp(block, self.private_key, self.modulus)
            decrypted_blocks.append(number)
            
        return self.process_decrypted(decrypted_blocks)



        
    
