import io
import shutil
import tempfile
import zipfile
from pathlib import Path

import pandas as pd
import requests


def coroutine(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)              # автоматично запускаємо генератор
        return gen
    return wrapper

def download_zip_to_memory(url: str, timeout=(5, 60)) -> io.BytesIO:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DataFetch/1.0)",
        "Accept": "application/octet-stream",
    }
    resp = requests.get(url, stream=True, timeout=timeout, headers=headers)
    if not resp.ok:
        raise RuntimeError(f"Download failed: HTTP {resp.status_code} - {resp.reason}")

    buf = io.BytesIO()
    sig_checked = False
    signature_ok = False

    for chunk in resp.iter_content(chunk_size=1024 * 64):
        if not chunk:
            continue
        if not sig_checked:
            # ZIP локальний заголовок: PK\x03\x04
            signature_ok = chunk[:4] == b"PK\x03\x04"
            sig_checked = True
        buf.write(chunk)

    buf.seek(0)

    # Якщо Content-Type підозрілий і сигнатура не збіглась — явно сигналізуємо
    content_type = resp.headers.get("Content-Type", "")
    if ("zip" not in content_type.lower()) and (not signature_ok):
        # Іноді GitHub віддає HTML помилки чи сторінки rate limit
        # Покажемо невеликий фрагмент для діагностики
        preview = buf.getvalue()[:200].decode("utf-8", errors="replace")
        raise RuntimeError(
            "Downloaded file is not a ZIP (content-type mismatch and signature failed). "
            f"Content-Type: {content_type or 'n/a'}; Preview: {preview}"
        )

    return buf

def safe_extract_all(zf: zipfile.ZipFile, dest_dir: Path) -> list[str]:
    # Проста безпечна розпаковка, що не допускає вихід за межі папки призначення
    extracted = []
    for info in zf.infolist():
        # Нормалізуємо шлях
        target = dest_dir.joinpath(Path(info.filename)).resolve()
        if not str(target).startswith(str(dest_dir.resolve())):
            # Захист від Zip Slip
            continue
        if info.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(info, "r") as src, open(target, "wb") as dst:
            dst.write(src.read())
        extracted.append(str(target))
    return extracted

def load_dataset(url: str, load_file_name: str) -> pd.DataFrame:
    buf = download_zip_to_memory(url)
    with zipfile.ZipFile(buf) as zf:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            extracted_paths = safe_extract_all(zf, tmp_path)

            # Спробуємо знайти конкретний файл, інакше — перший CSV
            target = None
            for p in extracted_paths:
                if p.endswith(load_file_name):
                    target = p
                    break
            if target is None:
                csvs = [p for p in extracted_paths if p.lower().endswith(".csv")]
                if not csvs:
                    raise FileNotFoundError("No CSV files found in the ZIP archive.")
                target = csvs[0]

            df = pd.read_csv(target, header=0)

            shutil.rmtree(tmpdir)
            return df
