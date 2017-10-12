from Crypto.Cipher import AES

def parse_as_blocks(ciphertxt, block_length):
  num_blocks = len(ciphertxt) / (block_length)
  blocks = []
  for x in range(num_blocks):
    blocks.append(ciphertxt[:block_length])
    ciphertxt = ciphertxt[block_length:]
  return blocks
  
def aes128_decrypt(ciphertxt, key):
  ciphertxt = ciphertxt.decode('base64')
  obj = AES.new(key, AES.MODE_ECB)
  plaintext = ''
  blocks = parse_as_blocks(ciphertxt, 128)
  for x in blocks:
    plaintext += obj.decrypt(x)
  return plaintext

def count_repeats(ciphertxt):
  ciphertxt = ciphertxt.decode('hex')
  blocks = parse_as_blocks(ciphertxt, 16)
  repeat_dict = {}
  for x in blocks:
    if x in repeat_dict.keys():
      repeat_dict[x] += 1
    else:
      repeat_dict[x] = 0
  repeats = sum(repeat_dict[x] for x in repeat_dict.keys())
  return float(repeats) / len(blocks)

def aes128_encrypt(plaintxt, key):
  #plaintxt = plaintxt.decode('base64')
  obj = AES.new(key, AES.MODE_ECB)
  ciphertxt = obj.encrypt(plaintxt)
  return ciphertxt
