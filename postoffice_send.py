import socket

IP = "127.0.0.1"
PORT = 7878

message = "Hello World"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((IP, PORT))
sock.send(message.encode())
data = sock.recv(1024)

if str(data) == "OK":
    print(str(data))

sock.close()


sock.close
