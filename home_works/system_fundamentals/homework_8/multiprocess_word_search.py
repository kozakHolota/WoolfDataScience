import multiprocessing
import re
from copy import copy
from multiprocessing import Process, current_process
from multiprocessing.managers import DictProxy
from pathlib import Path
from timeit import timeit

import click


def worker(
        files_q: multiprocessing.Queue,
        lock: multiprocessing.Lock,
        words: tuple[str],
        result_dict: DictProxy
):
    """Процес-робітник: бере файли з черги та рахує входження слів."""
    pid = current_process().pid
    name = current_process().name

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
                    print(f"Слово '{word}' знайдено у файлі '{file}' процесом {name}: {pid}")
                    # Читаємо-оновлюємо-записуємо цілий об’єкт під локом
                    with lock:
                        d = result_dict.get(word)
                        if d is None:
                            d = {"findings": [], "count": 0}
                        d["findings"].append({"path": file, "occurrences": occurrences})
                        d["count"] += occurrences
                        result_dict[word] = d
        except Exception:
            # Пропускаємо проблемні файли, щоб не ламати весь процес
            continue

@click.command()
@click.option("--n", default=10, help="Number of processes")
@click.option("--input_dir", help="Input directory")
@click.argument("words", nargs=-1, required=True)
def main(n: int, input_dir: str, words: tuple[str]):
    search_dir = Path(input_dir)
    if not search_dir.exists():
        raise ValueError(f"Директорії {input_dir} не існує")
    if not search_dir.is_dir():
        raise ValueError(f"Шлях {input_dir} не директорія")

    files_q = multiprocessing.Queue()
    result_dict = multiprocessing.Manager().dict()

    for file in search_dir.iterdir():
        if file.is_file():
            files_q.put(str(file))

    lock = multiprocessing.Lock()

    processes = []
    for _ in range(n):
        pr = Process(target=worker, args=(files_q, lock, copy(words), result_dict))
        pr.start()
        processes.append(pr)

    for pr in processes:
        pr.join()

    # Вивід результатів
    for w in words:
        data = result_dict.get(w)
        print(10*"=")
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
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        pass
    execution_time = timeit(lambda: main(standalone_mode=False), number=1)
    print(f"Пошук виконувався {execution_time} секунд")
