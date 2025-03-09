from colorama import init, Fore, just_fix_windows_console, deinit, Style

init()
just_fix_windows_console()

def get_input(prompt: str) -> str:
    return input(Fore.BLUE + prompt + Style.DIM + Style.RESET_ALL)

def output_info(msg: str) -> None:
    print(Fore.GREEN + msg + Style.DIM + Style.RESET_ALL)

def output_error(msg: str) -> None:
    print(Fore.RED + msg + Style.DIM + Style.RESET_ALL)

def deinit_colorama() -> None:
    deinit()

# Decorators
def bot_command(func):
    def wrapper(*args, **kwargs):
        try:
            preliminary_result = func(*args, **kwargs)
            if preliminary_result is None:
                return

            status, result = preliminary_result
            if status:
                output_info(result)
            else:
                output_error(result)
        except (TypeError, ValueError):
            output_error("Incorrect arguments to the command")
            output_info(func.__doc__)

    return wrapper