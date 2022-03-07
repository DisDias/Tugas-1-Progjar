import socket
import threading
import socketserver
import os

host = '127.0.0.1'
port = 65436

#input_socket = [server_socket]
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

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        cur_thread = threading.current_thread()
        while True:
            self.data = self.request.recv(1024)
            print(self.request.getpeername(), self.data)

            if self.data:
                    kata = self.data.decode('utf-8')
                    splitKata = kata.split(" ")
                    if splitKata[0] == 'unduh':
                        filename = splitKata[1].strip()
                        resultFile = findFile(filename)
                        if resultFile is False:
                            self.request.send(bytes('File Tidak Ditemukan', 'utf-8'))
                        else:
                            pathFile = sourcePath + resultFile
                            sizeFile = os.path.getsize(pathFile)
                            # header = f"File-name:{resultFile},\nFile-size:{sizeFile}\n\n\n"
                            self.request.send(f"File-name:{resultFile},\nFile-size:{sizeFile}\n\n\n".encode())
                            sendFile(pathFile, self.request)
                    else:
                        self.request.send(bytes('Command yang dimasukkan salah. Silahkan masukkan unduh nama_file', 'utf-8'))

            else:
                return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


with ThreadedTCPServer((host, port), ThreadedTCPRequestHandler) as s:
        try:
            s.serve_forever()

        except KeyboardInterrupt:
            print('selesai')
            s.shutdown()
