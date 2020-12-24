
import random, sys, os, rabinMiller, cryptoMath


def generateKey(keySize):
   # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
   print('Generating p prime...')
   p = rabinMiller.generateLargePrime(keySize)
   print(p)
   print('Generating q prime...')
   q = rabinMiller.generateLargePrime(keySize)
   print(q)
   n = p * q
	
   # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
   print('Generating e that is relatively prime to (p-1)*(q-1)...')
   while True:
      e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
      if cryptoMath.gcd(e, (p - 1) * (q - 1)) == 1:
         break
   print(e)
   # Step 3: Calculate d, the mod inverse of e.
   print('Calculating d that is mod inverse of e...')
   d = cryptoMath.findModInverse(e, (p - 1) * (q - 1))
   print(d)
   publicKey = (n, e)
   privateKey = (n, d)
   print('Public key:', publicKey)
   print('Private key:', privateKey)
   return (publicKey, privateKey)

  
   
def RSAdecrypt(Key, number, cipher):
  
    decryption = (cipher ** Key )% number
    return decryption

def RSAencrypt(Key, number, text):
       
    cipher = (text ** Key) % number 
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
        #print(hexInt)
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


'''
key = [0x00, 0x99, 0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11]


a,b=generateKey(9)
arr=[0]*10
for k in range(len(arr)):
     
     c=RSAencrypt(a[1], a[0], key[k])
     arr[k]=c
print("after encryption")     
print(arr)
newArr=""
for j in range(len(arr)):
      newArr=newArr+str(arr[j])
      newArr=newArr+","
arrMsg=newArr.split(',')
arrHex=[0]*10
for t in range(10):
     arrHex[t]=int(arrMsg[t]) 
print("after casting from string to int array")  
print(arrHex)     
arr1=[0]*10
for k in range(len(arr1)):
     d=RSAdecrypt(b[1], b[0], arrHex[k])
     arr1[k]=d
print("after decryption")
print(arr1)

'''   
   
   
   
   
   
   
   
   
   
   
   