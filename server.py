import socket
import threading 

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

server.bind(('localhost' , 9999))

server.listen()
print("Server is Listening....")


clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try :
            message = client.recv(1024)
            broadcast(message)
        except:
            index= clients.index(client)
            clients.remove(client)
            nickname =nicknames[index]
            broadcast(f"{nickname}left the chat room!".encode("ascii"))
            nicknames.remove(nickname)
            clients.remove(client)
            client.close()
            break

  

def receive():
    while True : 
        client , address = server.accept()

        print(f"Connection from {address} has been established")
        client.send("Welcome to the chat Room!".encode("ascii"))
        client.send("NICK".encode("ascii"))
        
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat room!".encode("ascii"))
        client.send("Connected to the Server!".encode("ascii"))
        thread = threading.Thread(target=handle , args=(client,))
        thread.start()

                 
    
receive()