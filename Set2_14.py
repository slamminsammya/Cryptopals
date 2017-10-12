from Crypto.Cipher import AES
import random
import math
import string

'''Byte at a time ECB decryption (Harder)'''

'''Create AES oracle that uses random key and encrypts
strings as
(random prefix || attacker-controlled input || target-bytes)'''

def pad(plaintext):
    pad_length = (-len(plaintext)) % 16
    return plaintext + chr(pad_length) * pad_length

def parse_as_blocks(text, blocksize):
    blocks = []
    num_blocks = int(math.ceil(len(text)/blocksize))
    text_copy = text[:]
    for x in range(num_blocks):
        blocks.append(text_copy[:blocksize])
        text_copy = text_copy[blocksize:]
    return blocks

'''Begin by creating our oracle. Random key and random
byte prependage are generated at initialization'''

class encryption_oracle(object):
    def __init__(self):
        self.key = self.rand_key()
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.prefix = self.rand_prefix()

    def rand_key(self):
        key = ''.join(random.choice(string.printable) for x in range(16))
        return key

    def rand_prefix(self):
        length = random.randint(1,10)
        prefix = ''.join(random.choice(string.printable) for x in range(length))
        return prefix

    def encrypt(self, plaintext):
        target_bytes = '''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK'''.decode('base64')
        plaintext = pad(self.prefix + plaintext + target_bytes)
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)

##Plan is the following:
##    1) Determine length of (prepend + appendage)
##    2) Determine length of prepend and appendage individually
##    3) Use info from step 2 to create a test block where we
##        can make a library of output blocks
##    4) Use library to compare with isolated bytes, decrypting
##        one byte at a time.

'''This function gets the last n bytes of the target text isolated
in the final block of the ciphertext. It returns the final block of
ciphertext.'''

def isolate_n_bytes(n, oracle):
    ciphertext = oracle.encrypt('')
    initial_length = len(ciphertext)
    isolated_bytes = 0
    plaintext = ''
    while isolated_bytes < n:
        plaintext += 'a'
        ciphertext = oracle.encrypt(plaintext)
        if len(ciphertext) > initial_length:
            isolated_bytes += 1
    return parse_as_blocks(ciphertext, 16)[-1]


'''This is step 1. Unsure if its completely necessary but is not so difficult.'''

def get_length(oracle):
    plaintext = ''
    ciphertext = oracle.encrypt('')
    initial_length = len(ciphertext)
    pad_length = -1
    while len(ciphertext) == initial_length:
        plaintext += 'a'
        ciphertext = oracle.encrypt(plaintext)
        pad_length += 1
    return initial_length - pad_length


'''Given two ciphertexts of equal length, outputs first block is different.'''

def changed_block(ciphertext_1, ciphertext_2):
    blocks_1 = parse_as_blocks(ciphertext_1, 16)
    blocks_2 = parse_as_blocks(ciphertext_2, 16)
    for x in range(len(blocks_1)):
        if blocks_1[x] != blocks_2[x]:
            return x

'''Gets length of prepend and appendage individually, given knowledge of their
total length.'''

def get_individual_lengths(oracle, length):
    pad_length = (- length) % 16
    inserted_text = 'a' * (pad_length + 32)
    base_ciphertext = oracle.encrypt(inserted_text)
    test_vector = 'x' + inserted_text[1:]
    compared_ciphertext = oracle.encrypt(test_vector)
    prepend_endblock = changed_block(base_ciphertext, compared_ciphertext)
    n = 1

    while prepend_endblock == changed_block(base_ciphertext, compared_ciphertext):
        test_vector = inserted_text[:n] + 'x' + inserted_text[n + 1:]
        compared_ciphertext = oracle.encrypt(test_vector)
        n += 1

    prepend_length = 16 -(n-1) + (16 * prepend_endblock)
    append_length = length - prepend_length
    return (prepend_length, append_length)

'''Gives a dictionary key: value where key is a character and
value is the encryption of the block (key || chosen_text || pad)
and uses knowledge of length of prepend and appendage.'''

def create_dictionary(oracle, chosen_text):
    lengths = get_individual_lengths(oracle, get_length(oracle))
    prepend_pad, appendage_pad = (-lengths[0]) % 16, (-lengths[1]) % 16
    dictionary = {}
    observation_block = (lengths[0] + prepend_pad) / 16
    for x in string.printable:
        chosen_plaintext = prepend_pad * 'a' + pad(x + chosen_text) + appendage_pad * 'a'
        ciphertext = oracle.encrypt(chosen_plaintext)
        cipher_blocks = parse_as_blocks(ciphertext, 16)
        dictionary[x] = cipher_blocks[observation_block]
    return dictionary


def byte_at_time(oracle):
    target_bytes = ''
    lengths = get_individual_lengths(oracle, get_length(oracle))
    prepend_pad, appendage_pad = (-lengths[0]) % 16, (-lengths[1]) % 16
    pad = 'a' * (prepend_pad + appendage_pad)
    observation_block = int(len(oracle.encrypt(pad)) / 16)

    for n in range(lengths[1]):
        chosen_plaintext = (prepend_pad + appendage_pad + 1 + n) * 'a'
        dictionary = create_dictionary(oracle, target_bytes)
        ciphertext = oracle.encrypt(chosen_plaintext)
        cipher_blocks = parse_as_blocks(ciphertext, 16)

        for x in string.printable:
            if dictionary[x] == cipher_blocks[observation_block]:
                target_bytes = x + target_bytes

    return target_bytes
        

