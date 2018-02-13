import random

from Set2_16 import EncryptionOracle
from Set1_7 import parse_as_blocks
from Set3_18 import repeated_xor


class IV_is_Key(EncryptionOracle):


    def __init__(self):
        
        super(IV_is_Key, self).__init__()
        self.IV = self.key

    def check_ascii(self, text):
        
        for character in text:
            if ord(character) > 128:
                print text
                raise Exception('Non ASCII compliant byte.')
                

    def decrypt(self, ciphertext):
        
        plaintext = super(IV_is_Key, self).decrypt(ciphertext)
        self.check_ascii(plaintext)
        return plaintext

def modify_cipherblocks(ciphertext):
    cipherblocks = parse_as_blocks(ciphertext, 16)
    ciphertext = cipherblocks[0] + 16 * chr(0) + cipherblocks[0]
    return ciphertext

s = IV_is_Key()
plaintext = ''.join(chr(random.randrange(128)) for n in range(48))
ciphertext = s.encrypt(plaintext)
malicious_ciphertext = modify_cipherblocks(ciphertext)
s.decrypt(malicious_ciphertext)


