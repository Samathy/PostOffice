import cups
import sys
import time
import socket
import os
import gnupg
from daemonize import Daemonize

connection_limit = 10

cups_connection = cups.Connection()

def check_rate_limit(connection_ip):
    '''Checks previous connections and rejects this one if connected too over
    some number of times today. 
    Returns True if connection allowed, false if not.
    
    Delete last line: https://stackoverflow.com/a/10289740
    '''

    try:
        f = open(connection_ip+".rate", "r+")
    except FileNotFoundError:
        f = open(connection_ip+".rate", "a+")

    #This is really slow, apparently. But we probably don't care much.
    last = ""
    first = f.readline()
    for last in f: pass

    
    if (last.split(" ")[0] == time.strftime("%d/%m/%Y")):
        #Check the existing value for today
        if (int(last.split(" ")[1]) >= 20):
            #Return false if we've exceeded the limit
            f.close()
            return False
        else:
            #Increment it
            previous_val = int(last.split(" ")[1])
            f.seek(0, os.SEEK_END)
            pos = f.tell() - 1
            while pos > 0 and f.read(1) != "\n":
                pos -= 1
                f.seek(pos, os.SEEK_SET)

            if pos > 0:
                f.seek(pos, os.SEEK_SET)
                f.truncate()

            f.write("\n"+time.strftime("%d/%m/%Y")+" "+str(previous_val+1))
             
    elif(last.split(" ")[0] != time.strftime("%d/%m/%Y")):
        #Add a new date if it doesnt exist yet.
        f.close()
        f = open(connection_ip+".rate", "a")

        f.writelines(time.strftime("%d/%m/%Y")+" "+str(1)+"\n")

    f.close()

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
    
    default = cups_connection.getDefault();

    cups_connection.printFile(default, filename, filename, dict())

    return

def decrypt(string):
    '''Decrypt the string using user's pgp key'''
    return

def parse_string(string):
    '''Parses the printable bytes with an attempt to find 
    one of the special strings we can handle'''

    gpg = gnupg.GPG()

    key_len = 40
    if ("-----BEGIN PGP MESSAGE----" in string[:30]):
        message_decrypted = gpg.decrypt(string)

        return message_decrypted

    return string

def await_connections():
    
    IP = "127.0.0.1"
    PORT = 7878
    
    buffer_size = 240

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))

    while True:
        sock.listen(1)

        conn, addr = sock.accept()

        if check_rate_limit(addr[0]):
            data = conn.recv(buffer_size)

            filename = write_file(parse_string(data.decode()), addr[0], time.strftime("%d-%m-%Y-%H-%M"))

            print_file(filename)

            conn.send(b"OK")

            conn.close()

        else:

            conn.close()


if __name__ == "__main__":

    pid = "/tmp/postoffice.pid"

    if ("-d" in sys.argv):
        print("Daemonizing....")
        daemon = Daemonize(app="PostOffice", pid=pid, action=await_connections)
        daemon.start()
    else:
        await_connections()
