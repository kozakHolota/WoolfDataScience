from colorama import init, Fore, just_fix_windows_console, deinit, Style

init()
just_fix_windows_console()

def _get_input(prompt: str) -> str:
    return input(Fore.BLUE + prompt + Style.DIM + Style.RESET_ALL)

def _output_info(msg: str) -> None:
    print(Fore.GREEN + msg + Style.DIM + Style.RESET_ALL)

def _output_error(msg: str) -> None:
    print(Fore.RED + msg + Style.DIM + Style.RESET_ALL)

def _deinit_colorama() -> None:
    deinit()