from random import randrange
from hashlib import sha256
import random
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime
#=======Math functions============
def gcd(a, b):
   while a != 0:
      a, b = b % a, a
   return b

def findModInverse(a, m):
   if gcd(a, m) != 1:
      return None
   u1, u2, u3 = 1, 0, a
   v1, v2, v3 = 0, 1, m
   
   while v3 != 0:
      q = u3 // v3
      v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
   return u1 % m
def is_coprime(x, y):
    return gcd(x, y) == 1

def phi_func(x):
    if x == 1:
        return 1
    else:
        n = [y for y in range(1,x) if is_coprime(x,y)]
        return len(n)
def rabinMiller(num):
   s = num - 1
   t = 0
   
   while s % 2 == 0:
      s = s // 2
      t += 1
   for trials in range(5):
      a = random.randrange(2, num - 1)
      v = pow(a, s, num)
      if v != 1:
         i = 0
         while v != (num - 1):
            if i == t - 1:
               return False
            else:
               i = i + 1
               v = (v ** 2) % num
      return True
def isPrime(num):
   if (num < 2):
      return False
   lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
   67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
   157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 
   251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,317, 331, 337, 347, 349, 
   353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 
   457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 
   571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 
   673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
   797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 
   911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
	
   if num in lowPrimes:
      return True
   for prime in lowPrimes:
      if (num % prime == 0):
         return False
   return rabinMiller(num)
def generateLargePrime(keysize = 1024):
   while True:
      num = random.randrange(2**(keysize-1), 2**(keysize))
      if isPrime(num):
         return num
def listToString(arr):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for index in range(len(arr)-1):  
        str1 +=str(arr[index])  +","
    str1+=str(arr[index+1])
    return str1
def StringToList(str1):  
    print(str1)
    # initialize an empty string 
    
    arr1=str1.split(',')
    arr=[0]*len(arr1)
    print(arr1)
    # traverse in the string   
    for index in range(len(arr1)):  
        arr[index]=int(arr1[index])
        
    # return string   
    return arr  
def checkEquals(arr1,arr2):
    if len(arr1)!=len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i]!=arr2[i]:
            return False
    return True
#=======Math functions-End==========

#=======RSA functions============

def generate_p_q_for_RSA(size):
   print('Generating p prime...')
   p = generateLargePrime(size)
   print('Generating q prime...')
   q = generateLargePrime(size)
   return p,q
def generate_public_params_RSA(sizePQ,keySize):
    p, q = generate_p_q_for_RSA(sizePQ)
    n=p*q
    pi=(p-1)*(q-1)
    while True:
      e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
      if gcd(e, pi) == 1:
         break
    return e,n
def generate_private_params_RSA(e,n):
    d = findModInverse(e, phi_func(n))
    return d
def RSAEncrypt(Key, n, text):
    cipher = [((num) ** Key) % n for num in text]
    return cipher 
def RSADecrypt(Key, n, cipher):
    decryption = [num ** Key % n for num in cipher]
    return decryption



#=======Digital Signature functions============
#creates keys p,q
def generate_p_q(L, N):
    g = N  # g >= 160
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # generate q
        while True:
            s = xmpz(randrange(1, 2 ** (g)))
            a = sha256(to_binary(s)).hexdigest()
            zz = xmpz((s + 1) % (2 ** g))
            z = sha256(to_binary(zz)).hexdigest()
            U = int(a, 16) ^ int(z, 16)
            mask = 2 ** (N - 1) + 1
            q = U | mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            V = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = sha256(to_binary(arg)).hexdigest()
                V.append(int(zzv, 16))
            W = 0
            for qq in range(0, n):
                W += V[qq] * 2 ** (160 * qq)
            W += (V[n] % 2 ** b) * 2 ** (160 * n)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)
            p = X - c + 1  # p = X - (c - 1)
            if p >= 2 ** (L - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1

#calculate g with given p,q(g=h^((p-1)/q))
def generate_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g

#calculate keys x,y with given g,q,p
def generate_keys(g, p, q):
    x = randrange(2, q)  # x < q
    y = powmod(g, x, p)
    return x, y

#generate p,q,g with given sizes L,N
def generate_params_digital_signature(L, N):
    p, q = generate_p_q(L, N)
    g = generate_g(p, q)
    return p, q, g


 

#create digital signature with given message and keys
def sign(M, p, q, g, x):
    if not validate_params(p, q, g):
        raise Exception("Invalid params")
    while True:
        k = randrange(2, q)  # k < q
        r = powmod(g, k, p) % q
        #calculate hash value of message as number
        m = int(sha256(M).hexdigest(), 16)
        try:
            s = (invert(k, q) * (m + x * r)) % q
            return r, s
        except ZeroDivisionError:
            pass

#verify digital signature 
def verify(M, r, s, p, q, g, y):
    if not validate_params(p, q, g):
        raise Exception("Invalid params")
    if not validate_sign(r, s, q):
        return False
    try:
        w = invert(s, q)
    except ZeroDivisionError:
        return False
    m = int(sha256(M).hexdigest(), 16)
    u1 = (m * w) % q
    u2 = (r * w) % q
    # v = ((g ** u1 * y ** u2) % p) % q
    v = (powmod(g, u1, p) * powmod(y, u2, p)) % p % q
    if v == r:
        return True
    return False
def validate_params1(p, q):
     if is_prime(p) and is_prime(q):
        return True
     return False
def validate_params2(p, q,g):
    if powmod(g, q, p) == 1 or g > 1 and (p - 1) % q:
        return True
    return False
#validate that the given p,q,g are legal
def validate_params(p, q, g):
    return validate_params1(p, q) and validate_params2(p, q, g)
    

#validate that created signature is legal
def validate_sign(r, s, q):
    if r < 0 and r > q:
        return False
    if s < 0 and s > q:
        return False
    return True
#=======Digital Signature functions-end============

