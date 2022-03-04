import socket
import sys

host = '127.0.0.1'
port = 65435

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    sys.stdout.write('>> ')

    try:
        while True:
            message = sys.stdin.readline()
            s.send(bytes(message, 'utf-8'))
            received_data = s.recv(1024).decode('utf-8')
            sys.stdout.write(received_data)
            sys.stdout.write('>> ')

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

