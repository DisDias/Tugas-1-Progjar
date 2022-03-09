import socket
import sys
import math
import re

host = '127.0.0.1'
port = 65435

def receiveFile(conn, namaFile, sizeFile):
    find_loop = math.ceil(int(sizeFile) / 1024)
    flag = 0
    with open(namaFile, 'wb') as rf:
        while True:
            data = conn.recv(1024)
            flag += 1
            rf.write(data)
            # print(flag, max_loop)
            if find_loop == flag:
                print('\nFile selesai ditransfer.')
                break
    rf.close()

def splitData(received_data):
    namaFile, sizeFile = received_data.split(",\n")
    title_name, namaFile = namaFile.split(":")
    sizeFile = int(''.join(filter(str.isdigit, sizeFile)))
    
    return namaFile, str(sizeFile)
    


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
            elif received_data == 'Command yang dimasukkan salah. Silahkan masukkan unduh nama_file':
                print(received_data)
            else:
                # TO DO: cari parsing DONE
                namaFile, sizeFile = splitData(received_data)
                print("File-name:", namaFile)
                print("File-Size:", sizeFile)
                # print()
                # File-name: coba.txt 
                # File-size:33\n\n\n
                receiveFile(s, namaFile, sizeFile)

            #sys.stdout.write('>> ')
            print('>>', flush=True, end=' ')

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)