import os
import subprocess
from datetime import datetime
import signal
import time
from .lolcat import lolcat
import importlib

RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
NC = '\033[0m'
def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")
    
def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)

    
def get_server_date():
    try:
        result = subprocess.check_output(
            ["curl", "-sI", "https://google.com"], stderr=subprocess.DEVNULL
        ).decode("utf-8")
        for line in result.splitlines():
            if line.startswith("Date:"):
                return datetime.strptime(line.split("Date: ")[1], "%a, %d %b %Y %H:%M:%S GMT")
    except Exception:
        pass
    return datetime.now()

def clear_console():
    os.system("clear")

def list_users():
    back = importlib.import_module("modules.mmxsh")
    found = False
    print(f"\033[34m╔═{RED}─────────────────────────────────────\033[34m═╗")
    print(f"\033[31m| \033[1;31;44;1mUSERNAME       EXP DATE    DAYS LEFT \033[0m\033[31m |")
    print(f"\033[34m╚═{RED}─────────────────────────────────────\033[34m═╝")
    print(f"{BLUE}┌──────────────────────────────────────┐{NC}")
    print("")

    with open("/etc/passwd", "r") as passwd_file:
        for line in passwd_file:
            fields = line.split(":")
            username = fields[0]
            uid = int(fields[2])

            if uid >= 1000 and username != "nobody":
                try:
                    exp_output = subprocess.check_output(
                        ["chage", "-l", username], stderr=subprocess.DEVNULL
                    ).decode("utf-8")
                    exp = [line.split(": ")[1].strip() for line in exp_output.splitlines() if "Account expires" in line][0]
                    exp_date = datetime.strptime(exp, "%b %d, %Y")
                    days_left = (exp_date - datetime.now()).days
                    
                    print(f"\033[92m{username:<17}|{exp:<15}|{days_left} days left\033[0m")
                    found = True
                except Exception:
                    continue
    print(f"{BLUE}└──────────────────────────────────────┘{NC}")
    if not found:
        print(f"{RED}User not found!{NC}")
        print(f"{BLUE}└──────────────────────────────────────┘{NC}")
        print(f" 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆")
        lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
        user_input = input(" \033[93mInput Options\033[0m: ").strip()
        if user_input.lower() == "x":
            lolcat(" Exiting SSH Account Delete Process")
            back.ssh_menu()
            return
        else:
            return

    delete_user()

def delete_user():
    back = importlib.import_module("modules.mmxsh")
    while True:
        username = input(" \033[93mInput  the Username (x to cancel): \033[0m").strip()
        if username.lower() == "x":
            lolcat(" Exiting SSH Account Delete Process")
            back.ssh_menu()
            return
        elif username == "root":
            os.system("clear")
            print(f" {RED}what are you doing bro!!{NC}")
            print(f" {RED}Jangan Masukin Root ya anjj, Lu mau Vps lu gak bisa di akses{NC}")
        elif username in [line.split(":")[0] for line in open("/etc/passwd")]:
            print(f"{BLUE}User deleted.{NC}")
            subprocess.run(["userdel", username])
            subprocess.run(["rm", "-rf", f"/etc/xraylog/ssh-{username}.txt"])
            subprocess.run(["sed", "-i", f"/### {username}/d", "/etc/qos/ssh/sshadmin.txt"])
            break
        else:
            print(f"{RED}Enter correctly, repeat!!{NC}")

    clear_console()
    print(f"\033[34m╔═{RED}─────────────────────────────────────\033[34m═╗")
    print(f"\033[31m| \033[1;31;44;1m            Delete SSH User          \033[0m\033[31m |")
    print(f"\033[34m╚═{RED}─────────────────────────────────────\033[34m═╝")
    print(f"{BLUE}┌───────────────────────────────────┐{NC}")
    print(f"{GREEN}        User {NC} {RED} {username} {NC} {GREEN} Deleted{NC} ")
    print(f"{BLUE}└───────────────────────────────────┘{NC}")
    print(f" \033[92m𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆\033[0m")
    lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
    while True:
        action = input(" \033[93mInput Options: \033[0m").strip().lower()
        if action == "x":
          lolcat("\033[93m Exiting SSH Account Delete Process\033[0m")
          time.sleep(0.5)
          os.system("clear")
          back.ssh_menu()
          break
        elif action == "":
          os.system("clear")
          list_users()
          delete_user()
          break
        else:
          print("\033[91mPlease enter 'x' to exit or press Enter to return.\033[0m")
