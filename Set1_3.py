import char_operations
import string
import array
from itertools import izip, cycle

#First we set up a dict with form [character : frequency]

#list of frequencies
frequencies = """0.0651738 0.0124248 0.0217339 0.0349835 0.1041442 0.0197881 0.0158610 0.0492888 0.0558094 0.0009033 0.0050529 0.0331490 0.0202124 0.0564513 0.0596302 0.0137645 0.0008606 0.0497563 0.0515760 0.0729357 0.0225134 0.0082903 0.0171272 0.0013692 0.0145984 0.0007836 0.1918182"""
frequencies = frequencies.split()

#list of characters of alphabet including space
alphabet = string.ascii_lowercase
characters = [alphabet[i] for i in range(len(alphabet))]
characters.append(' ')

#now we make our dict
frequency = { }
for i in range(len(characters)):
  frequency[characters[i]] = float(frequencies[i])
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#Need a list of ASCII characters.
chars = list(string.printable)



#Set up a way to score plaintexts for closeness to actual language


#letter_frequency is a dict of form [character : observed frequency]
def least_squares(letter_frequency):
  return sum((letter_frequency[x] - frequency[x])**2 for x in letter_frequency.keys())

  
def score(text):
  #first we ignore all upper case characters
  text = text.lower()

  #total counts all valid characters in the text
  total = sum(text.count(x) for x in characters)

  #set up letter_frequency dict to pass to least squares
  letter_frequency = {}

  if total != 0:
    for x in frequency.keys():
      letter_frequency[x] = float(text.count(x)) / total
    return least_squares(letter_frequency)

  #if there are no valid characters give high score since its probably wrong
  else:
    return 100000
#////////////////////////////////////////////////////////////////



#determines most likely keys for cipher text xor'd with a single repeating character
def getkey_xor(ciphertext):
  #start with a dict with freq scores of xord texts
  scores = {}
  
  for k in chars:
    #text is the decoded result of xoring ciphertext with character k
    text = char_operations.repeated_xor(k, ciphertext).decode('hex')
    scores[k] = score(text)
    
  #answer = min(scores, key=scores.get)

  sort = sorted(scores.items(), key = lambda s: s[1])
  #returns a list with tuples (character, score) ordered by increasing score
  return sort[:3]


#test = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
#print getkey_xor(test)
