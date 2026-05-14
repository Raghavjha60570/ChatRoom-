import socket 
import threading 

nickname = input("Choose Your Nickname :")

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

client.connect(('localhost', 9999))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")

            if "NICK" in message:
                client.send(nickname.encode("ascii"))
            else:
                print(message)

        except:
            print("An error occurred!")
            client.close()
            break
def write():
     while True:
          message = f"{nickname}: {input('')}"
          client.send(message.encode("ascii"))
         
receive_thread = threading.Thread(target = receive)
receive_thread.start()
write_thread= threading.Thread(target=write)
write_thread.start()
