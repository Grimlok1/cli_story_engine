from colorama import Fore, Style, init
init()

def info(text):
    print(Fore.CYAN + text + Style.RESET_ALL)

def success(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

def warning(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)

def error(text):
    print(Fore.RED + text + Style.RESET_ALL)