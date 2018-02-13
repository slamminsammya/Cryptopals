import SHA1
import random

class KeyedMAC:

    def __init__(self):
        self.key = ''.join(chr(random.randrange(256))
                           for x in range(random.randrange(32)))

    def sign(self, message):
        sha = SHA1.SHA1()
        message = self.key + message
        sha.update(message)
        return sha.hexdigest()

## Insert how to get the keylength here. I am lazy but its simple.
## Just need to copy the function within SHA1 that pads a given
## message until you get one that has the right padding.

def SHA_padding(stream):
    
    length = len(stream)
    long_num_relatedto_length = hex(length * 8)[2:].rjust(16, '0')
    some_list = [int(long_num_relatedto_length[i : i + 2], 16)
                 for i in range(0, 16, 2)]
    some_number = (56 - length) % 64
    
    if some_number == 0:
        some_number = 64

    if isinstance(stream, str):
        stream += chr(0b10000000)
        stream += chr(0) * (some_number - 1)
        for numbers in some_list:
            stream += chr(numbers)

    elif isinstance(stream, bytes):
        stream += bytes([0b10000000])
        stream += bytes(some_number - 1)
        stream += bytes(some_list)

    return stream



def get_key_length(key_MAC):
    
    for predicted_length in range(1,32):
        padding_guess = predicted_padding(predicted_length)
        print actualSig_equals_predictedSig(padding_guess, key_MAC)

        
def actualSig_equals_predictedSig(predicted_padding, key_MAC):

    sig_1 = key_MAC.sign('')
    sig_2 = key_MAC.sign(predicted_padding)
    return sig_1 == sig_2
        
def predicted_padding(predicted_keylength):
    
    dummy_message = 'a' * predicted_keylength
    predicted_padding = SHA_padding(dummy_message)[predicted_keylength:]
    return predicted_padding

a = KeyedMAC()
get_key_length(a)

def get_SHA_state(signature):
    
    chunks = break_sig_into_chunks(signature)
    state = convert_the_chunks(chunks)
    
    return state

def break_sig_into_chunks(signature):
    
    signature = str(signature)
    chunk_indices = [0] + determine_chunk_endings(signature)
    chunks = []
    for i in range(5):
        chunk = signature[chunk_indices[i] : chunk_indices[i + 1]]
        chunks.append(chunk)
    return chunks

def convert_the_chunks(chunks):
    
    for i in range(5):
        chunks[i] = convert_chunk_to_hex(chunks[i])
    return chunks

def convert_chunk_to_hex(chunk):
    
        chunk = chunk_to_string(chunk)
        chunk = chunk_to_hex(chunk)
        return chunk
    
def chunk_to_string(chunk):
    
    return '0x' + chunk

def chunk_to_hex(chunk):

    if chunk[-1] == 'L':
        return long(chunk, 16)
    else:
        return int(chunk, 16)

def determine_chunk_endings(string):
    
    chunk_beginning = 0
    endings = []
    final_index = len(string) - 1
    for i in range(5):
        if final_index < chunk_beginning + 8:
            chunk_ending = chunk_beginning + 8
        else:
            chunk_ending = (chunk_beginning
                            + 8
                            + (string[chunk_beginning + 8] == 'L'))
        chunk_beginning = chunk_ending
        endings.append(chunk_ending)
    return endings

########################################################################

def create_SHA_with_state(state):

    sha1_instance = SHA1.SHA1()
    sha1_instance.H = state
    return sha1_instance






##for n in range(50):
##    s = SHA1.SHA1()
##    test_vector = ''.join(chr(random.randrange(128)) for n in range(5))
##    signature = s.hexdigest()
##    print s.H == get_SHA_state(signature)
##       
