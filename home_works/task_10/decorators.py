def params_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError):
            return False, f"Incorrect arguments to the command. Seecommand usage:\n {func.__doc__}"
    return wrapper