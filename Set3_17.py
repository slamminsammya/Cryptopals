import random
import math
import string
import Set2_16
import Set2_15
import Set1_7
import time


class CBC_PaddingOracle(object):
    def __init__(self):
        self.CBC_Oracle = Set2_16.EncryptionOracle()
        self.IV = self.CBC_Oracle.IV

    def decrypt(self, Ciphertext):
        return self.CBC_Oracle.decrypt(Ciphertext)

    def RandomEncryption(self):
        randint = random.randrange(10)
        strings = '''MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'''.split('\n')
        RandomString = strings[randint]
        Ciphertext = self.CBC_Oracle.encrypt(RandomString)
        return Ciphertext

    
    
    def PaddingOracle(self, Ciphertext):
        Plaintext = self.decrypt(Ciphertext)
        try:
            return Set2_15.verify_padding(Plaintext)
        except Set2_15.PaddingError:
            raise ValueError

a = CBC_PaddingOracle()


        
def Replace(Text, index, newcharacter):
    if index == -1:
        return Text[:-1] + newcharacter
    else:
        return Text[:index] + newcharacter + Text[index + 1:]

def Prepend(Text, prependage):
    return prependage + Text


def XOR(a,b):
    return Set2_16.XOR(a,b)
        

def PrepareMaliciousBlock(DesiredPaddingCharacter, MutableBlock, KnownPlaintext):
    ### This takes the ciphertext block we want to mess with and, for padding character
    ### j, alters the last j-1 characters of the ciphertext block so that upon
    ### decryption the last j-1 characters of the plaintext become character j.
    
    NumSteps = ord(DesiredPaddingCharacter)
    MaliciousBlock = MutableBlock[:]
    
    for j in range(NumSteps - 1):
        index = - j - 1
        intermediateCharacter = XOR(KnownPlaintext[index], DesiredPaddingCharacter)
        NewCharacter = XOR(intermediateCharacter, MutableBlock[index])
        MaliciousBlock = Replace(MaliciousBlock, index, NewCharacter)
        
    return MaliciousBlock

def PickRemoveRandomCharacter(ListofCharacters):
    ### For a list, picks a random element and discards it.
    Range = len(ListofCharacters)
    RandomIndex = random.randrange(Range)
    RandomCharacter = ListofCharacters[RandomIndex]
    del ListofCharacters[RandomIndex]
    return RandomCharacter

class NoValidCharacter(ValueError):
    def __init__(self):
        ValueError.__init__(self)

def FindPlaintextCharacter(i, Ciphertext, PaddingOracle):
    ### Takes a ciphertext and alters the ith last character of the 
    ### second to last block with a randomly chosen character until
    ### the decrypted thing has valid padding. If this does not occur 
    ### throws an exception. Note that always assumes the block of
    ### ciphertext we change is the second to last.
    
    PossibleCharacters = [chr(x) for x in range(256)]
    OriginalCharacter = Ciphertext[-i - 16]
    if i == 1:
        PossibleCharacters.remove(OriginalCharacter)
        
    while len(PossibleCharacters)> 0:
        RandomCharacter = PickRemoveRandomCharacter(PossibleCharacters)
        MaliciousCiphertext = Replace(Ciphertext, -i - 16, RandomCharacter)
        try:
            if PaddingOracle.PaddingOracle(MaliciousCiphertext):
                intermediate_step  = XOR(RandomCharacter, OriginalCharacter)
                return XOR(chr(i), intermediate_step)
        except ValueError:
            pass
    if len(PossibleCharacters)== 0:
        raise NoValidCharacter


def PaddingOracle_Attack(Ciphertext, PaddingOracle):

    CipherBlocks = Set1_7.parse_as_blocks(Ciphertext, 16)
    Plaintext = ''
    for i in range(len(CipherBlocks) - 1):
        TargetBlock = CipherBlocks[-i - 1]
        MutableBlock = CipherBlocks[-i - 2]
        DecryptedBlock = DecipherBlock(MutableBlock, TargetBlock, PaddingOracle)
        Plaintext = Prepend(Plaintext, DecryptedBlock)

    ### Special Handling for final block.
    MutableBlock = PaddingOracle.IV
    TargetBlock = CipherBlocks[0]
    DecryptedBlock = DecipherBlock(MutableBlock, TargetBlock, PaddingOracle)
    Plaintext = Prepend(Plaintext, DecryptedBlock)

    return Plaintext
    

def DecipherBlock(MutableBlock, TargetBlock, PaddingOracle):
    DecryptedBlock = ''
    try:
        for j in range(16):
            index = j + 1
            DesiredPaddingCharacter = chr(index)
            MaliciousBlock = PrepareMaliciousBlock(DesiredPaddingCharacter, MutableBlock, DecryptedBlock)
            DecryptedCharacter = FindPlaintextCharacter(index, MaliciousBlock + TargetBlock, PaddingOracle)
            DecryptedBlock = Prepend(DecryptedBlock, DecryptedCharacter)
        return DecryptedBlock
            
    except NoValidCharacter:
        print 'We made a bad choice. Trying again.'
        return DecipherBlock(MutableBlock, TargetBlock, PaddingOracle)


##correct = 0
##start = time.time()
##for x in range(50):
##    c = a.RandomEncryption()
##    b = PaddingOracle_Attack(c,a)
##    if b == a.decrypt(c):
##        correct += 1
##print correct
##print '50 tries took', time.time() - start, 'seconds.'
    
            
        
