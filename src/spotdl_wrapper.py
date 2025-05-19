from colorama import Fore, Style, init
import re
import requests
import yt_dlp
from logging import Logger
import os
from typing import Any


class SpotdlWrapper:
    def __init__(self, settings: dict[str, Any], logger: Logger) -> None:
        # self.settings = settings
        self.bitrate = settings.get("bitrate", "160k")
        self.format = settings.get("format","mp3")
        self.skipAlbumArt = settings.get("skip-album-art",False)
        self.printErrors = settings.get("print-errors",False)
        self.overwrite = settings.get("overwrite","skip")
        self.threads = settings.get("threads",8)
        self.outputPath = os.path.join(settings.get("output-path","output"))

        self.logger: Logger = logger
        self.logger.info("SpotdlWrapper initialized")
        self.ensureOutputPath()

    def __call__(self, url:str) -> None:
        """
        downloads song/playlist from url and saves to self.outputPath

        Args:
            url (str): url to song 
        """       

        def get_youtube_playlist_name(url) -> str | None:
            '''
            return youtube playlist name from url via api
            '''
            print('getting playlist name..')
            try:
                ydl_opts = {
                    "quiet": True,  
                    "extract_flat": True, 
                    "playlist_items": "0",
                    "socket_timeout": 3, 
                    "force_generic_extractor": True,
                    "ignoreerrors": True  
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    if info := ydl.extract_info(url, download=False):
                        print('success!')
                        return info.get('title')
            except Exception as e:
                print(f"YouTube error: {type(e).__name__}")
            return None


        def get_spotify_playlist_name(url) -> str | None:
            """
            return spotify playlist name from url via api
            """
            print('getting playlist name..')
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                title_match = re.search(r'<title>(.+?)</title>', response.text)
                
                print('success!')
                return title_match.group(1).replace(" | Spotify", "").strip() if title_match else None
            except Exception as e:
                print(f"Error: {e}")
                return None
            
        platform: str = ""
        playlist_name: str = ""
        output: str = ''

        if url.find("youtube") != -1:
            platform = "youtube"
            playlist_name = get_youtube_playlist_name(url)

        elif url.find("spotify") != -1:
            platform = "spotify"
            playlist_name = get_spotify_playlist_name(url)

        path = os.path.join(self.outputPath, platform, playlist_name)
        output = f'"{os.path.join(path, "{artist} - {title}.mp3")}"'
        # print(output)

        skip_album_art = "--skip-album-art" if self.skipAlbumArt else ""
        print_errors = "--print-errors" if self.printErrors else ""

        command = f"python -m spotdl download {url} --bitrate {self.bitrate} --format {self.format} --overwrite {self.overwrite} --threads {self.threads} --output {output} {skip_album_art} {print_errors}"
        print(command)

        self.logger.debug(f"executing command: {command}")
        os.system(command)


    def ensureOutputPath(self) -> None:
        """
        check if outputPath and spotify/youtube inside exists
        """
         
        if not os.path.exists(self.outputPath):
            self.logger.debug(f"{self.outputPath} doesn't exists, creating")
            os.mkdir(self.outputPath)
            
        for platform in ["spotify", "youtube"]:
            if not os.path.exists(os.path.join(self.outputPath, platform)):
                 self.logger.debug(f"{self.outputPath}/{platform} doesn't exists, creating")
                 os.mkdir(os.path.join(self.outputPath, platform))


init(autoreset=True)
def colored_text(text: str, color: str = 'white', style: str = 'normal') -> None:
    colors = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    styles = {
        "dim": Style.DIM,
        "normal": Style.NORMAL,
        "bright": Style.BRIGHT
    }
    
    color_code = colors.get(color.lower(), Fore.WHITE)
    style_code = styles.get(style.lower(), Style.NORMAL)

    print(style_code + color_code + text + Style.RESET_ALL)


if __name__ == "__main__":
    pass
