from Crypto.Cipher import AES
import random
import string
import Set1_7
import Set1_6
from itertools import izip, cycle

def pad(text, blocksize):
    pad_length = (blocksize - (len(text) % blocksize)) % blocksize
    pad_character = chr(pad_length)
    padded_text = text + pad_length * pad_character
    return padded_text

def xor(p,q):
    if len(q) > len(p):
        p,q = q,p
    return ''.join(chr(ord(a)^ord(b))for a,b in izip(p, cycle(q)))

class CBC_AES(object):
    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_ECB)
        self.IV = ''.join(random.choice(string.printable) for x in range(16))

    def encrypt(self, text):
        """ First pad text to be multiple of blocksize.
        """
        text = pad(text, 16)

        """ Parse the text as blocks. """

        blocks = Set1_7.parse_as_blocks(text, 16)
        diffusion = self.IV
        ciphertext = ''

        """ Run CBC mode."""
        for n in range(len(blocks)):
            feed_me = xor(blocks[n], diffusion)
            output = self.cipher.encrypt(feed_me)
            ciphertext += output
            diffusion = output

        return ciphertext

    def decrypt(self, ciphertext):
        blocks = [self.IV] + Set1_7.parse_as_blocks(ciphertext, 16)
        plaintext = ''

        for n in range(len(blocks) - 1):
            ''' decrypted is text that was passed into the
            AES encryption. To get plaintext we must XOR
            with the 'diffusion', which is the previous index
            of ciphertext. The IV acts as the zeroth block
            of ciphertext for this purpose.'''

            decrypted = self.cipher.decrypt(blocks[-n - 1])
            diffusion = blocks[-n - 2]
            plaintext += xor(decrypted, diffusion)

        return plaintext
#Output is in hex.

class encryption_oracle(object):
        def __init__(self):
            self.key = self.rand_key()
            self.CBC = CBC_AES(self.key)
            self.ECB = AES.new(self.key, AES.MODE_ECB)
            self.mode = 0

        def rand_key(self):
            key = ''.join(random.choice(string.printable) for n in range(16))
            return key

        def random_pad(self, text):
            pad_lengths = [random.randrange(5,11), random.randrange(5,11)]
            pad_1 = ''.join(random.choice(string.printable) for x in range(pad_lengths[0]))
            pad_2 = ''.join(random.choice(string.printable) for x in range(pad_lengths[1]))
            return pad_1 + text + pad_2

        def encrypt(self, text):
            CBC = random.randrange(2)
            self.mode = CBC
            text = pad(self.random_pad(text), 16)
            if CBC:
                return self.CBC.encrypt(text)
            else:
                return self.ECB.encrypt(text)

class encryption_oracle_2(object):
    def __init__(self):
        self.key = self.rand_key()
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def rand_key(self):
        key = ''.join(random.choice(string.printable) for n in range(16))
        return key

    def encrypt(self, text):
        text = pad(text, 16)
        return self.cipher.encrypt(text)
    

def detect_mode(oracle):
    test_vector = '0'*16*4
    ciphertext = oracle.encrypt(test_vector)
    cipher_blocks = Set1_7.parse_as_blocks(ciphertext, 16)
    guess = cipher_blocks[1] != cipher_blocks[2]
    if guess:
        return 'CBC'
    else:
        return 'ECB'

def detect_blocksize(text, oracle):
    ciphertext = oracle.encrypt(text)
    length = len(ciphertext)
    max_blocksize = int(length / 2)
    blocksize_scores = {}
    
    for x in range(max_blocksize):
        max_pairs = int(math.floor(length / x)) - 1
        edit_distance = Set1_6.av_distance(ciphertext, max_pairs, x)
        blocksize_scores[i] = edit_distance

    return max(blocksize_scores.items(), key = lambda s: s[1])[0]

def ciphertext_dict(oracle, blocksize):
    pass


def ecb_decrypt(text, oracle):
    '''First determine blocksize using hamming distance.'''
    blocksize = detect_blocksize(text, oracle)

    '''Then determine the oracle is using ecb.'''
    mode = detect_mode(oracle)

    if mode != 'ECB':
        return None

    else:
       pass 




