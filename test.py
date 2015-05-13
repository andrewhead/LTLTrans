import math

def thing(n, lbd = math.e):
    p_sum = 0.0
    for x in range(int(math.floor(n/lbd)),n + 1):
        p_sum += 1/float(x)
    print p_sum


        
