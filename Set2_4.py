import random
import math
import string
from Crypto.Cipher import AES

def pad(text, blocksize):
    padlength = blocksize - (len(text) % blocksize)
    return text + padlength * chr(padlength)

def parse_as_blocks(text, blocksize):
    blocks = []
    num_blocks = int(math.ceil(len(text)/blocksize))
    text_copy = text[:]
    for x in range(num_blocks):
        blocks.append(text_copy[:blocksize])
        text_copy = text_copy[blocksize:]
    return blocks


def parser(string):
    pairs = string.split('&')
    output_dictionary = {}
    for x in pairs:
        keypair = x.split('=')
        key = keypair[0]
        value = keypair[1]
        output_dictionary[key] = value
    return output_dictionary

def profile_for(address):
    if '&' in address or '=' in address:
        print 'Not a valid address. Cannot contain characters "&" or "=".'

    else:
        uid = '10'
        return 'email=' + address + '&uid=' +uid + '&role=user'
    

class oracle(object):
    def __init__(self):
        self.key = self.rand_key()
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def rand_key(self):
        key = ''.join(random.choice(string.printable) for n in range(16))
        return key

    def encrypt(self, plaintext):
        plaintext = pad(plaintext, 16)
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)

    def parse(self, ciphertext):
        plaintext = self.decrypt(ciphertext)
        padding_char = plaintext[-1]
        if ord(padding_char) <= 16:
            n = ord(padding_char)
            plaintext = plaintext[:len(plaintext) - n]
        return parser(plaintext)

    def feed(self, address):
        plaintext = profile_for(address)
        return self.encrypt(plaintext)

def make_admin(oracle):
    malicious_address_1 = 'a'* 10 + pad('admin', 16)+'@gmail.com'
    '''Use the encrypted block 'admin' and padding'''
    given_ciphertext_1 = oracle.feed(malicious_address_1)
    malicious_block_3 = parse_as_blocks(given_ciphertext_1, 16)[1]

    fixed_length = len('email=' + '&uid=10' + '&role=' + '@gmail.com')
    needed_address_length = 16 - (fixed_length % 16)

    malicious_address_2 = 'a'*needed_address_length + '@gmail.com'
    given_ciphertext_2 = oracle.feed(malicious_address_2)
    malicious_block_1 = parse_as_blocks(given_ciphertext_2, 16)[0]
    malicious_block_2 = parse_as_blocks(given_ciphertext_2, 16)[1]

    malicious_ciphertext = malicious_block_1 + malicious_block_2 + malicious_block_3
    return malicious_ciphertext

