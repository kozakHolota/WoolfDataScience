from http_parts import return_content, compose_page


def error_page(status: int, title: str, subtitle: str, message: str):
    return return_content(
        content=compose_page(
            title=title,
            part_name="error_part",
            subpage_substitutions={"summary": subtitle, "description": message},
        ),
        status=status,
    )


def non_found_page():
    return error_page(
        status=404,
        title="Не знайдено",
        subtitle="Сторінки не знайдено",
        message="Спробуйте перейти на головну сторінку.",
    )


def method_not_allowed_page():
    return error_page(
        status=405,
        title="Невірний метод запита",
        subtitle="Метод запиту користувача невірний",
        message="Користувач здійснив запит не передбаченим для цього методом. Спробуйте скористатись формою на сторінці",
    )


def internal_server_error():
    return error_page(
        status=500,
        title="Помилка сервера",
        subtitle="Внутрішня помилка сервера",
        message="Щось зламалося в середині веб додатку. Вибачаємось за незручності. Перевантажте сторінку.",
    )
