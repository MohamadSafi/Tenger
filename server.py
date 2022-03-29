import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
seprator_token= "<SEP>"
client_sockets = set()
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_clients(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(seprator_token, ": ")
        
        for client_socket in client_sockets:
            if client_socket == cs:
                continue
            try:
                client_socket.send(msg.encode())
            except Exception as e:
                print(f"[!] Error: {e}")
def main():
    while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        client_sockets.add(client_socket)
        t = Thread(target=listen_for_clients, args = (client_socket,))
        t.deamon = True
        t.start()
try :
    main()
except KeyboardInterrupt:
    for cs in client_sockets:
        cs.close()
    s.close()
