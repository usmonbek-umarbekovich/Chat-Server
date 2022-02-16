# Chat server
Simple chat server application built with python

## Table of contents

- [How to run](#how-to-run)
- [Features](#features)
- [How to use](#how-to-use)
- [Authors](#authors)

## How to run

Do the following steps to run the application:

- Run the server `python server.py`
- Add a client `python client.py`
  - Enter your name (write admin for more privilages)
  - If you are admin, enter the admin password

## Features

The application has the following features:

- You can add as many clients as you want
- Server and other clients will be informed as soon as\
  new user joined or left the chat
- You can write messages to all the clients connected to the server
- You can write private messages to any client you want
- If you are an admin, you can have many privilages:
  - You can kick out any user
  - You can ban any user

## How to use

The application doesn't have GUI. It is run on the command line.\
Following sections describes how to use each feature of the application

### Adding many clients

In order to add many clients, you simply have to\
run `client.py` file in one of the following ways:

- Run in different command line window
- Run in another computer connected to the same local network

### Write message to other users

After you run `client.py` file and enter your credentials\
new input field will be opened. You can write your message there\
and press *Enter* keyboard. Your message will be delivered right away.

### Write private messages

You can also chat with any individual user.\
You have to prepend user's name with `@` symbol and\
put at least 1 whitespace and write your message.

For example, suppose you want to write to a user named *Jerry*.\
You need to do the following: `@Jerry Hello, how are you?`\
The message will be delivered only to Jerry.

### Admin privilages: Kicking out a user.

To be an admin, you need enter your name as `admin`\
and you will be asked to enter admin password.

All the commands have to be prepended with `/` character.\
If you want to kick out certain user, you need to\
write `/kick` followed by the name of the user\
you want to kick out.

For example: `/kick Jerry`

### Admin privilages: Banning a user

Banning a user is very similar to kicking out.\
The keyword: `/ban`

For example: `/ban Jerry`

## Authors

Following people built this application:

- Rustamov Usmonbek (ID: 52352)
- Otojonov Sherzod (ID: 52448)