import socket
import hashlib
import sys
str1 =''
def client():
    rsHostName, rsListenPort, tsListenPort = sys.argv[1], sys.argv[2], sys.argv[3]
    lst = makeList()
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    rsaddr = (rsHostName, int(rsListenPort))
    cs.connect(rsaddr)
    tsaddr = (rsHostName, int(tsListenPort))
    cs1.connect(tsaddr)

    for l in lst:
        try:
            cs.send(l)
            data = cs.recv(1024)
            #print(data.strip()[-1])
            if(data.strip()[-1] != "S"):
                print("Recieved: " + data)
            else:
                #print(data.strip()[0:-5])
                str1 = data.strip()[0:-5]
                #print(str1)
                ip = socket.gethostbyname(str1)
                #tsaddr = (ip, int(tsListenPort))
               # cs1.connect(tsaddr)
                #print(ip)
                cs1.send(l)
                data1 = cs1.recv(1024)
                if(data1.strip()[-1]=="A"):
                    print(data1)
                else: 
                    print("Hostname not found")
        except:
            print("ERROR")

def makeList():
    lst = []
    try:
        f = open('PROJI-HNS.txt', 'r')
        print('[C]: File successfully opened\n')
        lines = list(f)
        f.close()
    except IOError as err:
        sys.exit(format(err))

    # Extracting each line of our file and creatin
    for line in lines:
        lst.append(line)

    return lst

client()
