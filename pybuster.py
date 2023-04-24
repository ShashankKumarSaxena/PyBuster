from __future__ import annotations
import argparse
from colorama import Fore, init

from commons import *
from _buster import Buster

init()

ASCII = """
██▓███ ▓██   ██▓ ▄▄▄▄    █    ██   ██████ ▄▄▄█████▓▓█████  ██▀███
▓██░  ██▒▒██  ██▒▓█████▄  ██  ▓██▒▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒ ▒██ ██░▒██▒ ▄██▓██  ▒██░░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒ ░ ▐██▓░▒██░█▀  ▓▓█  ░██░  ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄
▒██▒ ░  ░ ░ ██▒▓░░▓█  ▀█▓▒▒█████▓ ▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░  ██▒▒▒ ░▒▓███▀▒░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░     ▓██ ░▒░ ▒░▒   ░ ░░▒░ ░ ░ ░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░
░░       ▒ ▒ ░░   ░    ░  ░░░ ░ ░ ░  ░  ░    ░         ░     ░░   ░
         ░ ░      ░         ░           ░              ░  ░   ░
         ░ ░           ░
"""

# Defining the argument parser for command line operations.
parser = argparse.ArgumentParser(
    prog="PyBuster",
    description="Fast directory buster tool with inbuilt wordlist.",
    epilog="By: ShashankKumarSaxena\nVisit: https://shashanksaxena.netlify.app/ to know more!",
)

# Adding the required and default arguments
parser.add_argument("url", help="URL of the target to bruteforce")  # URL of the host to brute-force
parser.add_argument(
    "-w", "--wordlist", default="./assets/wordlist.txt", help="Path to wordlist. Default: inbuilt"
)  # Default wordlist
parser.add_argument(
    "-t", "--threads", default=10, help="Number of threads to use. Default: 10"
)  # Default thread value = 10
parser.add_argument(
    "-sS", "--show-successful", action="store_true", help="Show only the results with 200 status. Default: off"
)
parser.add_argument("-s", "--secure", action="store_true", help="Is the host secure or not. Default: yes", default=True)
parser.add_argument("-f", "--file", default=None, help="Provide a file name to create and save the results in.")

if __name__ == "__main__":
    color_println(ASCII, Fore.RED)
    color_println(f"[+] TIP: Set the number of threads according to your system for faster result!", Fore.GREEN)

    args = parser.parse_args()

    if args.file:
        try:
            f = open(args.file, "w")
            f.close()
        except Exception as _:
            color_println("Provide a valid file name.", Fore.RED)
            quit()

    # Bruh, why don't I directly pass only args var and proccess other things in class Lol
    buster = Buster(args.url, int(args.threads), args.wordlist, args)

    try:
        buster.start_buster()
    except Exception as e:
        color_println(f"Oops! Something went wrong\n{e.__str__()}", Fore.RED)
