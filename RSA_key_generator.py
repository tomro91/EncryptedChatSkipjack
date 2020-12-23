
import random, sys, os, rabinMiller, cryptoMath


def generateKey(keySize):
   # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
   print('Generating p prime...')
   p = rabinMiller.generateLargePrime(keySize)
   print('Generating q prime...')
   q = rabinMiller.generateLargePrime(keySize)
   n = p * q
	
   # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
   print('Generating e that is relatively prime to (p-1)*(q-1)...')
   while True:
      e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
      if cryptoMath.gcd(e, (p - 1) * (q - 1)) == 1:
         break
   
   # Step 3: Calculate d, the mod inverse of e.
   print('Calculating d that is mod inverse of e...')
   d = cryptoMath.findModInverse(e, (p - 1) * (q - 1))
   publicKey = (n, e)
   privateKey = (n, d)
   print('Public key:', publicKey)
   print('Private key:', privateKey)
   return (publicKey, privateKey)

def makeKeyFiles(keySize):
   # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' 
   #  (where x is the value in name) with the the n,e and d,e integers written in them,
   # delimited by a comma.
  
   publicKey, privateKey,n = generateKey(keySize)
   print()
   print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1])))) 
   
   print()
   print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
   print()
   print(str(n))
   
   
   
def RSAdecrypt(Key, number, cipher):
    decryption = [num ** Key % number for num in cipher]
    return decryption

def RSAencrypt(Key, number, text):
    cipher = [((num) ** Key) % number for num in text]
    return cipher   
    
  # convert the text to a string with the ascii hex value of the word

def textToHexInt(text):
        hex_text = list(text)
        plain_text = "0x"
        for i in range(len(hex_text)):
            hex_text[i] = hex(ord(hex_text[i]))[2:]
            plain_text += hex_text[i]
        hex_int = int(plain_text, 16)
    
        return hex_int
    
    
    # convert a hexadecimal int array to a string
def hexIntToText(hexInt):
        encNum = str(hexInt)
        text = ""
        tempText = ""
        i = 2
        print(hexInt)
        while i < (len(encNum)-1):
            tempText += encNum[i]
            tempText += encNum[i+1]
            text += chr(int(tempText, 16))
            tempText = ""
            i += 2
        text.join(text)
        return text
    
def partPlaintext(text):
        print("partPlaintext")
        x = 8
        ptPart = [text[y - x:y] for y in range(x, len(text) + x, x)]
        print(ptPart)
    
        return ptPart
    
def partCiphertext(text):
        print("partCiphertext")
        ctTemp = text.split("0x")
        print(ctTemp)
        ctPart = []
        for i in range(1, len(ctTemp)):
            ctPart.append("0x" + ctTemp[i])
        print(ctPart)
        return ctPart



       

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   