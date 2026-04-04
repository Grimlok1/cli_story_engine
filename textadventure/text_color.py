from colorama import Fore, Back, Style, init
import os
os.system("")

init()
def info(text):
    print(Style.BRIGHT + Fore.YELLOW + text + Style.RESET_ALL)
    
def title(text):
    print(Style.BRIGHT + Fore.MAGENTA + text + Style.RESET_ALL)

def success(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

def error(text):
    print(Style.BRIGHT + Fore.RED + text + Style.RESET_ALL)