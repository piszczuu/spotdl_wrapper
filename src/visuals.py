from colorama import Fore, Style


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