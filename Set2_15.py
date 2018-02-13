## PKCS#7 padding validation

class PaddingError(ValueError):
    def __init__(self,arg):
        ValueError.__init__(self,arg)

class BadTextLength(PaddingError):
    def __init__(self,arg):
        PaddingError.__init__(self,arg)
        

class NoPadding(PaddingError):
    def __init__(self,arg):
        PaddingError.__init__(self,arg)
        

def verify_padding(string):
    if len(string) % 16 != 0:
        raise BadTextLength("The text is the wrong length.")
    else:
        padding_byte = string[-1]
        pad = ord(padding_byte)
        if pad in range(1,17):
            for n in range(- pad, 0):
                if string[n] != padding_byte:
                    return False
            return True

        else:
            raise PaddingError("The text is not padded.")


def strip_pad(string):
    try:
        if verify_padding(string):
            padding_byte = string[-1]
            pad = ord(padding_byte)
            return string[:-pad]
    except ValueError:
        return string

