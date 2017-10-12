import array
import string
from itertools import izip, cycle

def b64_to_hex(string):
  pad = len(string) % 4
  if string[-1] == '=':
    pad = (pad + 1) % 4
  if pad == 3: 
    string += 'A=='
  elif pad == 1 or pad == 2:
    string += b'=' * pad
  return string.decode('base64').encode('hex')
  
def pad_hex(string):
  if len(string) % 2 == 1:
    string += '0'
  return string
  
  
def hexto64(s):
  s = s.decode('hex').encode("base64")
  return s
  
def repeated_xor(key, ciphertext):
  return xor(key.encode('hex'),ciphertext)

  
def xor(p,q):
  #input must be in hex
  p = p.decode('hex')
  q = q.decode('hex')
  if len(q) > len(p):
    p,q = q,p
  return ''.join(chr(ord(a)^ord(b))for a,b in izip(p, cycle(q))).encode('hex')
