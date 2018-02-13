from Set3_21 import MT19937

def temper(y):
    
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    return y


def untemper(y):
    ## First two inversions are trivially easy since they are
    ## idempotent.
    y = y ^ y >> 18
    y = y ^ y << 15 & 4022730752

    ## Now we go 7 bits at a time. y_1 has 14 correct bits.
    y_1 = y ^ y << 7 & 2636928640
    ## y_2 in turn has 21 correct bits.
    y_2 = y ^ y_1 << 7 & 2636928640
    ## y_3 has 28.
    y_3 = y ^ y_2 << 7 & 2636928640
    ## y_4 has all 32 bits hot and ready to go.
    y_4 = y ^ y_3 << 7 & 2636928640
    ## It also has a hot mess in front so we (and) with
    ## 32 bits of ones to lop off the unnecessary part.
    y = y_4 & 0xFFFFFFFF

    ## y_5 now has 22 correct bits.
    y_5 = y ^ y >> 11
    ## This has all the good bits.
    y = y ^ y_5 >> 11
    
    return y
    

## To see if it works.        
##for x in range(2**22):
##    y = temper(x)
##    z = untemper(y)
##    if z != x:
##        raise Exception("Didn't invert.")


def clone_RNG(RNG):
    ## Create a clone. Seed value is irrelevant because we will be
    ## redoing all the state values.
    clone = MT19937(0)
    for n in range(624):
        output = RNG.extract_number()
        state_value = untemper(output)
        clone.mt[n] = state_value
    return clone

