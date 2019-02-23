import socket
import hashlib
import sys
str1 =''
def client():
    rsHostName, rsListenPort, tsListenPort = sys.argv[1], sys.argv[2], sys.argv[3]
    lst = makeList()
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #cs1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #cs1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    rsaddr = (rsHostName, int(rsListenPort))
    cs.connect(rsaddr)
    #tsaddr = (rsHostName, int(tsListenPort))
    #cs1.connect(tsaddr)
    text_file = open("Resolved.txt", "a")
    for l in lst:
        cs.send(l)
        data = cs.recv(1024)
        #print(data.strip()[-1])
        if(data.strip()[-1] != "S"):
            print("Recieved: " + data)
            text_file.write(str(data)+'\n')
        else:
            #print(data.strip()[0:-5])
            str1 = data.strip()[0:-5]
            #print(str1)
            ip = socket.gethostbyname(str1)
            tsaddr = (ip, int(tsListenPort)) 
            cs1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cs1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            cs1.connect(tsaddr)
            cs1.send(l)   
            data1 = cs1.recv(1024)
            #print(l[0:-1])
            #print('&&&&&&&&&&&&&&&&&&')
            #print(data1)
            print(data1)
            text_file.write(str(data1)+'\n')
    text_file.close()

    



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
