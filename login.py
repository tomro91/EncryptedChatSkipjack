from tkinter import *
from tkinter import messagebox as mb
from hashlib import sha256
import client
import _thread
import random
from csv import DictReader
import csv
import sys


#login screen
def login():
    #login GUI-login screen
    try:
        reg.destroy()
    except:
        pass
    
    global log
    log = Tk()
    log.title('Login')
    log.geometry('300x300+220+170')
    log.configure(bg='white')
    log.resizable(0,0)

    log_label = Label(log, text='Login', width=20, height=1, font=('Arial Black',20,'bold'))
    log_label.pack()

    u = Label(log, text='Username :', font=('Arial Black',14,'bold'),bg='white')
    u.place(x=10,y=50)
    
    user_entry = Entry(log, font=('Arial Black',10,'bold'),  width=25,bg='powder blue')
    user_entry.place(x=10, y=80)


    p = Label(log, text='Password :', font=('Arial Black',14,'bold'),bg='white')
    p.place(x=10,y=110)
    
    pass_entry = Entry(log,show='*', font=('Arial Black',10,'bold'),  width=25,bg='powder blue')
    pass_entry.place(x=10, y=140)

    resp = Label(log, text='',font=('Arial Black',10,'bold'),bg='white')
    resp.place(x=10, y=250)
     #login function
    def log_func(*args):

        f = open('resources/log_details.csv', 'r')
        r = DictReader(f)
        l = []
        for row in r:
            l1 = []
            l1.append(row['name'])
            l1.append(row['username'])
            l1.append(row['password'])
            l.append(l1)

        user = user_entry.get()
        #get password with hash
        input_pass = pass_entry.get()
        h = sha256()
        h.update((input_pass).encode('utf-8'))
        hash_pass = h.hexdigest()
        print(hash_pass)
        #validate user
        for i in l:
            print(i[1])
            if i[1] == user:
                passw = i[2]
                if hash_pass == passw:
                    username_name = i[0]
                    resp.configure(text=f'Login Successful\n Welcome {i[0]} ', fg='green')
                    client.main_func(i[0])
                else:
                    resp.configure(text=f'Wrong Password', fg='red')
                    break
            else:
                resp.configure(text=f'Username {user} Does Not Exist', fg='red') 
    submit = Button(log, text='Submit',font=('Arial Black',10,'bold'), width=14, bg='green', command=log_func,bd=0,fg='white')
    submit.place(x=10, y=180)

    Label(log, text='Dont\'t Have An Account.',bg='white').place(x=30,y=210)


    log.bind('<Return>', log_func)

    log.mainloop()
    
    
     




login()


