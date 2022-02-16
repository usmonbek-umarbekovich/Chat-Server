import socket
import threading

from config import *

name = input('Name: ')
if name == ADMIN:
  password = input('Admin Password: ')

# set up the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def recieve():
  while True:
    try:
      message = client.recv(HEADER).decode(FORMAT)

      if message == 'NAME':
        client.send(name.encode(FORMAT))

      # user is claiming to be the admin
      # send password to the server to verify
      elif message == 'PASSWORD':
        client.send(password.encode(FORMAT))

      # verification is NOT successful
      elif message == 'WRONG_PASSWORD':
        print('Connection was refused. Wrong password!')
        raise Exception()

      # if the user is in the ban list
      # remove the connection
      elif message == 'BANNED':
        print('Connection was refused. You are banned')
        raise Exception()
          
      # if message is from other clients
      else:
        if len(message): print(message)
    except:
      # close the connection
      client.close()
      break
    
def send():
  while True:
    try:
      message = input()
      
      # if message is a command
      if message.startswith('/'):
        if name == ADMIN:
          client.send(message.encode(FORMAT))
        else:
          print('Commands can only be executed by the admin!')
      
      # if message is intented for single user
      elif message.startswith('@'):
        client.send(message.encode(FORMAT))
        
      # if message is ordinary
      else:
        client.send(f'{name}: {message}'.encode(FORMAT))
    except OSError:
      break


# start the threads
receive_thread = threading.Thread(target=recieve)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
