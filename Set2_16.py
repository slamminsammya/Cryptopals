## CBC bitflipping

from Crypto.Cipher import AES
import math
import random
import string
import Set1_9
import Set1_7
import Set2_14


class EncryptionOracle(object):
    def __init__(self):
        self.key = self.RandomKey()
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.IV = ''.join(chr(random.randrange(256)) for x in range(16))

    def RandomKey(self):
        key = ''.join(chr(random.randrange(256)) for x in range(16))
        return key

    def encrypt(self, plaintext):
        PaddedPlaintext = Set2_14.pad(plaintext)
        blocks = Set1_7.parse_as_blocks(PaddedPlaintext, 16)
        XORThis = self.IV
        ciphertext = ''
        
        for n in range(len(blocks)):
            GetsEncrypted = Set1_9.xor(blocks[n], XORThis)
            CipherBlock = self.cipher.encrypt(GetsEncrypted)
            ciphertext += CipherBlock
            XORThis = CipherBlock
            
        return ciphertext

    def decrypt(self, ciphertext):
        CipherBlocks = [self.IV] + Set1_7.parse_as_blocks(ciphertext, 16)
        plaintext = ''

        for n in range(len(CipherBlocks) - 1):
            WasEncrypted = self.cipher.decrypt(CipherBlocks[-n - 1])
            XORThis = CipherBlocks[-n - 2]
            plaintext = Set1_9.xor(WasEncrypted, XORThis) + plaintext

        return plaintext
    


def TargetCiphertext(string, EncryptionOracle):
    
    string = string.replace(';','')
    string = string.replace('=','')
    plaintext = ("comment1=cooking%20MCs;userdata="
                 + string
                 + ";comment2=%20like%20a%20pound%20of%20bacon")
    ciphertext = EncryptionOracle.encrypt(plaintext)
    return ciphertext


def IsAdmin(ciphertext, EncryptionOracle):
    
    plaintext = EncryptionOracle.decrypt(ciphertext)
    tuples = plaintext.split(';')
    for x in tuples:
        x = tuple(x.split('='))
        if x == ('admin', 'true'):
            return True
    return False

def XOR(a,b):
    
    return Set1_9.xor(a,b)

def BitFlip(CipherText, TargetBlock,
            TargetIndex, DesiredCharacter, Plaintext):
    ### Given a ciphertext, alters single bit of ciphertext in order to flip a single bit of
    ### the decrypted plaintext to the desired character. TargetBlock cannot be 0
    ### (needs a block prior to mess around with).

    CipherBlocks = Set1_7.parse_as_blocks(CipherText, 16)
    FlipBlock = TargetBlock - 1
    FlipCharacter = CipherBlocks[FlipBlock][TargetIndex]

    PlaintextBlocks = Set1_7.parse_as_blocks(Plaintext, 16)
    PlaintextCharacter = PlaintextBlocks[TargetBlock][TargetIndex]

    MaliciousCharacter = XOR(
        XOR(DesiredCharacter, PlaintextCharacter), FlipCharacter)
    CipherBlocks[FlipBlock] = (CipherBlocks[FlipBlock][:TargetIndex]
                               + MaliciousCharacter
                               + CipherBlocks[FlipBlock][TargetIndex + 1:])

    MaliciousCiphertext = ''
    for n in range(len(CipherBlocks)):
        MaliciousCiphertext += CipherBlocks[n]
    return MaliciousCiphertext


def MakeAdminCiphertext(EncryptionOracle):
    
    DesiredOutputString = ';admin=true;'
    DummyString = 'a' * 32
    Ciphertext = TargetCiphertext(DummyString, EncryptionOracle)
    Plaintext = EncryptionOracle.decrypt(Ciphertext)
    for x in range(len(DesiredOutputString)):
        Ciphertext = BitFlip(
            Ciphertext, 2, x,
            DesiredOutputString[x],
            Plaintext)
    return Ciphertext


    

