import socket
import select
import sys

host = '127.0.0.1'
port = 65435

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    input_socket = [s]

    try:
        while True:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
        
            for sock in read_ready:
                if sock == s:
                    client_socket, client_address = s.accept()
                    input_socket.append(client_socket)        
                
                else:            	
                    data = sock.recv(1024)
                    print(sock.getpeername(), data)
                
                    if data:
                        sock.send(data)
                    else:                    
                        sock.close()
                        input_socket.remove(sock)

    except KeyboardInterrupt:        
        s.close()
        sys.exit(0)