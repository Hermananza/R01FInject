import os
import subprocess
from datetime import datetime
import importlib
import re
import time
import signal
from .lolcat import lolcat
def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)


RED = '\033[0;31m'
NC = '\033[0m'
ORANGE = '\033[0;33m'
CYAN = '\033[0;36m'
BLUE = '\033[0;34m'


LOG = "/var/log/auth.log" if os.path.exists("/var/log/auth.log") else "/var/log/secure"

def get_date_from_server():
    result = subprocess.run(
        ["curl", "-v", "--insecure", "--silent", "https://google.com/"], 
        capture_output=True, text=True
    )
    date_match = re.search(r'Date: (.*)', result.stderr)
    if date_match:
        date_str = date_match.group(1).strip()
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
    else:
        return None

def parse_logs(log_file, service):
    with open(log_file, "r") as file:
        lines = file.readlines()
    return [line for line in lines if service in line and "Password auth succeeded" in line]

def get_user_and_ip_from_pid(log_lines, pids):
    user_pids = {}
    user_ips = {}
    for pid in pids:
        relevant_lines = [line for line in log_lines if f"{pid}" in line]
        for line in relevant_lines:
            parts = line.split()
            if "dropbear" in line:
                user, ip = parts[9], parts[11]
            else:
                user, ip = parts[8], parts[10]
            if user:
                user_pids.setdefault(user, []).append(pid)
                user_ips.setdefault(user, set()).add(ip)  # Use set to ensure unique IPs
    return user_pids, user_ips

def display_users(user_pids, user_ips):
    if not user_pids:
        print(f"{RED}User Account Does Not Exist{NC}")
        return False
    else:
        for user in user_pids:
            unique_pids = len(set(user_pids[user]))
            unique_ips = user_ips[user]
            print("--------------------")
            print(f" Username = {user}")
            print(f" Log IP = {unique_pids}")
            print(" IPs:")
            for ip in unique_ips:
                print(f"   - {ip}")
            print("--------------------")
        print("")
        return True

def online_ssh():
    back = importlib.import_module("modules.mmxsh")
    os.system("clear")
    print(f"{ORANGE}╒────────────────────────────────────────────╕{NC}")
    print(" \033[0;36;44;1m               SSH User Online              \033[0m")
    print(f"{CYAN}╘────────────────────────────────────────────╛{NC}")
    print(f"{RED}┌────────────────────────────────────────────┐{NC}")
    print("\n\n")

    dropbear_pids = [line.split()[1] for line in subprocess.getoutput("ps aux | grep -i dropbear").splitlines() if "dropbear" in line]
    sshd_pids = [line.split()[1] for line in subprocess.getoutput("ps aux | grep '[priv]'").splitlines() if "[priv]" in line]

    dropbear_logs = parse_logs(LOG, "dropbear")
    dropbear_users, dropbear_ips = get_user_and_ip_from_pid(dropbear_logs, dropbear_pids)

    sshd_logs = parse_logs(LOG, "sshd")
    sshd_users, sshd_ips = get_user_and_ip_from_pid(sshd_logs, sshd_pids)

    user_pids = {**dropbear_users, **sshd_users}
    user_ips = {**dropbear_ips, **sshd_ips}

    if not display_users(user_pids, user_ips):
        lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
        print("")
        input(" \033[93mYour choice: \033[0m")
        back.ssh_menu()
        return

    print(f"{RED}└────────────────────────────────────────────┘{NC}")
    print(f" 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆")
    lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
    print("")
    
    while True:
        action = input(" \033[93mInput Options: \033[0m").strip().lower()
        if action == "x":
            lolcat("Exiting the Online User SSH process.")
            time.sleep(0.5)
            os.system("clear")
            back.ssh_menu()
            break
        elif action == "":
            os.system("clear")
            online_ssh()
            break
        else:
            print("\033[91mPlease enter 'x' to exit or press Enter to return.\033[0m")