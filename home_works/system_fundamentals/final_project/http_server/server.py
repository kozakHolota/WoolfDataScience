import asyncio
import importlib
import inspect
import logging
import sys
from pathlib import Path
from urllib.parse import parse_qs

from aiohttp import web

from non_routed_pages import (
    non_found_page,
    internal_server_error,
    method_not_allowed_page,
)
from util import get_route

# Ініціалізація логування на рівні модуля
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    datefmt="%-Y-%m-%d %H:%M:%S" if sys.platform != "win32" else "%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
# Зменшити шум від aiohttp/asyncio за потреби:
logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def http_dispatch(request: web.Request) -> web.StreamResponse:
    """
    Єдиний HTTP-обробник для всіх шляхів. Визначає реальний метод запиту,
    викликає відповідний callback із реєстру маршрутів і повертає відповідь.
    """
    method = request.method.upper()  # реальний метод із браузера
    path_only = request.path
    logger.info("HTTP %s %s", method, path_only)

    handler = get_route(path_only)
    if handler is None:
        return non_found_page()

    callback = handler.get("callback")
    allowed_method = (handler.get("method") or "GET").upper()

    if not callable(callback):
        logger.error("Route for %s is not callable: %r", path_only, callback)
        return internal_server_error()

    if method != allowed_method:
        return method_not_allowed_page()

    # Підготовка даних для POST-запитів
    post_payload = None
    if method == "POST":
        try:
            if request.content_type == "application/json":
                post_payload = await request.json()
            else:
                # Підійде для application/x-www-form-urlencoded або multipart/form-data
                post_payload = await request.post()
        except Exception:
            logger.exception("Failed to parse POST body for %s", path_only)
            return internal_server_error()

    try:
        # Підтримка як sync, так і async callback-ів
        if inspect.iscoroutinefunction(callback):
            if method == "POST":
                result = await callback(post_payload)
            else:
                query_params = parse_qs(request.query_string, keep_blank_values=True)
                if query_params:
                    result = await callback(query_params)
                else:
                    result = await callback()
        else:
            logger.error("Callback for %s is not async: %r", path_only, callback)
            return internal_server_error()
    except Exception:
        logger.exception("Handler error for %s %s", method, path_only)
        return internal_server_error()

    # Пряме повернення результату callback. Очікуємо aiohttp.web.StreamResponse
    if isinstance(result, web.StreamResponse):
        return result

    logger.error("Unsupported endpoint result type: %r", type(result))
    return internal_server_error()


def create_app() -> web.Application:
    app = web.Application()

    # Імпорт заради побічного ефекту: реєстрації маршрутів через декоратори
    importlib.import_module("endpoints")

    # Статика: CSS/JS/зображення
    base_dir = Path(__file__).parent
    app.router.add_static("/html/", base_dir / "html", show_index=False)
    app.router.add_static("/img/", base_dir / "img", show_index=False)

    # Catch-all HTTP-роут для всіх методів і шляхів
    app.router.add_route("*", "/{tail:.*}", http_dispatch)

    return app


async def _run_app():
    app = create_app()
    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    host = "0.0.0.0"
    port = 3000

    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    logger.info(f"Server is running on http://{host}:{port}")

    # тримаємо процес живим
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(_run_app())
    except KeyboardInterrupt:
        pass
