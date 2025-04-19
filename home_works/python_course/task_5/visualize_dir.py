import sys
from os import PathLike
from pathlib import Path
from typing import Union

from colorama import init, Fore, just_fix_windows_console


def visualize_dir(path: Union[PathLike, str], indent: int=1) -> None:
    init()
    just_fix_windows_console()
    visualizations = {"directory": Fore.BLUE, "file": Fore.RED}
    for item in Path(path).iterdir():
        print(f"{' ' * indent}{visualizations['directory' if item.is_dir() else 'file']}{item.name}")
        if item.is_dir():
            visualize_dir(item, indent + 2)

if __name__ == '__main__':
    visualize_dir(sys.argv[1])
