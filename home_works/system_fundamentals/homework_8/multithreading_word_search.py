import multiprocessing
import queue
import re
import threading
from pathlib import Path

import click

class Counter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def inc(self, n=1):
        with self._lock:
            self.value += n


def worker(files_q: queue.Queue, word: str, count: Counter):
    pattern = re.compile(rf"\b{re.escape(word.lower())}\b")
    name = threading.current_thread().name
    ident = multiprocessing.current_process().ident

    while True:
        try:
            file = files_q.get_nowait()
        except Exception:
            break
        try:
            with Path(file).open("r") as f:
                txt = f.read().lower()
            occurrences = len(pattern.findall(txt))
            if occurrences:
                print(f"Слово '{word}' знайдено у файлі '{file}' {occurrences} разів. Потік "
                      f"{name} ({ident}).")
                count.inc(occurrences)
        except Exception:
            continue


@click.command()
@click.option("--n", default=10, help="Number of processes")
@click.option("--input_dir", help="Input directory")
@click.option("-s", help="word to search")
def main(n: int, input_dir: str, s: str):
    search_dir = Path(input_dir)
    count = Counter()
    if not search_dir.exists():
        raise ValueError(f"Директорії {input_dir} не існує")
    if not search_dir.is_dir():
        raise ValueError(f"Шлях {input_dir} не директорія")

    files_q = queue.Queue()
    for file in search_dir.iterdir():
        if file.is_file():
            files_q.put(str(file))

    threads = []
    for _ in range(n):
        t = threading.Thread(target=worker, args=(files_q, s, count))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"Слово '{s}' знайдено {count.value} раз(и) в папці '{input_dir}'")

if __name__ == "__main__":
    main()