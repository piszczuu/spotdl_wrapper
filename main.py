from datetime import datetime 
import json
import logging
import os
from time import sleep
from typing import Any
from src.spotdl_wrapper import SpotdlWrapper, colored_text

def get_playlist_count() -> int:
    while True:
        try:
            count = int(input("Ile playlist chcesz pobrać?\n> ").strip())
            if count > 0:
                return count
            colored_text("Podaj liczbę większą od 0!", "red", "bright")
        except ValueError:
            colored_text("To nie jest liczba!", "red", "bright")

def get_playlist_urls(count: int) -> list[str]:
    urls = []
    for i in range(1, count + 1):
        while True:
            url = input(f"\nPodaj URL playlisty {i}/{count}:\n> ").strip()
            if "youtube.com" in url or "spotify.com" in url:
                urls.append(url)
                break
            colored_text("URL musi być z YouTube lub Spotify!", "red", "bright")
    return urls

def Main() -> None:
    try:
        os.system('cls')
        
        # Inicjalizacja loggera
        logger = logging.getLogger("PlaylistDownloader")
        if not os.path.exists("logs"):
            os.mkdir("logs")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=os.path.join("logs", datetime.strftime(datetime.now(), "%Y-%m-%d.log"))
        )
        logger.info("Rozpoczęcie pobierania playlist")

        # Ładowanie ustawień
        SETTINGS = {}
        try:
            with open(os.path.join("data", "settings.json")) as f:
                SETTINGS = json.load(f)
        except FileNotFoundError:
            colored_text("Ustawienia nie znalezione - używam domyślnych", "yellow", "normal")

        # Nagłówek programu
        ascii_art = r'''
   ____          __     ____  _      __                          
  / __/__  ___  / /____/ / / | | /| / /______ ____  ___  ___ ____
 _\ \/ _ \/ _ \/ __/ _  / /  | |/ |/ / __/ _ `/ _ \/ _ \/ -_) __/
/___/ .__/\___/\__/\_,_/_/   |__/|__/_/  \_,_/ .__/ .__/\__/_/   
   /_/                                      /_/  /_/             
        '''
        colored_text("Pobieracz playlist YouTube/Spotify", "green", "bright")
        colored_text(ascii_art, "cyan", "dim")

        # Pobranie liczby playlist i URL-i
        playlist_count = get_playlist_count()
        playlist_urls = get_playlist_urls(playlist_count)

        # Inicjalizacja SpotdlWrapper (jeden obiekt dla wszystkich playlist)
        spotdl = SpotdlWrapper(settings=SETTINGS, logger=logger)

        # Pobieranie każdej playlisty
        for i, url in enumerate(playlist_urls, 1):
            colored_text(f"\n▶ Pobieranie playlisty {i}/{playlist_count}...", "magenta", "bright")
            spotdl(url)  # Automatycznie tworzy folder i pobiera
            colored_text(f"✔ Zakończono playlistę {i}/{playlist_count}", "green", "bright")

        colored_text("\nWszystkie playlisty pobrane!", "green", "bright")

    except KeyboardInterrupt:
        colored_text("\nPrzerwano działanie.", "red", "bright")

if __name__ == '__main__':
    while True:
        Main()
        retry = input("\nPobrać kolejne playlisty? (T/N): ").strip().lower()
        if retry not in ("t", "tak", "y", "yes"):
            colored_text("Koniec programu.", "blue", "bright")
            break