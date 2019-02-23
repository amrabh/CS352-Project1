import socket
import hashlib
import sys
import threading 

# Table element object -- Will be used for our dictionary
dnstable = []
str3 = ' '

class tableElement:
    def __init__(self, hostname, ipaddr, flag):
        self.hostname = hostname
        self.ipaddr = ipaddr
        self.flag = flag

    def tostring(self):
        return "Hostname: " + self.hostname + " \n\t\t\t IP Addr: " + self.ipaddr + " \n\t\t\t Flag: " + self.flag

def TSServer():
    poptable()
    print('*******')
    print(socket.gethostname())
    print(socket.gethostbyname(socket.gethostname()))
    try:
        rss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rss.bind(('', int(sys.argv[1])))
        print('[RS]: Socket was successfully created')
    except socket.error as err:
        sys.exit(format(err))
    rss.listen(1)
    while True:
        print>>sys.stderr, 'Waiting for connection...'
        connection, caddr = rss.accept()
        print>> sys.stderr, 'Connected to ', connection    
        try:
            message = connection.recv(1024)
            if message:
                print("Received " + message +
                    "from client at: " + str(caddr[0]) + ", " + str(caddr[1]))
                # TODO: Add the lookup at this point
                str3 = lookup(message)
                connection.send(str3)
            else: 
                print('Client disconnected')
                connection.close()
                break
        finally:
            connection.close()



def poptable():
    
    # Reading and making sure that the file opens
    try:
        f = open('PROJI-DNSTS.txt', 'r')
        print('[TS]: File successfully opened\n')
        lines = list(f)
        f.close()
    except IOError as err:
        sys.exit(format(err))

    # Extracting each line of our file and creatin
    for line in lines:
        hostname, ip, flag = line.strip().split()
        #dnstable[hashlib.md5(hostname).hexdigest()] = tableElement(
        #    hostname, ip, flag)
        dnstable.append([hostname, ip, flag])


def lookup(msg):
    str3 = ' '
    for i in range(len(dnstable)-1):
        str1 = dnstable[i][0]
        str2 = msg.rstrip('\r\n')
        print(str2)
        if str1.lower() == str2.lower():
            tmpstr = dnstable[i]
            str3 = ' '.join(tmpstr)
            break
        else:
            str3 = str(str2 + ' - Error: Host Name Not Found')
        print(str3)
    return str3

    # Printing out the contents of the dnstable
    print('[TS]: Printing DNS Table contents... \n')
    for item in dnstable:
        print('[TS]:  Key: ' + item + '\n\t\t\t ' + dnstable[item].tostring())

TSServer()
