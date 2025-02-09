import os
import signal
import time
from .ADHT import menull
from .lolcat import lolcat
def clear():
    os.system("clear")
def domain_m():
    while True:
        print(f"""
        \033[94m╔─╗\033[0m\033[94m┌────────────────────────────────────────────┐\033[0m
        \033[91m| |\033[0m                     D̳O̳M̳A̳I̳N̳ ̳M̳E̳N̳U̳ 
        \033[91m| |\033[0m\033[94m└────────────────────────────────────────────┘\033[0m 
        \033[91m| |\033[0m[\033[96m01\033[0m] GANTI DOMAIN VPS
        \033[91m| |\033[0m[\033[96m02\033[0m] PERBARUI CERTIFICATE DOMAIN
        \033[91m| |\033[0m
        \033[91m| |\033[0m[\033[91m0\033[0m] \033[91mBACK TO MENU\033[0m
        \033[91m| |\033[0m
        \033[94m╚─╝\033[0m\033[94m└────────────────────────────────────────────┘\033[0m"
         [\033[91m•0\033[0m] \033[91mBACK TO MENU\033[0m
        """)
        lolcat(f" Press [ Ctrl+C ] • To-Exit")
        options = input(" \033[93mInput Options: \033[0m")
        if options == "1":
            clear()
            menull()
            return
        else:
            print("\033[91m What are you doing. Select the above option\033[0m")