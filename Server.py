import socket
import threading
import os.path

host = "localhost"
port = 9000

mySocket = socket.socket()
mySocket.bind((host, port))
mySocket.listen(5)


def waitForConnection():
    while True:
        if threading.activeCount() <= 5:
            conn, addr = mySocket.accept()
            threading.Thread(target=isConnected, args=(conn, addr)).start()


def getContent(myFile):
    response = False
    if os.path.exists(myFile):
        try:
            file = open(myFile, 'rb')
            response = file.read()
            file.close()
        except Exception as e:
            print(e)
    return response

def isConnected(conn, addr):
    while True:
        request = conn.recv(1024).decode('utf-8')
        print(request)

        listOfStringRequest = request.split(" ")
        fileSelector = listOfStringRequest[1]
        if fileSelector == "/":
            fileSelector = "/index.html"

        myFile = "." + fileSelector

        response = getContent(myFile)


        header = 'HTTP/1.1 200 OK\n'

        if response == False:
            response = getContent("./404.html")
            header = "HTTP/1.1 404 Not Found\n"

        header += 'File:' + myFile + "\n"
        header += 'Connection: close\n\n'

        final_response = header.encode('utf-8')
        final_response += response
        conn.send(final_response)
        conn.close()
        break

waitForConnection()