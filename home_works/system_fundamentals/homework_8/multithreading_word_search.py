import multiprocessing
import queue
import re
import threading
from copy import copy
from pathlib import Path
from timeit import timeit

import click

class Counter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def inc(self, n=1):
        with self._lock:
            self.value += n


def worker(
        files_q: queue.Queue,
        words: tuple[str],
        result_dict: dict,
        lock: threading.Lock
):
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
            for word in words:
                pattern = re.compile(r"\b" + word + r"\b")
                occurrences = len(pattern.findall(txt))
                if occurrences:
                    print(f"Слово '{word}' знайдено у файлі '{file}' потоком {name}: {ident}")
                    # Читаємо-оновлюємо-записуємо цілий об’єкт під локом
                    with lock:
                        d = result_dict.get(word)
                        if d is None:
                            d = {"findings": [], "count": 0}
                        d["findings"].append({"path": file, "occurrences": occurrences})
                        d["count"] += occurrences
                        result_dict[word] = d
        except Exception:
            continue


@click.command()
@click.option("--n", default=10, help="Number of processes")
@click.option("--input_dir", help="Input directory")
@click.argument("words", nargs=-1, required=True)
def main(n: int, input_dir: str, words: tuple[str]):
    search_dir = Path(input_dir)
    result_dict = {}
    lock = threading.Lock()

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
        t = threading.Thread(target=worker, args=(files_q, copy(words), result_dict, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Вивід результатів
    for w in words:
        data = result_dict.get(w)
        print(10 * "=")
        print(f"Слово '{w}' по файлах")
        print(10 * "=")
        if data:
            for finding in data["findings"]:
                print(f"{finding['path']}: {finding['occurrences']}")
            print(10 * "=")
            print(f"Слово '{w}': {data['count']}")
        else:
            print("Нічого не знайдено")
        print(10 * "=")

if __name__ == "__main__":
    execution_time = timeit(lambda: main(standalone_mode=False), number=1)
    print(f"Пошук виконувався {execution_time} секунд")