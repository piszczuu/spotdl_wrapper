from datetime import datetime 
import json
import logging
import os
from time import sleep
from typing import Any
from src.spotdl_wrapper import SpotdlWrapper
from src.spotdl_wrapper import colored_text

def Main() -> None:
    try:
        os.system('cls')

        logger: logging.Logger = logging.getLogger("FileOrganizer")
        if not os.path.exists("logs"):
            os.mkdir("logs")

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=os.path.join("logs", datetime.strftime(datetime.now(), format="%Y-%m-%d.log"))
        )
        logger.info("Logger initialized")


        SETTINGS: dict[str, Any] = {}
        try:
            with open(os.path.join("data", "settings.json")) as f:
                SETTINGS = json.load(f)
        except FileNotFoundError:
            print
            colored_text("Settings not found, using default settings", "red", "normal")


        sleep(1)
        os.system('cls')
        ascii = r'''
        
   ____          __     ____  _      __                          
  / __/__  ___  / /____/ / / | | /| / /______ ____  ___  ___ ____
 _\ \/ _ \/ _ \/ __/ _  / /  | |/ |/ / __/ _ `/ _ \/ _ \/ -_) __/
/___/ .__/\___/\__/\_,_/_/   |__/|__/_/  \_,_/ .__/ .__/\__/_/   
   /_/                                      /_/  /_/             

                        
       '''

        colored_text('Welcome to my cli playlist downloader', "green", "bright")
        colored_text(ascii, "green", "dim")
        
        spotdl_wrapper: SpotdlWrapper = SpotdlWrapper(settings=SETTINGS, logger=logger)

        while True:
            url: str = input('Paste playlist url:\n> ').strip()
            spotdl_wrapper(url)


    except KeyboardInterrupt:
            print("\nExiting...")



if __name__ == '__main__':
    while True:
        Main()
        try:
            retry = input("Try again? Yes(y) / No(q):\n> ").strip().lower()
            if retry not in ("y", "yes"):
                print(" Exiting.")
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
