import os
import subprocess
import importlib
from datetime import datetime
import time
import signal
from .lolcat import lolcat
def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)


def get_expiration_info(username):
    try:
        exp = subprocess.check_output(f"chage -l {username} | grep 'Account expires'", shell=True).decode().strip().split(": ")[1]
        exp_date = datetime.strptime(exp, "%b %d, %Y").timestamp()
        now_date = datetime.now().timestamp()
        days_left = (exp_date - now_date) // 86400
        status = subprocess.check_output(f"passwd -S {username}", shell=True).decode().strip().split()[1]
        return exp, int(days_left), status
    except Exception as e:
        return None, None, None

def read_users():
    back = importlib.import_module("modules.mmxsh")
    found = False
    print("\033[34m╔════════════════════════════════════════════════════╗\033[0m")
    print("\033[31m┃        Log Data SSH Account       ┃\033[0m")
    print("\033[34m╚════════════════════════════════════════════════════╝\033[0m")
    print("\033[34m╔════════════════════════════════════════════════════╗")
    lolcat(" USERNAME       EXP DATE    DAYS LEFT")
    print("\033[34m╚════════════════════════════════════════════════════╝")

    with open("/etc/passwd", "r") as passwd:
        for line in passwd:
            parts = line.split(":")
            username, uid = parts[0], int(parts[2])
            if uid >= 1000 and username != "nobody":
                exp, days_left, status = get_expiration_info(username)
                if exp and status:
                    print(f"{username:<17} {exp} | {days_left}")
                    found = True

    total_users = subprocess.getoutput("awk -F: '$3 >= 1000 && $1 != \"nobody\" {print $1}' /etc/passwd | wc -l")
    print("\033[34m┌───────────────────────────────────────┐")
    print(f"       \033[93mJumlah User:\033[0m\033[91m {total_users}\033[0m\033[93m user\033[0m")
    print("\033[34m└───────────────────────────────────────┘")

    if not found:
        print("\033[34m╔════════════════════════════════════════════════════╗")
        print("\033[31m|                            DATA Failure            |\033[0m")
        print("\033[34m╚════════════════════════════════════════════════════╝\033[0m")
        print(f" 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆")
        print("\n \033[91mUser Account Does Not Exist \033[0m \n")
        lolcat("\n Press enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
        user_input = input(" \033[93mYour choice:\033[0m ").strip()
        if user_input.lower() == "x":
            lolcat("Exiting...")
            back.ssh_menu()
            return
    check_user()

def check_user():
    back = importlib.import_module("modules.mmxsh")
    while True:
        user = input(" \033[93mInput Username (x to cancel):\033[0m ")
        if user.lower() == "x":
            lolcat(" Exiting SSH account data process")
            time.sleep(0.5)
            os.system("clear")
            back.ssh_menu()
            break
        elif os.path.isfile(f"/etc/xraylog/log-ssh-{user}.txt"):
            print("\033[34mUser exists\033[0m")
            os.system(f"cat /etc/xraylog/log-ssh-{user}.txt")
            print(f"Copy your account data")
            while True:
                choice = input("\033[93mPress 'x' to exit or Enter to check another account:\033[0m ").strip().lower()
                if choice == "x":
                    lolcat(" Exiting SSH account data process")
                    time.sleep(0.5)
                    os.system("clear")
                    back.ssh_menu()
                    return
                elif choice == "":
                    os.system("clear")
                    read_users()
                    break
                else:
                    print("\033[91mInvalid input. Please press 'x' or Enter. \033[0m")
        else:
            print("\033[31mUser does not exist\033[0m")