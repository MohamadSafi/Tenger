import socket
from threading import Thread
from colorama import Fore
import subprocess
import re
from time import sleep
from os import remove

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
seprator_token= "<SEP>"
client_sockets = set()
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_clients(cs):
    try:
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
                    remove("jprq_output")
                
    except KeyboardInterrupt:
        return

def start_jprq():
    with open("/dev/null","w") as which_output:
        jprq_check = subprocess.run(["which", "jprq"],stdout = which_output)
    if jprq_check.returncode == 0:
        with open("jprq_output", "w+") as jprq_output:
            with open("/dev/null","w") as err_file:
                subprocess.run(["jprq", "tcp", "5000"], stderr = err_file, stdout = jprq_output)

    else:
        print("Please install jprq to start your server.")
        exit(1)
        remove("jprq_output")

def get_jprq_port():
    res = None
    while res == None:
        jprq_output = open("jprq_output","w+")
        file_content = jprq_output.read()
        res = re.search("tcp\.jprq\.io:[0-9]+",file_content)
        jprq_output.close()
    host_and_port = file_content[res.start():res.end()]
    jprq_host = host_and_port[:host_and_port.find(":")]
    jprq_port = host_and_port[host_and_port.find(":")+1:]
    print(f"""Your HOST is "{Fore.RED}{jprq_host}{Fore.RESET}"\nYour PORT is "{Fore.RED}{jprq_port}{Fore.RESET}" """)

def main_server():
    while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        client_sockets.add(client_socket)
        t = Thread(target=listen_for_clients, args = (client_socket,))
        t.deamon = True
        t.start()
def main():
    server_thread = Thread(target=main_server, args = ())
    server_thread.deamon = True
    server_thread.start()

    jprq_thread = Thread(target=start_jprq, args =())
    jprq_thread.deamon = True
    jprq_thread.start()
    
    get_jprq_port()
try :
    main()
except KeyboardInterrupt:
    for cs in client_sockets:
        cs.close()
    remove("jprq_output")
    s.close()
