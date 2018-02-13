from Set3_18 import CTR_Cipher, repeated_xor
from Set1_7 import aes128_decrypt

class ReadWrite_API(CTR_Cipher):

    def __init__(self):
        super(ReadWrite_API, self).__init__(chr(0)*8)

    def edit(self, ciphertext, offset, newtext):
        plaintext = self.encrypt(ciphertext)
        plaintext = plaintext[:offset] + newtext + plaintext[offset + len(newtext):]
        new_ciphertext = self.encrypt(plaintext)
        return new_ciphertext


a = open('25.txt', 'rb')
ctext = a.read()
a.close()

API = ReadWrite_API()
plaintext = aes128_decrypt(ctext, 'YELLOW SUBMARINE')
ciphertext = API.encrypt(plaintext)


length = len(ciphertext)
keystream = API.edit(ciphertext, 0, chr(0) * length)
guessed_plaintext = repeated_xor(keystream, ciphertext)
