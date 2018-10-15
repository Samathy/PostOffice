import cups
import sys
import time
import socket

connection_limit = 10

cups_connection = cups.Connection()

def check_rate_limit(connection_ip):
    '''Checks previous connections and rejects this one if connected too over
    some number of times today. 
    Returns True if connection allowed, false if not.
    '''

    return True

def write_file(string, ip, date):
    '''Saves the passed string to a file.
    File name is: <ipv4>_<d/m/Y>
    Return filename.
    '''
    
    filename = str(ip)+"_"+str(date)
    with open(filename, "w+") as f:
       f.write("----"+ip+"  "+date+"----\n")
       f.write(string)

    return filename

def print_file(filename):
    
    with open(filename, "r") as f:
        print(f.readline())

    default = cups_connection.getDefault();

    cups_connection.printFile(default, filename, filename, dict())

    return

def decrypt(string):
    '''Decrypt the string using user's pgp key'''
    return

def parse_string(string):
    '''Parses the printable bytes with an attempt to find 
    one of the special strings we can handle'''

    return

def await_connections():
    
    IP = "127.0.0.1"
    PORT = 7878
    
    buffer_size = 240

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))

    sock.listen(1)
    
    conn, addr = sock.accept()

    if (check_rate_limit(addr) == True):
        data = conn.recv(buffer_size)

        print(data.decode())
        filename = write_file(data.decode(), addr[0], time.strftime("%d-%m-%Y"))

        print_file(filename)

        conn.send(b"OK")

    else:
        conn.close()


if __name__ == "__main__":
    await_connections()
