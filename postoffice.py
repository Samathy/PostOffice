import sys
import time
import os
import socket
import gnupg
from daemonize import Daemonize
import cups

CONNECTION_LIMIT = 20

CUPS_CONNECTION = cups.Connection()

def check_rate_limit(connection_ip):
    '''Checks previous connections and rejects this one if connected too over
    some number of times today.
    Returns True if connection allowed, false if not.

    Delete last line: https://stackoverflow.com/a/10289740
    '''

    try:
        rate_limit_file = open(connection_ip+".rate", "r+")
    except FileNotFoundError:
        rate_limit_file = open(connection_ip+".rate", "a+")

    #This is really slow, apparently. But we probably don't care much.
    last = ""
    for last in rate_limit_file:
        pass

    if last.split(" ")[0] == time.strftime("%d/%m/%Y"):
        #Check the existing value for today
        if int(last.split(" ")[1]) >= CONNECTION_LIMIT:
            #Return false if we've exceeded the limit
            rate_limit_file.close()
            return False
        else:
            #Increment it
            previous_val = int(last.split(" ")[1])
            rate_limit_file.seek(0, os.SEEK_END)
            pos = rate_limit_file.tell() - 1
            while pos > 0 and rate_limit_file.read(1) != "\n":
                pos -= 1
                rate_limit_file.seek(pos, os.SEEK_SET)

            if pos > 0:
                rate_limit_file.seek(pos, os.SEEK_SET)
                rate_limit_file.truncate()

            rate_limit_file.write("\n"+time.strftime("%d/%m/%Y")+" "+str(previous_val+1))
    elif last.split(" ")[0] != time.strftime("%d/%m/%Y"):
        #Add a new date if it doesnt exist yet.
        rate_limit_file.close()
        rate_limit_file = open(connection_ip+".rate", "a")

        rate_limit_file.writelines(time.strftime("%d/%m/%Y")+" "+str(1)+"\n")

    rate_limit_file.close()

    return True

def write_file(string, ip_addr, date):
    '''Saves the passed string to a file.
    File name is: <ip_addrv4>_<d/m/Y>
    Return filename.
    '''
    folder = "logs/"
    filename = folder + str(ip_addr)+"_"+str(date)
    with open(filename, "w+") as message_file:
        message_file.write("------------\n"+ip_addr+"\n"+date+"\n------------\n")
        message_file.write(string)
        message_file.write("------------")

    return filename

def print_file(filename):
    '''Sends the file to the printer '''
    default = CUPS_CONNECTION.getDefault()

    CUPS_CONNECTION.printFile(default, filename, filename, dict())

def parse_string(string):
    '''Parses the printable bytes with an attempt to find
    one of the special strings we can handle'''

    gpg = gnupg.GPG()

    if "-----BEGIN PGP MESSAGE----" in string[:30]:
        message_decrypted = gpg.decrypt(string)

        return message_decrypted

    return string

def await_connections():
    '''Await connections from the outside
    and take all actions necessary to print
    our content '''
    #Uncomment the below to accept non-localhost connections
    #IP = "0.0.0.0"
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

    if "-d" in sys.argv:
        print("Daemonizing....")
        daemon = Daemonize(app="PostOffice", pid=pid, action=await_connections)
        daemon.start()
    else:
        await_connections()
