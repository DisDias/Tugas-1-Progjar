import socket
import sys
import math

host = '127.0.0.1'
port = 65436

def receiveFile(conn, namaFile, sizeFile):
    max_loop = math.ceil(int(sizeFile) / 1024)
    flag = 0
    with open(namaFile, 'wb') as rf:
        while True:
            data = conn.recv(1024)
            flag += 1
            rf.write(data)
            # print(flag, max_loop)
            if max_loop == flag:
                print('Selesai')
                break
            # rf.write(data)
    rf.close()

def splitData(received_data):
    namaFile, sizeFile = received_data.split(",\n")
    title_name, namaFile = namaFile.split(":")
    sizeFile = int(''.join(filter(str.isdigit, sizeFile)))
    
    return namaFile, str(sizeFile)

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    # Connect to server and send data
    print('>>', end=' ', flush=True)
    try:
        while True:
            message = sys.stdin.readline()
            sock.send(bytes(message, 'utf-8'))
            received_data = sock.recv(1024).decode('utf-8')
            if received_data == 'File Tidak Ditemukan':
                #sys.stdout.write(received_data)
                print(received_data)
            elif received_data == 'Command yang dimasukkan salah. Silahkan masukkan unduh nama_file':
                print(received_data)
            else:
                # TO DO: cari parsing
                namaFile, sizeFile = splitData(received_data)
                print(namaFile, sizeFile)
                # File-name: coba.txt 
                # File-size:33\n\n\n
                receiveFile(sock, namaFile, sizeFile)

            #sys.stdout.write('>> ')
            print('>>', ' ', flush=True)


    except KeyboardInterrupt:
        sock.close()
    


