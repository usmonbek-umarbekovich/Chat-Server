import re
import socket
import threading

from config import *

clients = []
names = []
bans = []

# set up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def send_message(sender, receiver_name, message):
  sender_index = clients.index(sender)
  sender_name = names[sender_index]
  if receiver_name not in names:
    sender.send(f'There is no such User'.encode(FORMAT))
    return
  
  index = names.index(receiver_name)
  receiver = clients[index]
  receiver.send(f'{sender_name}: {message}'.encode(FORMAT))


def broadcast(message):
  for client in clients:
    client.send(message)


def handle(client):
  while True:
    try:
      message = client.recv(HEADER)
      decoded = message.decode(FORMAT)

      # if message was a command
      if decoded.startswith('/'):
        decoded = re.split('\s+', decoded)
        if len(decoded) == 1:
          command = decoded[0].lower()
          if command == '/ban' or command == '/kick':
            client.send('Please specify the user to kick out'.encode(FORMAT))
          else:
            client.send('There is no such command'.encode(FORMAT))
          continue
        else:
          command, user = decoded
        
        if command.lower() == '/kick':
          kick_user(user)
        elif command.lower() == '/ban':
          kick_user(user, forever=True)
        
      # if message was intended for single user  
      elif decoded.startswith('@'):
        decoded = re.split('\s+', decoded[1:])
        
        # if there is no message, do nothing
        if len(decoded) == 1:
          continue
        
        # find sender name, and send message to user
        user, *user_message = decoded
        user_message = ' '.join(user_message)
        send_message(client, user, user_message)
        
      # ordinary message to group
      else:
        broadcast(message)
    except:
      if client not in clients: break
      
      index = clients.index(client)
      name = names[index]
      
      # remove the client from the list
      del clients[index]
      del names[index]
          
      # close the connection with the user and notify others
      client.close()
      broadcast(f'{name} left the chat'.encode(FORMAT))
      
      print(f'[USER LEFT] {name} left the chat')
      print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 2}')
      break


def start():
  # start the server
  server.listen()
  print(f'[LISTENING] Server is listening')
  
  while True:
    client, address = server.accept()

    client.send('NAME'.encode(FORMAT))
    name = client.recv(HEADER).decode(FORMAT)
    
    if name in bans:
      client.send('BANNED'.encode(FORMAT))
      client.close()
      continue
    
    if name == ADMIN:
      # if client claims to be the admin, VERIFY it
      client.send('PASSWORD'.encode(FORMAT))
      password = client.recv(HEADER).decode(FORMAT)

      if password != PASSWORD:
        client.send('WRONG_PASSWORD'.encode(FORMAT))
        client.close()
        continue
    
    # inform server and clients that new user has joined
    print(f'[NEW CONNECTION]')
    print(f'[USER] {name} {address}')
    broadcast(f'{name} joined the chat'.encode(FORMAT))
    
    # add client to list and inform
    clients.append(client)
    names.append(name)
    client.send('Connected to the server'.encode(FORMAT))
    
    # start handling new client
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()
    print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')


def kick_user(name, forever=False):
  # if there is no such user, terminate the command
  if name not in names: return
  
  if forever:
    info = 'banned'
    bans.append(name)
  else:
    info = 'kicked'

  # find the user and do the operation
  index = names.index(name)
  client_to_kick = clients[index]
  
  if name == ADMIN:
    client_to_kick.send(f"You can't kick out yourself :)".encode(FORMAT))
    return
  
  client_to_kick.send(f'You have been {info} by the admin'.encode(FORMAT))
  client_to_kick.close()
  
  del clients[index]
  del names[index]
  
  print(f'[{info.upper()}] {name} has been {info}')
  print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')
  broadcast(f'{name} was {info} by the admin'.encode(FORMAT))
    

print('[STARTING] server is starting...')
start()
