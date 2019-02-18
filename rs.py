import socket
import hashlib
import sys
# Table element object -- Will be used for our dictionary

dnstable = []
elements = []
elem = []
tmpstr =[]
str3 = ' '
class tableElement(object):
    def __init__(self, hostname, ipaddr, flag):
        self.hostname = hostname
        self.ipaddr = ipaddr
        self.flag = flag

    def tostring(self):
        return "Hostname: " + self.hostname + " \n\t\t\t IP Addr: " + self.ipaddr + " \n\t\t\t Flag: " + self.flag

def rsServer():
    poptable()
    print('*******')
    print(socket.gethostname())
    print(socket.gethostbyname(socket.gethostname()))
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
            if not message:
                print>>sys.stderr, 'No more messages. Connection will close. Bye.'
                break
            print("Received " + message +
                  "from client at: " + str(caddr[0]) + ", " + str(caddr[1]))
            # TODO: Add the lookup at this point
            
            str3 = lookup(message)
            connection.send(str3)

    finally:
        connection.close()


def poptable():
     # dictionary for our dnstable

    # Reading and making sure that the file opens
    try:
        f = open('PROJI-DNSRS.txt', 'r')
        print('[RS]: File successfully opened\n')
        lines = list(f)
        f.close()
    except IOError as err:
        sys.exit(format(err))

    # Extracting each line of our file and creatin
    for line in lines:
        hostname, ip, flag = line.strip().split()
        dnstable.append([hostname, ip, flag])


def lookup(msg):
    str3 = ' '
    for i in range(len(dnstable)-1):
        str1 = dnstable[i][0]
        str2 = msg.rstrip('\r\n')
        if str1.lower() == str2.lower():
            tmpstr = dnstable[i]
            str3 = ' '.join(tmpstr)
            break
        else:
            tmpstr = dnstable[len(dnstable)-1]
            str3 = ' '.join(tmpstr)
            print(str3)
    return str3
        

def printdns():
    print('[RS]: Printing contents of dnstable...')
    for item in dnstable:
        print('[RS]:  Key: ' + str(item) +
              '\n\t\t\t ' + dnstable[item].tostring())


rsServer()
