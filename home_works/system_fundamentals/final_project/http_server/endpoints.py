import json
import logging
from io import StringIO
import html

from http_parts import return_content, compose_page, return_status
from non_routed_pages import internal_server_error
from socket_client import SocketClient
from util import route


async def get_post_data(req_or_data):
    # Якщо це вже розпарсені дані (dict/MultiDict тощо) — просто повертаємо їх
    if not (hasattr(req_or_data, "headers") and hasattr(req_or_data, "json")):
        return req_or_data

    # Приймаємо лише application/json
    content_type = (req_or_data.headers.get("content-type") or "").lower()
    if "application/json" not in content_type:
        return return_status(
            415, "unsupported content-type, expected application/json".encode("utf-8")
        )
    try:
        return await req_or_data.json()
    except Exception:
        return return_status(400, "invalid request body".encode("utf-8"))


@route(path="/", method="GET")
async def index_endpoint():
    return return_content(
        compose_page(title="Реєстрація", part_name="login_part"), status=200
    )


@route(path="/home", method="GET")
async def home_endpoint(data):
    user = data.get("username")[0].strip() if data.get("username") else ""

    index_page = compose_page(
        title="Старт", part_name="index_part", subpage_substitutions={"username": user}
    )

    return return_content(index_page, status=200)


@route(path="/messages", method="GET")
async def messages_endpoint():
    return return_content(
        compose_page(title="Вислати повідомлення", part_name="message_part"), status=200
    )


@route(path="/login", method="POST")
async def login_endpoint(data):
    user = (data.get("username") or "").strip()

    index_page = compose_page(
        title="Старт", part_name="index_part", subpage_substitutions={"username": user}
    )

    return return_content(index_page, status=200)


@route(path="/send_message", method="POST")
async def send_message(data):
    message = (data.get("message") or "").strip()
    user = (data.get("username") or "").strip()
    if not user:
        return return_status(400, "user is not found".encode("utf-8"))
    if not message:
        return return_status(400, "message is not found".encode("utf-8"))

    sock_client = SocketClient()
    await sock_client.connect()

    message = {"user": user, "message": message}
    request = {"request": "send_message", "data": message}

    response = await sock_client.send_request(request)

    if "mongo error" in response or "Error in callback" in response:
        return return_status(500, response.encode("utf-8"))
    elif "Validation error in send_message" in response:
        return return_status(400, response.encode("utf-8"))

    # Тут можна виконати збереження повідомлення або іншу бізнес-логіку
    return return_status(200, "ok".encode("utf-8"))


