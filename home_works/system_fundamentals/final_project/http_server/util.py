_routes: dict[str, callable] = {}


def get_route(path: str):
    """Повертає callable-обробник для шляху або None, якщо не зареєстрований."""
    return _routes.get(path)


def route(path: str, method: str):
    """
    Декоратор для реєстрації обробника маршруту.
    ВАЖЛИВО: повертати оригінальну функцію, щоб не зламати її ім'я у модулі
    та не втратити асинхронність.
    """

    def decorator(func):
        # РЕЄСТРУЄМО ОРИГІНАЛЬНУ ФУНКЦІЮ БЕЗ ОБГОРТОК
        _routes[path] = {"method": method, "callback": func}
        return func  # Повертаємо оригінал, щоб зберегти асинхронність і метадані

    return decorator
