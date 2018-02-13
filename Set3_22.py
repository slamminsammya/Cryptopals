from Set3_21 import MT19937
import time
import random

def nick_cave_andthe_bad_seed():
    delay = random.randrange(40, 1000)
    ## time.sleep(delay)
    seed = int(time.time())
    delay_2 = random.randrange(40,1000)
    ## time.sleep(delay_2)
    total_delay = float(delay + delay_2) / 60
    print 'Pretend you just waited around', total_delay, 'minutes.'
    
    return MT19937(seed).extract_number()

s = nick_cave_andthe_bad_seed()

## Cracking is trivial if you have even week long window in which
## the seeding could have occurred. Exhaustive search! In particular,
## 600000 seedings takes about fifteen minutes, which is a week's worth
## of possible seedings. 


for n in range(7):
    start = time.time()
    for i in range(10**n):
        t = MT19937(i).extract_number()
    print 'Took', time.time() - start, 'seconds to try', 10**n, 'seeds.'
