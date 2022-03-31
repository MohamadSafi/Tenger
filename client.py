import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, Back
import colorama
import os

banner = f"""
{Fore.BLUE}████████╗███████╗███╗   ██╗ ██████╗ ███████╗██████╗ 
{Fore.BLUE}╚══██╔══╝██╔════╝████╗  ██║██╔════╝ ██╔════╝██╔══██╗
{Fore.BLUE}   ██║   █████╗  ██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
{Fore.BLUE}   ██║   ██╔══╝  ██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
{Fore.BLUE}   ██║   ███████╗██║ ╚████║╚██████╔╝███████╗██║  ██║
{Fore.BLUE}   ╚═╝   ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝{Fore.RESET}
"""

def startup():
    os.system("clear")
    print(banner)


colors = [Fore.BLUE, Fore.GREEN, Fore.LIGHTRED_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.YELLOW]

username = os.getenv("LOGNAME")
client_color = random.choice(colors)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
seprator_token = "<SEP>"
s = socket.socket()

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print(message)


def main():
    colorama.init()
    startup()
    print(f"{Fore.GREEN}[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...{Fore.RESET}")
    s.connect((SERVER_HOST, SERVER_PORT))
    print(f"{Fore.GREEN}[+] Connected.{Fore.RESET}")

    t = Thread(target = listen_for_messages)
    t.daemon = True
    t.start()

    while True:
        to_send = input()
        if to_send.lower() == "exit":
            break

        date_now = datetime.now().strftime('%H:%M:%S')
        to_send = f"{client_color}[{date_now}] {username}{seprator_token}{to_send}{Fore.RESET}"
        s.send(to_send.encode())

try:
    main()
except KeyboardInterrupt:
    pass
finally:
    s.close()



