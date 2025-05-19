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
        platform: str = ""

        if url.find("youtube") != -1:
            platform = "youtube"
        elif url.find("spotify") != -1:
            platform = "spotify"

        path = os.path.join(self.outputPath, platform)

        skip_album_art = "--skip-album-art" if self.skipAlbumArt else ""
        print_errors = "--print-errors" if self.printErrors else ""

        command = f"python -m spotdl download {url} --bitrate {self.bitrate} --format {self.format} {skip_album_art} {print_errors} --overwrite {self.overwrite} --threads {self.threads} --output {path}"

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


if __name__ == "__main__":
    pass