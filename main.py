from datetime import datetime 
import json
import logging
import os
from typing import Any
from src.spotdl_wrapper import SpotdlWrapper

def Main() -> None:

    logger: logging.Logger = logging.getLogger("FileOrganizer")
    if not os.path.exists("logs"):
        os.mkdir("logs")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=os.path.join("logs", datetime.strftime(datetime.now(), format="%Y-%m-%d.log"))
    )
    logger.info("Logger initialized")

    os.system('cls')
    print("AUDIO DOWNLOADER", end="\n\n")

    SETTINGS: dict[str, Any] = {}
    try:
        with open(os.path.join("data", "settings.json")) as f:
            SETTINGS = json.load(f)
    except FileNotFoundError:
        print("file not found, using default settings")
    
    spotdl_wrapper: SpotdlWrapper = SpotdlWrapper(settings=SETTINGS, logger=logger)

    while True:
        url: str = input('paste url\n')
        # url: str =  "https://open.spotify.com/album/3fG8R9opVLvddvkUQ90feC?si=fb3a5afa5d6f422d"

        spotdl_wrapper(url)

if __name__ == '__main__':
    Main()