from __future__ import annotations
import urllib3.util
import urllib.parse

import requests
import threading
from colorama import Fore
from commons import *
import urllib3


class StatusColors:
    STATUS_200 = Fore.GREEN
    STATUS_201 = Fore.YELLOW
    STATUS_202 = Fore.YELLOW
    STATUS_203 = Fore.YELLOW
    STATUS_204 = Fore.YELLOW
    STATUS_205 = Fore.RED
    STATUS_206 = Fore.YELLOW
    STATUS_207 = Fore.YELLOW
    STATUS_301 = Fore.YELLOW
    STATUS_302 = Fore.BLUE
    STATUS_303 = Fore.YELLOW
    STATUS_304 = Fore.YELLOW
    STATUS_305 = Fore.BLUE
    STATUS_306 = Fore.YELLOW
    STATUS_307 = Fore.YELLOW
    STATUS_308 = Fore.YELLOW
    STATUS_400 = Fore.RED
    STATUS_401 = Fore.RED
    STATUS_402 = Fore.WHITE
    STATUS_403 = Fore.YELLOW
    STATUS_404 = Fore.RED
    STATUS_405 = Fore.YELLOW
    STATUS_406 = Fore.YELLOW
    STATUS_407 = Fore.YELLOW
    STATUS_408 = Fore.YELLOW
    STATUS_500 = Fore.YELLOW
    STATUS_501 = Fore.YELLOW
    STATUS_502 = Fore.YELLOW
    STATUS_503 = Fore.YELLOW


# The main thing starts here!
class Buster:
    def __init__(self, url: str, threads: int, wordlist: str, args) -> None:
        self.url = url
        self.threads = threads
        self.wordlist = wordlist

        self.args = args
        self.results = []

        # Open wordlist
        with open(self.wordlist, "r") as wordlist_file:
            wordlist_data = wordlist_file.read()
            self.parsed_wordlist = wordlist_data.split("\n")

    def _make_request(self, url: str, dir_names):
        for dir_name in dir_names:
            parsed_url = urllib.parse.urljoin(url, dir_name)

            resp = requests.get(parsed_url)

            if resp.status_code == 200:
                if self.args.show_successful:
                    color_println(
                        f"[STATUS: {resp.status_code}] {parsed_url}", getattr(StatusColors, f"STATUS_{resp.status_code}")
                    )
                    self.results.append(parsed_url + "\n")
                else:
                    self.results.append(parsed_url + "\n")

                color_println(
                    f"[STATUS: {resp.status_code}] {parsed_url}",
                    getattr(StatusColors, f"STATUS_{resp.status_code}", Fore.WHITE),
                )

    def start_buster(self):
        color_println("================== ! Starting Buster ! ==================", Fore.BLUE)
        if not self.parsed_wordlist:
            return color_println("- Invalid wordlist provided!", Fore.RED)

        url: str = self.args.url

        if not url.startswith("http://") or not url.startswith("https://"):
            if self.args.secure:
                url = "https://" + url
            else:
                url = "http://" + url

        try:
            parsed_url = urllib3.util.parse_url(url)
        except Exception:
            return color_println("- Invalid URL provided!", Fore.RED)

        session = requests.Session()
        threads = []
        wordlist_chunks = divide_list_into_chunks(self.parsed_wordlist, self.threads)
        for i in range(self.threads):
            try:
                thread = threading.Thread(target=self._make_request, args=(session, url, wordlist_chunks[i]))
                threads.append(thread)

                thread.start()
            except (Exception, IndexError) as e:
                continue

        for idx, thread in enumerate(threads):
            thread.join()

        print("\n================================================\n")
        color_println("Successfully fuzzed all the results!", Fore.GREEN)
        if self.args.file:
            with open(self.args.file, "w") as save:
                for result in self.results:
                    save.write(result)

            color_println(f"\nSuccessfully saved the contents in file: {self.args.file}!", Fore.CYAN)
