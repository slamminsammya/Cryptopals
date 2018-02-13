import random
import string
import math
import time
from itertools import izip

from Set3_21 import MT19937
from Set3_17 import XOR


class RNG_Stream_Cipher(object):
    

    def __init__(self):
        
        self.seed = random.getrandbits(16)
        self.RNG = MT19937(self.seed)
        self.keystream = None

    def _8bit(self, number):
        
        return number & 0xFF

    def generate_keystream(self, length):
        
        keystream = ''
        for i in range(length):
            Random8Bit = self._8bit(self.RNG.extract_number())
            RandomCharacter = chr(Random8Bit)
            keystream += RandomCharacter
        self.keystream = keystream
        return keystream

    def encrypt(self, text):

        length = len(text)
        keystream = self.generate_keystream(length)
        ciphertext = ''.join(XOR(a,b) for a, b in izip(text, keystream))
        return ciphertext

    def decrypt(self, ciphertext):

        length = len(ciphertext)
        plaintext = ''.join(XOR(a,b) for a, b in izip(self.keystream, ciphertext))
        return plaintext


known_plaintext = 'A' * 14
pad_length = random.randrange(10)
random_pad = ''.join(random.choice(string.printable)
                     for x in range(pad_length))
plaintext = random_pad + known_plaintext


a = RNG_Stream_Cipher()
ciphertext = a.encrypt(plaintext)

### Try an exhaustive search, since key is not very long. Just 16 bits!
### Use knowledge of final 14 bytes of the plaintext.
ciphertext_length = len(ciphertext)
known_keystream = ''.join(XOR(ciphertext[i], 'A') for i in range(
    pad_length, ciphertext_length))

def test_seed(seed):
    test_RNG = MT19937(seed)
    keystream = ''.join(chr(test_RNG.extract_number() & 0xFF)
                        for x in range(ciphertext_length))
    keystream = keystream[pad_length:]
    if keystream == known_keystream:
        return True
    else:
        return False


start = time.time()
for n in range(2**16):
    seed = n
    if test_seed(seed):
        print seed
print time.time() - start

## Took two minutes.
    
