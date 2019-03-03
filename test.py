from __init__ import *

prec = 64

%timeit pow_simple(3, 100000, 7)
%timeit pow_fast(3, 100000, 7)

ts1 = generate_prime(50, prec)
ts2 = generate_prime(100, prec)
%timeit get_arithmetic_inv(ts1, ts2)

test_prime = generate_prime(100, prec)
%timeit primality_test(test_prime, prec)

%timeit -n 10 generate_prime(100, prec)

%timeit -n 10 generate_keypair()

keypair = generate_keypair()
%timeit decrypt_message(keypair[1], encrypt_message(keypair[0], 'Hello World!'))