@route(path="/search_messages", method="GET")
async def search_messages(data):
    if not "q" in data:
        return internal_server_error()

    sock_client = SocketClient()
    await sock_client.connect()
    search_pattern = data["q"][0]
    search_query = {"message": {"$regex": f".*{search_pattern}.*"}}
    request = {"request": "find_messages", "data": search_query}
    sock_response = await sock_client.send_request(request)
    logging.info(f"sock_response: {sock_response}")
    response = json.loads(sock_response)
    if "mongo error" in response:
        return return_status(500, response.encode("utf-8"))
    elif "Error in callback" in response:
        return return_status(500, response.encode("utf-8"))

    if response:
        table_opening = """<section class="table-section">
  <h2>Знайдені повідомлення</h2>

  <div class="table-wrapper" style="overflow:auto">
    <table class="sortable-table" aria-describedby="tableHelp">
      <caption id="tableHelp" style="text-align:left">
        Клікніть по заголовку стовпця, щоб відсортувати. Натискайте знову для зміни напрямку.
      </caption>
      <thead>
        <tr>
          <th scope="col" data-type="date" tabindex="0" aria-sort="none">Створено</th>
          <th scope="col" data-type="string" tabindex="0" aria-sort="none">Користувач</th>
          <th scope="col" data-type="string" tabindex="0" aria-sort="none">Повідомлення</th>
        </tr>
      </thead>
      <tbody>
"""
        table_closing = """</tbody>
    </table>
  </div>
  <script>
    (function() {
      const table = document.querySelector('.sortable-table');
      if (!table || !table.tHead) return;

      // Перевага data-value, якщо задано, інакше беремо текст
      const getCellValue = (row, index) => {
        const cell = row.children[index];
        if (!cell) return '';
        const data = cell.getAttribute('data-value');
        const raw = (data ?? cell.textContent ?? '').trim();
        return raw;
      };

      // Більш надійний парсер значень
      const parseValue = (val, type) => {
        if (type === 'number') {
          const cleaned = val
            .replace(/\\s+/g, '')
            .replace(/[^0-9+\\-.,]/g, '')
            .replace(',', '.');
          const num = parseFloat(cleaned);
          return isNaN(num) ? Number.NEGATIVE_INFINITY : num;
        }
        if (type === 'date') {
          let t = Date.parse(val);
          if (!isNaN(t)) return t;

          const dm = val.match(/^(\\d{1,2})\\.(\\d{1,2})\\.(\\d{4})(?:[ T](\\d{1,2}):(\\d{2})(?::(\\d{2}))?)?$/);
          if (dm) {
            const [ , d, m, y, hh='0', mm='0', ss='0'] = dm;
            const dt = new Date(Number(y), Number(m)-1, Number(d), Number(hh), Number(mm), Number(ss));
            t = dt.getTime();
            if (!isNaN(t)) return t;
          }

          const ym = val.match(/^(\\d{4})-(\\d{1,2})-(\\d{1,2})(?:[ T](\\d{1,2}):(\\d{2})(?::(\\d{2}))?)?$/);
          if (ym) {
            const [ , y, m, d, hh='0', mm='0', ss='0'] = ym;
            const dt = new Date(Number(y), Number(m)-1, Number(d), Number(hh), Number(mm), Number(ss));
            t = dt.getTime();
            if (!isNaN(t)) return t;
          }

          return -8640000000000000;
        }
        return (val || '').toLowerCase();
      };

      const setAriaSort = (ths, activeIndex, dir) => {
        ths.forEach((th, i) => {
          th.setAttribute('aria-sort', i === activeIndex ? (dir > 0 ? 'ascending' : 'descending') : 'none');
        });
      };

      const ths = Array.from(table.tHead.querySelectorAll('th[scope="col"]'));
      if (!ths.length) return;

      const onActivate = (th) => {
        const idx = ths.indexOf(th);
        if (idx === -1) return;

        const tbody = table.tBodies[0];
        const rows = Array.from(tbody.querySelectorAll('tr'));
        if (!rows.length) return;

        const type = th.getAttribute('data-type') || 'string';
        const currentSort = th.getAttribute('aria-sort');
        const dir = currentSort === 'ascending' ? -1 : 1;

        const indexed = rows.map((r, i) => ({ r, i }));

        indexed.sort((a, b) => {
          const av = parseValue(getCellValue(a.r, idx), type);
          const bv = parseValue(getCellValue(b.r, idx), type);
          if (av < bv) return -1 * dir;
          if (av > bv) return 1 * dir;
          return a.i - b.i;
        });

        const frag = document.createDocumentFragment();
        indexed.forEach(({ r }) => frag.appendChild(r));
        tbody.appendChild(frag);

        setAriaSort(ths, idx, dir);
      };

      table.tHead.addEventListener('click', (e) => {
        const th = e.target.closest('th[scope="col"]');
        if (!th || !table.tHead.contains(th)) return;
        onActivate(th);
      });

      table.tHead.addEventListener('keydown', (e) => {
        if (e.key !== 'Enter' && e.key !== ' ') return;
        const th = e.target.closest('th[scope="col"]');
        if (!th || !table.tHead.contains(th)) return;
        e.preventDefault();
        onActivate(th);
      });
    })();
  </script>
</section>
"""
        string_builder = StringIO()
        string_builder.write(table_opening)
        for message in response:
            date_val = str(message.get("date", ""))
            # Безпечний рендеринг значень
            safe_date = html.escape(date_val)
            safe_user = html.escape(str(message.get("user", "")))
            safe_text = html.escape(str(message.get("message", "")))
            # Використовуємо data-value для стабільного сортування і <time> для семантики
            string_builder.write(
                f"<tr>"
                f"<td data-value='{safe_date}'><time datetime='{safe_date}'>{safe_date}</time></td>"
                f"<td>{safe_user}</td>"
                f"<td class='message-cell' title='{safe_text}'>{safe_text}</td>"
                f"</tr>"
            )
        string_builder.write(table_closing)
        result_val = string_builder.getvalue()
    else:
        result_val = "<b>Нічого не знайдено</b>"

    return return_content(
        compose_page(
            title="Результати пошуку",
            part_name="search_results_part",
            subpage_substitutions={"search_results": result_val},
        ),
        status=200,
    )
