import os, sys
import subprocess

R = '\033[31m'  # Red
W = '\033[0m'   # White
G = '\033[32m'  # Green
Y = '\033[33m'  # Yellow
L = '\033[90m'  # Grey

try:
    import time
    import json
    import random
    from requests import Session
    from concurrent.futures import ThreadPoolExecutor

except ModuleNotFoundError:
    modules = "time json random requests concurrent"
    modules = modules.split()

    for module in modules:
        subprocess.run(["pip", "install", module])


class Discord:
    def __init__(self, tokens, super_properties):
        self.session = Session()
        self.tokens = tokens
        self.super_properties = super_properties
        self.headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "X-Super-Properties": self.super_properties
        }

        self.banner = """
    ____  _          __                               
   / __ \(_)___     / /_  __  ______  ____ ___________
  / /_/ / / __ \   / __ \/ / / / __ \/ __ `/ ___/ ___/
 / ____/ / / / /  / /_/ / /_/ / /_/ / /_/ (__  |__  ) 
/_/   /_/_/ /_/  /_.___/\__, / .___/\__,_/____/____/  
                       /____/_/                       
        """

    def get_message_ids(self, token, limit, channel_id):
        try:
            message_ids = []
            params = {
                "limit": limit
            }

            messages = self.session.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=self.headers, params=params
            ).json()

            for message in messages:
                message_ids.append(message["id"])

            params['before'] = messages[-1]['id']
            return message_ids

        except Exception as e:
            print(e)
            return None

    def pin_message(self, token, limit, channel_id, message_ids, delay):
        for message_id in message_ids:
            try:
                pin = self.session.put(
                    f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}",
                    headers=self.headers
                )
    
                if pin.status_code == 204:
                    print(f"{G}Pinned message{W} -> {message_id}")

                elif pin.status_code == 429:
                    print(f"{Y}Ratelimited{W} -> {token.split('.')[0]}")
                    time.sleep(1)

                else:
                    print(f"{R}Failed{W} -> {pin.json()['message']}")

                time.sleep(delay)

            except Exception as e: print(e)

    def main(self):
        global limit
        limit = 50

        os.system("cls" if os.name=="nt" else "clear")
        print(self.banner)

        try:
            self.set_limit_messages = input("Set message limit (y/n): ").lower()
            if self.set_limit_messages == "y":
                limit = int(input("Limit message 10-100: "))
    
            self.channel_id = int(input("Channel ID: "))
            print(f"{L}Getting {limit} messages ids in channel...")
            token = random.choice(self.tokens)
            message_ids = self.get_message_ids(token, limit, self.channel_id)
            
            print(f"{L}Obtained {len(message_ids)} messages{W}")
            self.threads = int(input(f"Threads 1-{len(tokens)}: "))
            self.delay = input("delay int: ")
            if self.delay == "":
                self.delay = 0
            self.delay = int(self.delay)

        except ValueError:
            print("Invalid option.")
            time.sleep(2)
            return self.main()

        print("\n")

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for token in self.tokens:
                self.headers.update({"authorization": token})
                executor.submit(
                    self.pin_message, token, limit,
                    self.channel_id, message_ids, self.delay
                )

if __name__ == "__main__":
    with open("tokens.txt", "r") as file:
        tokens = file.read().strip().splitlines()

    if len(tokens) < 1:
        print("No tokens in tokens.txt, please insert your tokens")
        sys.exit()

    super_properties = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
    Start = Discord(tokens, super_properties)
    Start.main()
