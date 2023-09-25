import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = '127.0.0.1'
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            conn.sendall(data)
    print('Connection closed by', addr)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()
        conn, addr = s.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

start_threaded_server()