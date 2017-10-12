from Crypto.Cipher import AES
import math
import random
import string
import Set1_7
import Set1_6
from itertools import izip, cycle
import Set1_9

class encryption_oracle(object):
    def __init__(self):
        self.key = self.rand_key()
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def rand_key(self):
        key = ''.join(random.choice(string.printable) for n in range(16))
        return key

    def encrypt(self, plaintext):
        appendage = '''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK'''.decode('base64')
        plaintext = Set1_9.pad(plaintext + appendage, 16)
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)


def get_blocksize(cipher):
    pass


def detect_mode(cipher):
    pass


def make_ctext_library(cipher, chosen_plaintext, blocksize, block_index):
    ciphertext_library = {}

    for x in string.printable:
        plaintext = chosen_plaintext + x
        ciphertext = cipher.encrypt(plaintext)
        cipher_blocks = Set1_7.parse_as_blocks(ciphertext, 16)
        ciphertext_library[x] = cipher_blocks[block_index]
        
    return ciphertext_library

def one_byte_ECB(cipher, blocksize):
    '''Assume here string_length <= blocksize'''
    hidden_string = ''
    string_length = len(cipher.encrypt(''))
    num_blocks = int(math.floor(string_length / blocksize))

    for block_index in range(num_blocks):
        for n in range(blocksize):
            
            chosen_plaintext = 'A' * (blocksize - 1 - n) + hidden_string
            ciphertext = cipher.encrypt('A' * (blocksize - 1 - n))
            cipher_blocks = Set1_7.parse_as_blocks(ciphertext, blocksize)
            chosen_cipher_block = cipher_blocks[block_index]
            ciphertext_library = make_ctext_library(cipher, chosen_plaintext, blocksize, block_index)
            for x in string.printable:
                if chosen_cipher_block == ciphertext_library[x]:
                    hidden_string += x
                    
    return hidden_string
    

##def first_byte(cipher, blocksize):
##    chosen_plaintext = 'A' * (blocksize - 1)
##    ciphertext = cipher.encrypt(chosen_plaintext)
##    ciphertext_library = make_ctext_library(cipher, chosen_plaintext, blocksize)
##    for x in ciphertext_library.keys():
##        if ciphertext[:blocksize] == ciphertext_library[x]:
##            return x

