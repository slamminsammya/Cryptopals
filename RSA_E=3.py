## Implement a broadcast attack. Here we assume the public key is 3,
## in general for the attack to work if public key is e Eve requires
## e copies of the same plaintext encrypted under different moduli.

from RSA_keygen import RSA
from CRT import CRT
import math
from Converter import Converter

class RSA_Replay:

    @staticmethod
    def ctext_to_cong(plaintext):
          
        oracle = RSA()
        ctext = oracle.encrypt(plaintext)
        congruences = [(block, oracle.modulus) for block in ctext]
        return congruences

    @staticmethod
    def congruence_array(plaintext, e):

        cong_array = []
        
        for replay in range(e):
            cong_array.append(RSA_Replay.ctext_to_cong(plaintext))
            
        ## Output is the transpose of the congruences from each instance.    
        output = [ [cong_array[i][j] for i in range(len(cong_array))]
                   for j in range(len(cong_array[0]))]
        
        return output

    @staticmethod
    def translate(number):

        return Converter().num_to_str(number)


    @staticmethod
    def cuberoot(number):

        return int(round(number **(float(1)/3)))
        

    @staticmethod
    def run():

        secret_plaintext = raw_input('Type in some plaintext for us to attack.')
        crt_blocks = RSA_Replay.congruence_array(secret_plaintext, 3)
        number_blocks = []
        output = ''
        
        for block in crt_blocks:
            number_blocks.append(CRT.compute_elt(block))

        for number in number_blocks:
            number = RSA_Replay.cuberoot(number)
            
            output = output + RSA_Replay.translate(number)

        return output
    
