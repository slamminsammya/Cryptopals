import random

from Set2_16 import TargetCiphertext, IsAdmin
from Set3_18 import CTR_Cipher, repeated_xor


class Encrypt_Input(object):

    def __init__(self):

        self._nonce = ''.join(chr(random.randrange(256)) for n in range(8))
        self._cipher = CTR_Cipher(self._nonce)

    def prepare(self, string):
        
        string = string.replace('=', '')
        string = string.replace(';', '')
        string = ("comment1=cooking%20MCs;userdata="
             + string
             + ";comment2=%20like%20a%20pound%20of%20bacon")
        return string

    def encrypt(self, string):

        string = self.prepare(string)
        ciphertext = self._cipher.encrypt(string)
        return ciphertext

    def decrypt(self, ciphertext):

        return self._cipher.encrypt(ciphertext)

def Malicious_Insertion(ctr_oracle, desired_string):
    
    base_length = len(ctr_oracle.encrypt(''))
    length = max(base_length, len(desired_string))
    plaintext_length = 2 * length
    chosen_plaintext = plaintext_length * chr(0)
    ciphertext = ctr_oracle.encrypt(chosen_plaintext)
    malicious_block = ciphertext[length : 2 * length]
    malicious_block = repeated_xor(malicious_block, desired_string)
    malicious_ciphertext = (ciphertext[:length]
                            + malicious_block
                            + ciphertext[2 * length:])
    return malicious_ciphertext


    
    
    

