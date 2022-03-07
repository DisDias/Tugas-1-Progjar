import socket
import select
import sys
import os

host = '127.0.0.1'
port = 65435

server_address = (host, port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
sourcePath = "./dataset/"

def findFile(filename):
    for file in os.listdir(sourcePath):
        # namaAja = os.path.splitext(file)
        if file.lower() == filename.lower():
            return file
    return False

def sendFile(pathFile, conn):
    with open(pathFile, "rb") as sf:
        data = sf.read(1024)
        while (data):
            conn.send(data)
            # data = sf.read(1024)
            # print ('Sent', repr(data))
            data = sf.read(1024)
    sf.close()

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:            	
                data = sock.recv(1024)
                print(sock.getpeername(), data)
            
                if data:
                    kata = data.decode("utf-8")
                    splitKata = kata.split(" ")
                    if splitKata[0] == 'unduh':
                        filename = splitKata[1].strip()
                        resultFile = findFile(filename)
                        if resultFile is False:
                            sock.send(bytes('File Tidak Ditemukan', 'utf-8'))
                        else:
                            pathFile = sourcePath + resultFile
                            sizeFile = os.path.getsize(pathFile)
                            # header = f"File-name:{resultFile},\nFile-size:{sizeFile}\n\n\n"
                            sock.send(f"File-name:{resultFile},\nFile-size:{sizeFile}\n\n\n".encode())
                            sendFile(pathFile, sock)
                    else:
                        sock.send(bytes('Command yang dimasukkan salah. Silahkan masukkan unduh nama_file', 'utf-8'))
                        
                    
                else:                    
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)