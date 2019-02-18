import socket
import hashlib
import sys

# Table element object -- Will be used for our dictionary
dnstable = []
elements = []
elem = []
tmpstr =[]
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
    try:
        rss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[RS]: Socket was successfully created')
    except socket.error as err:
        sys.exit(format(err))

    rss.bind(('', int(sys.argv[1])))
    rss.listen(1)

    print>>sys.stderr, 'Waiting for connection...'
    connection, caddr = rss.accept()
    try:
        print>> sys.stderr, 'Connected to ', caddr
        while True:
            message = connection.recv(1024)
            print("Received " + message +
                  "from client at: " + str(caddr[0]) + ", " + str(caddr[1]))
            # TODO: Add the lookup at this point
            
            str3 = lookup(message)
            connection.send(str3)

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
            print(str3)
            break
        else:
            str3 = str2 + '- Host Name Not Found'
            #print(str3)
    return str3

    # Printing out the contents of the dnstable
    print('[TS]: Printing DNS Table contents... \n')
    for item in dnstable:
        print('[TS]:  Key: ' + item + '\n\t\t\t ' + dnstable[item].tostring())

TSServer()
