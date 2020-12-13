from tkinter import *
from tkinter import messagebox as mb
import tkinter.scrolledtext as tks
import socket
import _thread
import sys
from csv import DictReader
import skipjack as skip
key = [0x00, 0x99, 0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11]
sj = skip.SkipJack()
#chat window of client
def main_func(username):

    i = 3
    client = 0
    start = True

    client_name = []
    client_name.append(username)        
  
        
  #initializes the availble users
    def del_dups(l):
        dup = []
        for i in l:
            if i not in dup:
                dup.append(i)
            else:
                pass
        global client_name
        client_name = dup
        return dup


    #log out function
    def log_out(username):
        to = username +',gone980'
        c.send(to.encode('ascii'))
        win.destroy()

        

    #creates the list of active users
    def list_insert(msg):
        active_users.delete(0,END)
        global active_list
        active_list = []
                
        for i in range(0,len(msg)):
            m = msg[i].split(',')
            for j in range(0,len(m)):
                client_name.append(m[j])
                active_users.insert(i+1,m[j])
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
    

    #encryption function
    def encrypt(plainText, key):
        ctFinal = ""
        # a list of strings that each one holds 64-bit words (all together make the plaintext)
        ptPart = partPlaintext(plainText.lower())
        for i in range(len(ptPart)):
            # turn the plaintext from a string to hexadecimal int
            pt = textToHexInt(ptPart[i])
            # send the plaintext and key to the skipjack class and encrypt it.
            ct = sj.encrypt(pt, key)
            ctFinal += str(hex(ct))
        print("Cipher text: " + str(ctFinal))
        return ctFinal 
    #decryption function          
    def decrypt(cipherText, key):
        dtFinal = ""
        # a list of strings that each one holds 64-bit words (all together make the ciphertext)
        ctPart = partCiphertext(cipherText)
        for i in range(len(ctPart)):
            # send the ciphertext and key to the skipjack class and decrypt it.
            dt = sj.decrypt(int(ctPart[i], 16), key)
            # turn the decrypted text from a hexadecimal int to string
            text = hexIntToText(hex(dt))
            dtFinal += text
        print("Decrypted text: " + dtFinal)
        return dtFinal

    #send message in the chat
    def sendMessage (username,*args):
        f = open('resources/log_details.csv', 'r')
        r = DictReader(f)
        l = []
        for row in r:
            l1 = []
            l1.append(row['name'])
            l1.append(row['username'])
            l1.append(row['password'])
            l1.append(row['permission'])
            l.append(l1)
        for i in l:
            if i[0] == username:
                print("hey"+i[3])
                if i[3]=="1":
                    u = username.split()[0]
                    global msg1
                    msg1=msg_entry.get()
                    global msg2
                    msg2=encrypt(msg1,key)
                    msg = u + ' : '+msg2
                    global c
                    c.send(msg.encode('ascii'))
                else:
                    msg="no premissions to send messages"
                    c.send(msg.encode('ascii'))
                    
    #recieve message in the chat
    #need to add decryption
    def recievingMessage (c): 
        while True :
            msg=c.recv(2048).decode('ascii')
            print(msg)
            x=msg.split(':')
            if len(x)==2:
                global msg3
                msg3=decrypt(x[1],key)
                global msg4
                msg4=x[0]+":"+msg3
                
            
            #new client log in
            if 'new980' in msg:
                
                msg = msg.split('@')
                msg.pop(-1)
                list_insert(msg)
                for i in msg:
                    client_name.append(i)
               
                
               #client log out
            elif 'gone980' in msg:
                
                
                msg = msg.split('@')
                msg.pop(-1)
                list_insert(msg)
                for i in msg:
                    client_name.append(i)
            elif 'there is no premissions'in msg:
               
               messagebox.showinfo("information","User does not have premissions to send messages!")  
            else:
                t = text.get(1.0,END)
                text.delete(1.0,END)
                text.insert(INSERT,t+msg4+'\n')
                text.yview('end')
               




            
    #Socket Creation
    def socketCreation (username):
        global c
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        host = '127.0.0.1'
        port = 5000
        c.connect((host,port))
        msg = username + ',new980'
        c.send(msg.encode('ascii'))
        global client
        client = c
        _thread.start_new_thread(recievingMessage, (c,) )


    #client GUI-chat window

    win = Toplevel()
    win.geometry('530x400')
    win.resizable(0,0)
    win.title('Chat')

    Label(win, text='Chat',bg='white', font=('arial black',18),width=50,height=1).pack()

    
    
    text = tks.ScrolledText(win,height=17,width=41, font=('arial black',10),wrap=WORD)
    text.place(x=10,y=40)
    text.yview('end')

    


    msg_entry = Entry(win, font=('arial black',13),width=25)
    msg_entry.place(x=10,y=365)

    send = Button(win, font=('arial black',10), text='Send',bd=0,bg='blue',fg='white',width=10,command=lambda : sendMessage(username))
    send.place(x=300,y=365)

    Label(win, font=('arial black',13),bg='blue',fg='white',text='Users',width=12).place(y=40,x=400)

    f = open('resources/log_details.csv', 'r')
    r = DictReader(f)
    l = []
    for row in r:
            l1 = []
            l1.append(row['name'])
            l.append(l1)

    user_list = Listbox(win,height=8,width=20)
    user_list.place(x=400,y=70)
    for i in l:        
        user_list.insert(END,i[0])



    

    Label(win, font=('arial black',13),bg='Green',fg='white',text='Active Users',width=10).place(y=200,x=400)

    active_users = Listbox(win,height=8,width=20)
    active_users.place(x=400,y=230)

    Label(win, text='Logged In as : \n'+ username,font=('arial black',10)).place(x=400,y=360)

    global set_img
    set_img = PhotoImage(file='resources\\icons8-menu-48.png')
    set_img = set_img.subsample(2)
    
    menu_b = Button(win, image=set_img,bd=0,bg='white')
    menu_b.image = set_img
    menu_b.place(x=490,y=2)

    

    def clear_chat_func():
        text.delete(1.0,END)


    pop = Menu(win, tearoff=0)    
    pop.add_command(label='Clear Chat',command=clear_chat_func)
    pop.add_separator()
    pop.add_command(label='Log Out',command=lambda: log_out(username))

    def do(event):
        try:
            pop.tk_popup(event.x_root,event.y_root,0)
        finally:
            pop.grab_release


    menu_b.bind('<Button-1>',do)



    def key_press(*args):
        sendMessage(username)
    
    win.bind('<Return>',key_press)

    _thread.start_new_thread(socketCreation, (username,) )
    
    win.mainloop()










