from RSA_math import gcd, modinv


class CRT:

    ## An implementation of the Chinese remainder theorem. Given
    ## data of congruences modulo pairwise coprime integers,
    ## computes element mod their product from isomorphism furnished by CRT.
    ##
    ## Reverse direction is trival: Given element mod N = pq, to get
    ## corresponding element modulo the direct product of factors is to take
    ## residues.

    @staticmethod
    def makepairs(arglist):

        pairs = []
        for i in range(len(arglist) - 1):
            for j in range(i + 1, len(arglist)):
                arg1 = arglist[i]
                arg2 = arglist[j]
                pair = (arg1, arg2)
                pairs.append(pair)
        return pairs


    @staticmethod
    def coprime(integers):

        pairs = CRT.makepairs(integers)
        for pair in pairs:
            if gcd(pair[0], pair[1]) > 1:
                return False
        return True


    @staticmethod
    def product(moduli):

        output = 1
        for modulus in moduli:
            output *= modulus
        return output


    @staticmethod
    def term(residue, smallmod, bigmod):

        factor1 = bigmod/smallmod
        factor2 = modinv(factor1, smallmod)
        return (residue * factor1 * factor2) % bigmod
        
    @staticmethod
    def compute_elt(congruences):

        integers = [x[0] for x in congruences]
        moduli = [x[1] for x in congruences]

        if CRT.coprime(moduli):

            modulus = CRT.product(moduli)
            output = 0
            
            for i in range(len(congruences)):
                residue = integers[i]
                n = moduli[i]
                output += CRT.term(residue, n, modulus)
                output %= modulus
                
            return output

        else:
            print 'These moduli are not coprime. CRT does not apply.'





    
        
    
    
