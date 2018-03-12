### This abstracts a communication protocol involving two parties: Alice, Bob,
### as well as an adversary, Eve, who may either be passive (mere evesdropping)
### or active (corrupting or altering data).

import sha
from Crypto.Cipher import AES

class Channel(object):

    def __init__(self):
        
        self.current_message = None


    def get_message(self, message):
        
        self.current_message = message


class Party(object):


    def __init__(self, name = 'Nobody'):
        
        self.sent = []
        self.received = []
        self.finished = False
        self.name = name
        self.cipher = AES.new


    def __repr__(self):
        return self.name


    def write_message(self):
        pass


    def send_message(self, channel):

        message = self.write_message()
        self.sent.append(message)
        channel.get_message(message)
        if type(message) == long:
            printed = hex(message)

        else:
            printed = message
            
        print self, 'sent', printed


    def receive_message(self, channel):
        
        message = channel.current_message
        self.received.append(message)
        if type(message) == long:
            printed = hex(message)

        else:
            printed = message
            
        print self, 'received', printed

### Eve class has an attack method that will
### vary depending on the mode of attack. Simply passive eavesdropping
### means the attack is simply receiving the message. Here you might pass
### bad parameters, alter some or all of the message, whatever you want!

class Eve(Party):

    def __init__(self):
        Party.__init__(self, 'Eve')

    def eavesdrop(self, channel):
        self.receive_message(channel)

    def alter_message(self, channel):
        pass
        
    def attack(self, channel):
        self.eavesdrop(channel)
        self.alter_message(channel)


class Protocol(object):

## We assume in a protocol Alice and Eve alternate exchanging messages.

    def __init__(self, alice, bob, eve = Eve()):
        self.alice = alice
        self.bob = bob
        self.eve = eve
        self.channel = Channel()

    def send(self, sender, recipient):

        ## 1) The sender puts the message in the channel.
        sender.send_message(self.channel)

        ## 2) Eve gets to perform an attack while the message is in transit.
        self.eve.attack(self.channel)

        ## 3) The recipient receives the (possibly altered) message.
        recipient.receive_message(self.channel)


    def exchange(self):

        self.send(self.alice, self.bob)
        self.send(self.bob, self.alice)


    def protocol_finished(self):
        return self.alice.finished and self.bob.finished


    def run(self):
        while self.protocol_finished() == False:
            self.exchange()

p = Protocol(Party('Alice'), Party('Bob'), Eve())

    

    

    

    

    
