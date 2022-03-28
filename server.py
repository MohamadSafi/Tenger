import socket
from threding import Thread

SERVER_HOST = "0.0.0.0"
SERVER_port = 5002
erarator_token = "<SEP>"
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
        except Eception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.repllace(seprator_token, ": ")
        
        for client_socket in client_sockets:
            client_socket.send(msg.encode)

while True:
    slient_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_socket.add(client_socket)
    t = Thread(target=listen_for_client, args = (client_socket,))
    t.deamon = True
    t.start()

for sc in client_sockets:
    cs.close()
