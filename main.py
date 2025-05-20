from datetime import datetime 
import json
import logging
import os
from time import sleep
from typing import Any
from src.spotdl_wrapper import SpotdlWrapper

def Main() -> None:
    try:
        os.system('cls')
        
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
        try:
            with open(os.path.join("data", "settings.json")) as f:
                SETTINGS = json.load(f)
        except FileNotFoundError:
            SpotdlWrapper.colored_text("Settings not found - using default", "white", "normal")

        sleep(1)
        os.system('cls')
        ascii_art = r'''
   ____          __     ____  _      __                          
  / __/__  ___  / /____/ / / | | /| / /______ ____  ___  ___ ____
 _\ \/ _ \/ _ \/ __/ _  / /  | |/ |/ / __/ _ `/ _ \/ _ \/ -_) __/
/___/ .__/\___/\__/\_,_/_/   |__/|__/_/  \_,_/ .__/ .__/\__/_/   
   /_/                                      /_/  /_/             
        '''
        SpotdlWrapper.colored_text("Playlist downloader Spotify/Youtube", "green", "bright")
        SpotdlWrapper.colored_text(ascii_art, "green", "dim")

        playlist_count = SpotdlWrapper.get_playlist_count()
        playlist_urls = SpotdlWrapper.get_playlist_urls(playlist_count)

        spotdl = SpotdlWrapper(settings=SETTINGS, logger=logger)

        for i, url in enumerate(playlist_urls, 1):
            SpotdlWrapper.colored_text(f"\nStarting downloading {i}/{playlist_count}", "white", "bright")
            spotdl(url) 
            SpotdlWrapper.colored_text(f" Finished downloading {i}/{playlist_count}", "green", "bright")

        SpotdlWrapper.colored_text("\nAll playlist downloaded successfully!", "green", "bright")

    except KeyboardInterrupt:
        SpotdlWrapper.colored_text("\nError, downloading interrupted.", "red", "bright")

if __name__ == '__main__':
    while True:
        Main()
        retry = input("\nDownload more? (Y/N): ").strip().lower()
        if retry not in ("y", "yes"):
            SpotdlWrapper.colored_text("Program finished.", "white", "bright")
            break