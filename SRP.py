## Implementation of Secure Remote Password protocol.

import random
import sha
import hmac
import hashlib

from RSA_primes import get_prime
from protocol import Party, Protocol, Eve
from ModularExponentiation import square_and_multiply as modexp


## For purposes of this problem these parameters are fixed. We can
## imagine things like g, prime, and k are pre-negotiated via some other
## protocol.


nist_prime = get_prime()
g = 2
k = 3
email = 'bob@gmail.com'
password = 'password'


class SRP_Party(Party):


    def __init__(self, name):
        
        Party.__init__(self, name)
        self.prime = nist_prime
        self.generator = g
        self.k = k
        self.email = email
        self.password = password

    
    def gen_keys(self):
        
        self.sk = self.private_key()
        self.pk = self.public_key()

        
    def private_key(self):

        sk = random.randint(2, self.prime - 1)
        return sk


    def public_key(self):

        pk = modexp(self.generator, self.sk, self.prime)
        return pk

    
    ## These three get functions all should output strings.
    
    def get_A(self):

        pass
    

    def get_B(self):
        
        pass
    

    def get_salt(self):

        pass


    def compute_x(self):
        
        salt = self.get_salt()
        xH = sha.new(salt + self.password).hexdigest()
        x = int(xH, 16)
        return x
    
    
    def compute_v(self):

        x = self.compute_x()
        v = modexp(self.generator, x, self.prime)
        return v
    

    def compute_u(self):

        A = self.get_A()
        B = self.get_B()
        uH = sha.new(A + B).hexdigest()
        u = int(uH, 16)
        return u


    def compute_S(self):

        pass


    def compute_K(self):

        S = self.compute_S()
        K = sha.new(str(S)).hexdigest()
        return K


    def hmac_salt(self):

        key = self.compute_K()
        salt = self.get_salt()
        return hmac.new(key, salt, hashlib.sha256).digest()
    

class Client(SRP_Party):


    def __init__(self):
        
        SRP_Party.__init__(self, 'Client')
        self.gen_keys()
        

    def write_message(self):

        if len(self.received) == 0:
            return (self.email, self.pk)

        else:
            self.finished = True
            return self.hmac_salt()


    def get_salt(self):

        ## Wants a string
        return str(self.received[0][0])


    def get_A(self):

        return str(self.sent[0][1])


    def get_B(self):

        return str(self.received[0][1])


    def compute_S(self):

        B = int(self.get_B())
        a = self.sk
        u = self.compute_u()
        v = self.compute_v()
        x = self.compute_x()

        base = (B - k * v) % self.prime
        exponent = (a + u * x)
        return modexp(base, exponent, self.prime)



class Server(SRP_Party):

    
    def __init__(self):

        SRP_Party.__init__(self, 'Server')
        self.salt = random.randrange(2**16)
        self.gen_keys()
        self.v = self.compute_v()
        self.key = None


    def write_message(self):
        
        if len(self.sent) == 0:
            return self.first_message()

        else:
            return self.second_message()
        

    def first_message(self):

        B = (self.k * self.v + self.pk) % self.prime
        return (self.salt, B)


    def second_message(self):

        self.finished = True
        
        if self.validate():
            return 'OK!'

        else:
            return 'Whoops. Something went wrong.'


    def get_A(self):

        return str(self.received[0][1])


    def get_B(self):

        return str(self.sent[0][1])


    def get_salt(self):
        
        return str(self.salt)
    

    def compute_S(self):

        A = int(self.get_A())
        v = self.compute_v()
        u = self.compute_u()
        b = self.sk

        v_to_u = modexp(v, u, self.prime)
        base = (A * v_to_u) % self.prime
        exponent = b
        S = modexp(base, exponent, self.prime)
        return S

 
    def validate(self):

        return self.received[1] == self.hmac_salt()

    
        
class SRP(Protocol):

    def __init__(self):
        Protocol.__init__(self, Client(), Server())

s = SRP()
s.run()



def exponent_test(a,b):

    x = modexp(2, a, nist_prime)
    y = modexp(x, b, nist_prime)
    z = modexp(2, a * b, nist_prime)
    return y == z


## This is me being suspicious theres a problem with my modular exponentiation.
##p = nist_prime
##
##for x in range(200):
##    for y in range(x):
##        if not exponent_test(x, y):
##            print 'Problem'

