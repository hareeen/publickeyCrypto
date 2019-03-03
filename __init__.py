import random
import base64


def pow_simple(n, e, MOD):  # O(e)
  _mul = 1
  for _ in range(e):
    _mul *= n
    _mul %= MOD
  return _mul


def pow_fast(n, e, MOD):  # O(log e)
  _mul = n
  _res = 1
  for digit in str(bin(e))[2:][::-1]:
    if digit == '1':
      _res *= _mul
      _res %= MOD
    _mul *= _mul
    _mul %= MOD
  return _res


def pow_negone(n):
  return 1 if n % 2 == 0 else -1


def gcd(a, b):  # 유클리드 호제법
  return a if b == 0 else gcd(b, a % b)


def jacobi(a, n):  # Jacobi Symbol (n이 홀수일 때만 정의됨)
  if a == 1:
    return 1
  elif a % 2 == 0:
    # J(a*b,n)=J(a,n)*J(b,n) && J(2,n)=(-1)**((n**2-1)/8)
    return jacobi(a // 2, n) * pow_negone((n * n - 1) // 8)
  else:
    return jacobi(n % a, a) * pow_negone((a - 1) * (n - 1) // 4)  # 이차상호법칙


def primality_test(p, loops):  # Solovay-Strassen Primality Test
  for _ in range(loops):
    r = random.randint(1, p - 1)
    if not (gcd(r, p) == 1 and jacobi(r, p) % p == pow_fast(r, (p - 1) // 2, p)):
      return False
  return True


def generate_prime(digits, prec):
  while True:
    p = random.randint(10**(digits - 1), 10**digits - 1)
    if p % 2 == 1 and primality_test(p, prec):
      return p


# 잉여역수 구하기 (Extended Euclidian Algorithm)
def get_arithmetic_inv(r1, r2, s1=1, s2=0, t1=0, t2=1):
  if r1 < r2:
    r1, r2 = r2, r1
  r = r1 % r2
  q = r1 // r2
  s = s1 - s2 * q
  t = t1 - t2 * q
  return t2 if r == 0 else get_arithmetic_inv(r2, r, s2, s, t2, t)


def generate_keypair(base_digits=100, prec=64):
  err_allow = base_digits // 20

  def digits_with_err(): return random.randint(-err_allow, err_allow) + base_digits
  prime_pair = (generate_prime(digits_with_err(), prec),
                generate_prime(digits_with_err(), prec))
  n = prime_pair[0] * prime_pair[1]
  phi_n = (prime_pair[0] - 1) * (prime_pair[1] - 1)
  d = generate_prime(len(str(max(prime_pair))) +
                     random.randint(0, 4 * err_allow), prec)
  e = get_arithmetic_inv(phi_n, d) % phi_n

  return ((e, n),  # public key
          (d, n))  # private key


def apply_key(n, key):
  return pow_fast(n, key[0], key[1])


def encrypt_message(key_public, message):
  ascii_message = base64.b64encode(message.encode()).decode()
  message_number = list(map(ord, ascii_message))
  encrypted = list(
      map(lambda x: str(apply_key(x, key_public)).rjust(len(str(key_public[1])), '0'), message_number))
  return ' '.join(encrypted)


def decrypt_message(key_private, message_enc):
  decrypted = list(map(lambda x: apply_key(
      int(x), key_private), message_enc.split()))
  decrypted_chr = list(map(chr, decrypted))
  return base64.b64decode(''.join(decrypted_chr).encode()).decode()
