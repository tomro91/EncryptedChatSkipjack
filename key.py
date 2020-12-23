import random

class Key:
    
    def init(self, key=''):
        if key=='':
            self.key= self.generate()
        else:
            self.key= self.lower()
    
    #generate a key
    def generate(self):
        key='0x'
        chunk='0x'
        check_digit_count=0
        alphabet='0123456789ABCDEF'
        #while(True):
        while len(key)<49:
            char= random.choice(alphabet)
            key= key+char
            chunk=chunk+char
            if len(chunk)==4:
                key= key+','+'0'+'x'
                chunk='0x'
        key= key[:-1]
        key1=key.split(',')
        key1.pop()
        return key1
    


