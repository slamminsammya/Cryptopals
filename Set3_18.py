from Set3_17 import XOR
from Crypto.Cipher import AES
from Set1_7 import parse_as_blocks

import Set1_3
import char_operations

import math
import random
import string
from itertools import izip, cycle



class CTR_Cipher(object):


    def __init__(self, nonce, key = None):
        
        if key == None:
            key = self.random_key()
            
        self.key = key
        self.nonce = nonce
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def random_key(self):
        
        random_key = ''.join(chr(random.randrange(256)) for n in range(16))
        return random_key

    def keystream(self, counter):
        
        CTR = chr(counter) + 7 * chr(0)
        EncryptMe = self.nonce + CTR
        Keystream = self.cipher.encrypt(EncryptMe)
        return Keystream

    def DifferentLengthXOR(self, plaintext_1, plaintext_2):
        
        length_1 = len(plaintext_1)
        length_2 = len(plaintext_2)
        length = min(length_1, length_2)
        plaintext_1, plaintext_2 = plaintext_1[:length], plaintext_2[:length]
        return XOR(plaintext_1, plaintext_2)

    def BlockParser(self, text, blocksize = None):
        
        if blocksize is None:
            blocksize = 16
        
        blocks = []
        length = len(text)
        num_blocks = int(math.ceil(length / blocksize))
        
        for i in range(num_blocks):
            CurrentBlock = text[i * blocksize : (i + 1) * blocksize]
            blocks.append(CurrentBlock)
            
        return blocks
        

    def encrypt(self, plaintext):
        ## Operate on raw bytes.
        ## Decrypt is same as encrypt.
        PlaintextBlocks = self.BlockParser(plaintext)
        num_blocks = len(PlaintextBlocks)
        Ciphertext = ''
        
        for counter in range(num_blocks):
            Keystream = self.keystream(counter)
            CipherBlock = self.DifferentLengthXOR(Keystream, PlaintextBlocks[counter])
            Ciphertext = Ciphertext + CipherBlock
        return Ciphertext


##key = 'YELLOW SUBMARINE'
##nonce = chr(0)*8
##a = CTR_Cipher(key, nonce)
##text = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
##text = text.decode('base64')
    
b = CTR_Cipher(chr(0)* 8)

ciphertexts = '''SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==
Q29taW5nIHdpdGggdml2aWQgZmFjZXM=
RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==
RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=
SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk
T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==
T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=
UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==
QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=
T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl
VG8gcGxlYXNlIGEgY29tcGFuaW9u
QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==
QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=
QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==
QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=
QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=
VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==
SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==
SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==
VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==
V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==
V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==
U2hlIHJvZGUgdG8gaGFycmllcnM/
VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=
QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=
VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=
V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=
SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==
U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==
U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=
VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==
QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu
SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=
VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs
WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=
SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0
SW4gdGhlIGNhc3VhbCBjb21lZHk7
SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=
VHJhbnNmb3JtZWQgdXR0ZXJseTo=
QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4='''.split('\n')

ciphertexts = [b.encrypt(x.decode('base64')) for x in ciphertexts]


columns = []
for j in range(16):
    columns_j = [ciphertexts[x][j] for x in range(len(ciphertexts))]
    columns.append(columns_j)
    
def most_common_letter(LetterList):
    LetterCount = {}
    for x in LetterList:
        LetterCount[x] = LetterList.count(x)

    SortedByFrequency = sorted(LetterCount.keys(), key = lambda x: LetterCount[x])
    return SortedByFrequency[0]


def common_truncation(ciphertexts):
    MinimumLength = len(ciphertexts[0])
    for i in range(len(ciphertexts)):
        if len(ciphertexts[i]) < MinimumLength:
            MinimumLength = len(ciphertexts[i])

    for x in range(len(ciphertexts)):
        ciphertexts[x] = ciphertexts[x][:MinimumLength]

    return ciphertexts

def SortByIndex(ciphertexts):
    ### Assumes you have already truncated all ciphertexts to be common length.
    NumberOfColumns = len(ciphertexts[0])
    columns = [''] * NumberOfColumns
    for i in range(NumberOfColumns):
        for j in range(len(ciphertexts)):
            columns[i] = columns[i] + ciphertexts[j][i]
    return columns

def ScoreText(text):
    
    ### Returns closeness of a text to english based on frequency of characters.
    modified_text = text.lower()
    frequencies = {}
    for character in (string.ascii_lowercase + ' '):
        frequencies[character] = float(modified_text.count(character)) / len(modified_text)

    english_frequencies = Set1_3.frequency
    
    score = sum((frequencies[character] - english_frequencies[character]) ** 2
               for character in (string.ascii_lowercase + ' '))
    if sum(frequencies[character] for character in (string.ascii_lowercase + ' ')) < .5:
        score = 100
    return score

def DetermineXOR(text):
    
    ### Given english text XOR'd with single character, determines most likely
    ### character it was XOR'd with.

    scores = {}
    for i in range(256):
        ShiftedText = ''.join(XOR(chr(i), text[j]) for j in range(len(text)))
        scores[chr(i)] = ScoreText(ShiftedText)

    return min(scores, key = scores.get)


def DetermineKeystream(ciphertexts):
    
    ### Given collection of ciphertexts, guesses Keystream they were XORd against

    ciphertexts = common_truncation(ciphertexts)
    columns = SortByIndex(ciphertexts)
    keystream = ''
    for text in columns:
        keystream = keystream + DetermineXOR(text)
    return keystream


### Check our work
def repeated_xor(string_1, string_2):
    if len(string_1) < len(string_2):
        string_1, string_2 = string_2, string_1

    return ''.join(chr(ord(a) ^ ord(b)) for a, b in izip(string_1, cycle(string_2)))

##keystream = DetermineKeystream(ciphertexts)
##for x in ciphertexts:
##    print repeated_xor(keystream, x)
