from pathlib import Path

from aiohttp import web
from string import Template


def compose_page(
    title: str, part_name: str, subpage_substitutions: dict = None
) -> bytes:
    with (
        Path(__file__).parent.joinpath("html/template.html").open(encoding="utf-8") as f
    ):
        template = f.read()
        with (
            Path(__file__)
            .parent.joinpath(f"html/{part_name}.html")
            .open(encoding="utf-8") as p
        ):
            content_raw = p.read()
            if subpage_substitutions:
                content_raw = Template(content_raw).substitute(**subpage_substitutions)
            # Використовуємо Template, щоб не конфліктувати з фігурними дужками у JS/CSS
            content = Template(template).substitute(title=title, content=content_raw)
            return content.encode("utf-8")


def return_content(
    content: bytes, content_type: str = "text/html", status: int = 200
) -> web.StreamResponse:
    resp = web.Response(
        status=int(status),
        body=content,
        content_type=content_type,
        charset="utf-8",
    )
    resp.headers["Connection"] = "close"
    return resp


def return_status(status: int, message: bytes) -> web.StreamResponse:
    resp = web.Response(
        status=int(status),
        body=message,
        content_type="text/plain",
        charset="utf-8",
    )
    resp.headers["Connection"] = "close"
    return resp
