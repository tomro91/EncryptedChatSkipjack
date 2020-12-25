#Server side
import _thread
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
host="localhost"
port=5000
s.bind((host,port))
s.listen(10)
clients=[]
clients_l = []
#function that handles message from client
def connectNewClient(c):
  
     while True:
          msgf = c.recv(2048).decode('ascii')
          print("msg",msgf)
          #new client connect to chat app
          if 'new980' in msgf:
             msg = msgf.split(',')[0]
             clients_l.append(msg)
             msgs = ','.join(clients_l)
             print(msg+' connected')
             sendToAll(msgs+'@new980',c)
             msg = ' \n    '+msg.title() + ' is online.\n'
          #client log out from the chat app   
          elif 'gone980' in msgf:
               msg = msgf.split(',')[0]
               print(msg+' Disconnected')
               clients_l.pop(clients_l.index(msg))
               msgs = ','.join(clients_l)
               sendToAll(msgs+'@gone980',c)
          #client try to send message but does not have premissions    
          elif 'no premissions to send messages' in msgf:
              msg1= "there is no premissions"
              c.send(msg1.encode('ascii'))
         #client send message in the chat
          else:
             msg =msgf
             sendToAll(msg,c)
#function that send message to all clients
def sendToAll(msg,con):
    for client in clients:
        client.send(msg.encode('ascii')) 
        
while True:
    c,ad=s.accept()
    print('Connection Established')
    clients.append(c)
    print('clients')
    print(clients)
    _thread.start_new_thread(connectNewClient,(c,))
