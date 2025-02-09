import re
import os
from datetime import datetime, timedelta
from .lolcat import lolcat
import importlib
import signal
import time
def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)
def clear_screen():
    os.system("clear")
signal.signal(signal.SIGINT, handle_sigint)
def gmer01fuser(user_file):
    users = []
    if not os.path.exists(user_file):
        print(f"File user {user_file} tidak ditemukan.")
        return users

    with open(user_file, 'r') as file:
        for line in file:
            if line.startswith("###"):
                parts = line.split()
                if len(parts) >= 2:
                    users.append(parts[1])
    return users


def connected(log_file, users_check, timeminutes=10):
    now = datetime.now()
    useripmap = {}

    if not os.path.exists(log_file):
        print(f"File log {log_file} tidak ditemukan.")
        return user_ip_map

    with open(log_file, 'r') as file:
        logs = file.readlines()
    log_pattern = re.compile(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (\d+\.\d+\.\d+\.\d+):\d+.*email:\s*([a-zA-Z0-9._%+-]+)')

    for log in logs:
        match = log_pattern.search(log)
        if match:
            timestamp_str = match.group(1)
            ip = match.group(2)
            email = match.group(3)
            log_time = datetime.strptime(timestamp_str, "%Y/%m/%d %H:%M:%S")
            time_difference = now - log_time
            if email in users_check and time_difference <= timedelta(minutes=timeminutes):
                if email not in useripmap:
                    useripmap[email] = set()
                useripmap[email].add(ip)

    return {email: ips for email, ips in useripmap.items() if ips}

log_file = '/var/log/xray/access.log'
user_file = '/etc/qos/xray/vless.txt'
timeminutes = 5
users_check = gmer01fuser(user_file)

def vless_on():
    os.system("clear")
    back = importlib.import_module("modules.vvx")
    if not users_check:
        while True:
            print("\033[34m╔═─────────────────────────────────────═╗\033[0m")
            print("\033[31m┃\033[0m \033[1;31;44;1m          VLESS ONLINE USER          \033[0m\033[31m ┃\033[0m")
            print("\033[34m╚═─────────────────────────────────────═╝\033[0m")
            print("")
            print("             \033[91m Empty Member\033[0m")
            print("")
            print(f"      \033[94m━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
            print(f"   \033[92m𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆\033[0m")
            lolcat("\nPress Enter to go back to VLESS menu or ( Ctrl + X )to exit.\n")
            user_input = input(" \033[93mPress Enter.. \033[0m").strip()
            if user_input.lower() == "":
                print(f"\033[93mExiting the VLESS User Online process.\033[0m")
                time.sleep(0.5)
                back.vless_menu()
                return
            else:
                print("\033[91m What are you doing ?\033[0m")
                time.sleep(0.5)
                clear_screen()
    else:
        print("\033[34m╔═─────────────────────────────────────═╗\033[0m")
        print("\033[31m┃\033[0m \033[1;31;44;1m          VLESS ONLINE USER          \033[0m\033[31m ┃\033[0m")
        print("\033[34m╚═─────────────────────────────────────═╝\033[0m")
        print(f" \033[92m𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆\033[0m")
        print("\033[34m┌────────────────────────────────────────────┐\033[0m")
        useripmap = connected(log_file, users_check, timeminutes)
        if useripmap:
            for user, ips in useripmap.items():
                print("       \033[31m-------------------------------\033[0m")
                print(f"           USER     : \033[32;1m{user}\033[0m")
                print(f"           Total IP : \033[31;1m{len(ips)}\033[0m")
                for ip in ips:
                    print(f"               IP   : \033[36;1m{ip}\033[0m")
                print("       \033[31m-------------------------------\033[0m")
        print("\033[34m└────────────────────────────────────────────┘\033[0m")
        print("")
        lolcat("\n Press Enter to return to User Online account or type 'x' to exit...\n")
        while True:
            action = input(" \033[93mInput Options:\033[0m ").strip().lower()
            if action == "x":
                print(f"\033[93mExiting the VLESS User Online process.\033[0m")
                time.sleep(0.5)
                os.system("clear")
                back.VLESS_menu()
                return
            elif action == "":
                os.system("clear")
                vless_on()
                return
            else:
                print("\033[91mPlease enter 'x' to exit or press Enter to return.\033[0m")
        else:
            while True:
                print("\033[34m╔═─────────────────────────────────────═╗\033[0m")
                print("\033[31m┃\033[0m \033[1;31;44;1m          VLESS ONLINE USER          \033[0m\033[31m ┃\033[0m")
                print("\033[34m╚═─────────────────────────────────────═╝\033[0m")
                print("")
                print("             \033[91m Empty Member\033[0m")
                print("")
                print(f"      \033[94m━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
                print(f"   \033[92m𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆\033[0m")
                lolcat("\n Input X to go back to VLESS menu or ( Ctrl + X )to exit.\n")
                user_input = input(" \033[93mInput Options : \033[0m").strip()
                if user_input.lower() == "":
                    vless_on()
                    return
                elif user_input.lower() == "x":
                    print(f"\033[93mExiting the VLESS User Online process.\033[0m")
                    time.sleep(0.5)
                    os.system("clear")
                    back.vless_menu()
                else:
                    print("\033[91m What are you doing ?\033[0m")
                    time.sleep(0.5)
                    clear_screen()