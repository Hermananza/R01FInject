import os
import re
import importlib
import subprocess
from datetime import datetime, timedelta
import time
import signal
from .lolcat import lolcat
def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip(), result.stderr.strip()

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def list_ssh_members():
    back = importlib.import_module("modules.mmxsh")
    print_colored("╔══════════════════════════════════════════╗", "34")
    print_colored("┃            SSH Member List               ┃", "31")
    print_colored("╚══════════════════════════════════════════╝", "34")
    print_colored(" USERNAME      EXP DATE        STATUS", "31")
    print("\033[34m┌────────────────────────────────────────┐\033[0m")

    user_found = False
    with open("/etc/passwd", "r") as passwd_file:
        for line in passwd_file:
            fields = line.split(":")
            username, uid, shell = fields[0], int(fields[2]), fields[-1].strip()
            if uid >= 1000 and shell != "/usr/sbin/nologin":
                user_found = True
                exp_date, _ = run_command(f"chage -l {username} | grep 'Account expires' | awk -F': ' '{{print $2}}'")
                status, _ = run_command(f"passwd -S {username} | awk '{{print $2}}'")
                status_text = "\033[91mLOCKED\033[0m" if status == "L" else "\033[93mUNLOCKED\033[0m"
                print(f" \033[92m{username:<17}{exp_date:<17}\033[0m{status_text}")
    print(f"\033[34m└────────────────────────────────────────┘\033[0m")
    if not user_found:
        print_colored("╔══════════════════════════════════════════╗", "34")
        print_colored("┃           Renewal Failure               ┃", "31")
        print_colored("╚══════════════════════════════════════════╝", "34")
        print_colored("Username not found ", "31")
        lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
        print("")
        user_input = input("\033[93mYour choice: \033[0m").strip()
        if user_input.lower() == "x":
            lolcat("Exiting...")
            back.ssh_menu()
        else:
            return

    renew_user()

def renew_user():
    back = importlib.import_module("modules.mmxsh")
    lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
    print("")
    while True:
        username = input(" \033[93mInput Username:\033[0m ")
        if username.lower() == "x":
            lolcat(" Exiting SSH Account Renewal Process")
            os.system("clear")
            back.ssh_menu()
            return
        if username == "root":
            os.system("clear")
            print(f" \033[91m Lu mau panik?? Tolol masukin root ?, makanya jangan masukin root\033[0m")
            time.sleep(3.0)
            back.ssh_menu()
        if re.search(f"^{username}:", open("/etc/passwd").read(), re.MULTILINE):
            print("\033[92mUsername found .\033[0m")
            break
        else:
            print("\033[91mUsername not found. Please try again.\033[0m")

    while True:
        days_input = input(" \033[93mDay Extend:\033[0m ")
        if days_input.lower() == "x":
            lolcat(" Exiting SSH Account Renewal Process")
            os.system("clear")
            back.ssh_menu()
            return
        if days_input.isdigit():
            days = int(days_input)
            break
        else:
            print("\033[91mPlease enter the number correctly.\033[0m")

    os.system("clear")
    today = datetime.now()
    expire_date = today + timedelta(days=days)
    expire_on = expire_date.strftime("%Y-%m-%d")

    os.system(f"passwd -u {username}")
    os.system(f"usermod -e {expire_on} {username}")

    print_colored("╔══════════════════════════════════════════╗", "34")
    lolcat("         Renewal Successfully            \n")
    print(f" \033[92mUsername   :\033[0m\033[93m {username}\033[0m")
    print(f" \033[92mDays Added : \033[0m\033[93m{days} \033[0m\033[92mDays\033[0m")
    print(f" \033[92mExpires on : \033[0m\033[93m{expire_date.strftime('%d %b %Y')}\033[0m")
    print_colored("╚══════════════════════════════════════════╝", "34")
    print(f" \033[92m𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆\033[0m")
    lolcat("\n Press enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
    while True:
        action = input(" \033[93mInput Options:\033[0m ").strip().lower()
        if action == "x":
          lolcat(" Exiting SSH Account Renewal Process")
          time.sleep(0.5)
          os.system("clear")
          back.ssh_menu()
          break
        elif action == "":
          os.system("clear")
          list_ssh_members()
          renew_user()
          break
        else:
          print("\033[91mPlease enter 'x' to exit or press Enter to return.\033[0m")