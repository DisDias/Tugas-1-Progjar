import socket
import select
import sys
import os

host = '127.0.0.1'
port = 65435

def findFile(datasetFile, namaFile):
    for file in datasetFile:
        namaAja = os.path.splitext(file)
        if namaAja[0].lower() == namaFile.lower():
            return file
    return False

def sendFile(pathFile, conn):
    with open(pathFile, "rb") as sf:
        data = sf.read(1024)
        while (data):
            conn.send(data)
            print ('Sent', repr(data))
            data = sf.read(1024)
    sf.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    input_socket = [s]

    try:
        while True:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            dataset = "./dataset/"
            datasetFile = []

            for (pathTemp, namaTemp, namaFile) in os.walk(dataset):
                datasetFile.extend(namaFile)
                break

            for sock in read_ready:
                if sock == s:
                    client_socket, client_address = s.accept()
                    input_socket.append(client_socket)        
                
                else:            	
                    data = sock.recv(1024)
                    print(sock.getpeername(), data)
                
                    if data:
                        kata = data.decode("utf-8")
                        splitKata = kata.split(" ")
                        namaFile = splitKata[1].strip()
                        resultFile = findFile(datasetFile, namaFile)
                        if resultFile is False:
                            sock.send(bytes('File Tidak Ditemukan', 'utf-8'))
                        else:
                            pathFile = dataset + resultFile
                            sizeFile = os.path.getsize(pathFile)
                            sock.send(f"{resultFile}:{sizeFile}".encode())
                            sendFile(pathFile, sock)

                    else:                    
                        sock.close()
                        input_socket.remove(sock)

    except KeyboardInterrupt:        
        s.close()
        sys.exit(0)