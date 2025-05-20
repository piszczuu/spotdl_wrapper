from datetime import datetime 
import json
import logging
import os
from time import sleep
from typing import Any
from src.spotdl_wrapper import SpotdlWrapper
from src.visuals import colored_text

def Main() -> None:
    while True:
        try:
            # os.system('cls')
            
            logger = logging.getLogger("PlaylistDownloader")
            if not os.path.exists("logs"):
                os.mkdir("logs")
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s",
                filename=os.path.join("logs", datetime.strftime(datetime.now(), "%Y-%m-%d.log"))
            )
            logger.info("Start of playlist download")

            SETTINGS = {}
            spotdl = SpotdlWrapper(settings=SETTINGS, logger=logger)

            try:
                with open(os.path.join("data", "settings.json")) as f:
                    SETTINGS = json.load(f)
            except FileNotFoundError:
                colored_text("Settings not found - using default", "white", "normal")
            sleep(1)
            # os.system('cls')
            ascii_art = r'''
   ____          __  ___  __     _      __                          
  / __/__  ___  / /_/ _ \/ /    | | /| / /______ ____  ___  ___ ____
 _\ \/ _ \/ _ \/ __/ // / /__   | |/ |/ / __/ _ `/ _ \/ _ \/ -_) __/
/___/ .__/\___/\__/____/____/   |__/|__/_/  \_,_/ .__/ .__/\__/_/   
   /_/                                         /_/  /_/             
            '''

            colored_text("Playlist downloader Spotify/Youtube", "green", "bright")
            colored_text(ascii_art, "green", "dim")


            playlist_count = spotdl.get_playlist_count()
            playlist_urls = spotdl.get_playlist_urls(playlist_count)


            for i, url in enumerate(playlist_urls, 1):
                colored_text(f"\nStarting downloading {i}/{playlist_count}", "white", "bright")
                spotdl(url) 
                colored_text(f" Finished downloading {i}/{playlist_count}", "green", "bright")

            colored_text("\nAll playlist downloaded successfully!", "green", "bright")

        except KeyboardInterrupt:
            colored_text("\nError, downloading interrupted.", "red", "bright")
            break

if __name__ == '__main__':
    while True:
        try:
            Main()
            retry = input("\nDownload more? (Y/N)\n> ").strip().lower()
            if retry not in ("y", "yes"):
                print("Program finished.")
                break
        except KeyboardInterrupt:
            colored_text("\nExiting..", "red", "bright")
            break
