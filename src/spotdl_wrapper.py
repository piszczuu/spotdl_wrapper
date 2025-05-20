from colorama import Fore, Style, init
import re
import requests
import yt_dlp as ytdlp
from logging import Logger
import os
from typing import Any

init(autoreset=True)

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
        """       

        def get_youtube_playlist_name(url) -> str | None:
            '''
            return youtube playlist name from url via api
            '''
            print('-> getting playlist name')
            try:
                ydl_opts = {
                    "quiet": True,  
                    "extract_flat": True, 
                    "playlist_items": "0",
                    "socket_timeout": 5, 
                    "force_generic_extractor": True,
                    "ignoreerrors": True  
                }
                with ytdlp.YoutubeDL(ydl_opts) as ydl:
                    if info := ydl.extract_info(url, download=False):
                        print('-> success!')
                        return info.get('title')
            except Exception as e:
                print(f"-> YouTube error: {type(e).__name__}")
            return None

        def get_spotify_playlist_name(url) -> str | None:
            """
            return spotify playlist name from url via api
            """
            print('-> getting playlist name')
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                title_match = re.search(r'<title>(.+?)</title>', response.text)
                
                print('-> success!')
                return title_match.group(1).replace(" | Spotify", "").strip() if title_match else None
            except Exception as e:
                print(f"-> Error: {e}")
                return None
            
        def cleanUrl(url: str) -> str:
            index = url.find('si=')
            if index != -1:
                return url[:index]
            return url

        platform: str = ""
        playlist_name: str = ""
        output: str = ''

        if url.find("youtube") != -1:
            platform = "youtube"
            playlist_name = get_youtube_playlist_name(url)

        elif url.find("spotify") != -1:
            platform = "spotify"
            playlist_name = get_spotify_playlist_name(url)

        skip_album_art = "--skip-album-art" if self.skipAlbumArt else ""
        print_errors = "--print-errors" if self.printErrors else ""

        clean_url: str = cleanUrl(url)

        if platform == "youtube":

            output = os.path.join(self.outputPath, platform, playlist_name.replace(" ", "_"))
            command = f"python -m yt_dlp --output {output} {clean_url}"
            print(command)

        elif platform == "spotify":
            # output = os.path.join(self.outputPath, platform, playlist_name.replace(" ", "_"),"{artist} - {title}.mp3")
            # command = f"python -m spotdl download {clean_url} --bitrate {self.bitrate} --format {self.format} --overwrite {self.overwrite} --threads {self.threads} --output {output} {skip_album_art} {print_errors}"
            output = os.path.join(self.outputPath, platform, playlist_name.replace(" ", "_"), "{artist} - {title}.mp3")
            command = f"python -m spotdl download {clean_url} --bitrate {self.bitrate} --format {self.format} --overwrite {self.overwrite} --threads {self.threads} --output \"{output}\" {skip_album_art} {print_errors}"


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

    @staticmethod
    def get_playlist_count() -> int:
        while True:
            try:
                count = int(input("How many playlists?\n> ").strip())
                if count > 0:
                    return count
                # Użyj self.colored_text jeśli wywołujesz z instancji klasy
                print(Fore.RED + Style.BRIGHT + "Number must be bigger than 0!" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "It must be a number!" + Style.RESET_ALL)

    @staticmethod
    def get_playlist_urls(count: int) -> list[str]:
        urls = []
        for i in range(1, count + 1):
            while True:
                url = input(f"\nPaste url of playlist {i}/{count}:\n> ").strip()
                if "youtube.com" in url or "spotify.com" in url:
                    urls.append(url)
                    break
                print(Fore.RED + Style.BRIGHT + "URL must be from YouTube or Spotify!" + Style.RESET_ALL)
        return urls

    

if __name__ == "__main__":
    pass
