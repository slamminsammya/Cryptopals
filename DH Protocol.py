import random
import sha
from protocol import Party as Party
from protocol import Protocol as Protocol
from protocol import Eve as Eve
from ModularExponentiation import square_and_multiply as square_and_multiply
from ModularExponentiation import modular_times as modular_times


class DH_Alice(Party):

    def __init__(self):
        Party.__init__(self, 'Alice')
        self.prime = self.get_prime()
        self.generator = self.get_generator()
        self.secret_key = self.get_secret()

    def get_prime(self):
        p = '''ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024
e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec
6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f
24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361
c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552
bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff
fffffffffffff'''
        prime = '0x'
        
        for part in p.split():
            prime += part

        return int(prime, 16)

    def get_generator(self):
        return 2

    def get_secret(self):
        return random.randint(1, self.prime - 1)

    def write_message(self):

        if len(self.sent) == 0:
            return self.write_parameters()

        else:
            self.finished = True
            return self.write_shared_key()

    def write_parameters(self):
        public_key = square_and_multiply(self.generator,
                                       self.secret_key,
                                       self.prime)
        return [self.prime, self.generator, public_key]

    def write_shared_key(self):
        
        key = self.compute_shared_secret()
        hashed_key = sha.new(str(key)).digest()[:16]
        return hashed_key
        
            
    def compute_shared_secret(self):

        bobs_public_key = self.received[0]
        return square_and_multiply(bobs_public_key,
                                   self.secret_key,
                                   self.prime)
        
    
class DH_Bob(Party):

    def __init__(self):
        Party.__init__(self, 'Bob')
        self.secret_key = 0
        self.generator = 0
        self.prime = 0

    def process_first_message(self):
        first_message = self.received[0]
        self.prime = first_message[0]
        self.generator = first_message[1]

    def generate_secret(self):
        self.process_first_message()
        self.secret_key = random.randint(1, self.prime - 1)
        

    def write_message(self):

        if len(self.sent) == 0:
            self.finished = True
            return self.write_public_key()

    def write_public_key(self):
        
        self.generate_secret()
        return square_and_multiply(self.generator,
                                       self.secret_key,
                                       self.prime)
        
    def compute_shared_secret(self):
        
        alice_public_key = self.received[1]
        return square_and_multiply(alice_public_key,
                                   self.secret_key,
                                   self.prime)





class Malicious_generator(Eve):

## This attacker alters the generator passed by Alice to Bob. If g = p, p-1, or 1
## the shared secret becomes very predictable.

    def __init__(self, malicious_generator):
        Eve.__init__(self)
        self.malicious_generator = malicious_generator
        

    def alter_message(self, channel):

        if len(self.received) == 1:
            parameters = self.received[0]
            channel.get_message(self.corrupt_parameters(parameters))

        else:
            pass

    def corrupt_parameters(self, parameters):
        
            parameters = self.received[0]
            prime = parameters[0]

            if self.malicious_generator == 'p':
                malicious_generator = 0

            elif self.malicious_generator == 'p-1':
                malicious_generator = -1

            else:
                malicious_generator = self.malicious_generator
                
            malicious_parameters = (prime, malicious_generator)
            
            return malicious_parameters
        

class Malicious_pk(Eve):
    pass
    

            

class DH_Protocol(Protocol):

    def __init__(self, attacker = Eve()):
        
        Protocol.__init__(self, DH_Alice(), DH_Bob(), attacker)
