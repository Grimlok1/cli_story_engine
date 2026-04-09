from colorama import Fore, Back, Style, init
import os
os.system("")
init()

class Renderer:
    def info(self, text):
        print(Style.BRIGHT + Fore.YELLOW + text + Style.RESET_ALL)
    
    def title(self, text):
        print(Style.BRIGHT + Fore.MAGENTA + text + Style.RESET_ALL)

    def success(self, text):
        print(Fore.GREEN + text + Style.RESET_ALL)

    def error(self, text):
        print(Style.BRIGHT + Fore.RED + text + Style.RESET_ALL)

    def normal(self, text):
        print(text)