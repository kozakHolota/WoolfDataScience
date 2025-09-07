def coroutine(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)              # автоматично запускаємо генератор
        return gen
    return wrapper