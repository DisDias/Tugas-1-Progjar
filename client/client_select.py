import socket
import sys

host = '127.0.0.1'
port = 65435

def receiveFile(conn, namaFile, sizeFile):
    with open(namaFile, 'wb') as rf:
        while True:
            data = conn.recv(int(sizeFile))
            if not data:
                print('Selesai')
                break
            rf.write(data)
    rf.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    #sys.stdout.write('>> ')
    print('>>', end=' ', flush=True)

    try:
        while True:
            message = sys.stdin.readline()
            s.send(bytes(message, 'utf-8'))
            received_data = s.recv(1024).decode('utf-8')
            if received_data == 'File Tidak Ditemukan':
                #sys.stdout.write(received_data)
                print(received_data)
            else:
                namaFile, sizeFile = received_data.split(":")
                receiveFile(s, namaFile, sizeFile)

            #sys.stdout.write('>> ')
            print('>>', ' ', flush=True)

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

