## Takes plaintext, makes it into blocks, and pads those blocks.


class BlockParser(object):


    def __init__(self, blocksize = 16, padding = False):
        
        self.blocksize = blocksize
        self.padding = padding


    def prepare_blocks(self, data):

        if self.padding:
            data = self.pad(data)
        return self.blockify(data)
        

    def blockify(self, data):

        ## Wants string input.

        blocks = []
        current_startindex = 0
        current_data = data
        
        while len(current_data) > 0:
            block = self.getblock(current_data)
            blocks.append(block)
            current_startindex += self.blocksize
            current_data = data[current_startindex:]

        return blocks


    def unblockify(self, blocks):

        ## Wants string input.

        output = ''
        for block in blocks:
            output = output + block

        return output


    def process_blocks(self, blocks):

        text = self.unblockify(blocks)
        if self.padding:
            text = self.strip_pad(text)
        return text        
        

    def getblock(self, data):

        if len(data) < self.blocksize:
            return data

        else:
            return data[:self.blocksize]


    def pad(self, text):

        pad_length = (self.blocksize -
                      (len(text) % self.blocksize)) % self.blocksize
        pad_character = chr(pad_length)
        padded_text = text + pad_length * pad_character
        
        return padded_text

    
    def strip_pad(self, text):

        pad_character = text[-1]
        if ord(pad_character) in range(self.blocksize):
            true_length = len(text) - ord(pad_character)

        else:
            true_length = len(text)

        return text[:true_length]

    
            


