import multiprocessing
import re
from multiprocessing import Process, current_process
from pathlib import Path

import click


def worker(files_q: multiprocessing.Queue, word: str, count: multiprocessing.Value, lock: multiprocessing.Lock):
    """Процес-робітник: бере файли з черги та рахує входження слова."""
    pid = current_process().pid
    name = current_process().name

    pattern = re.compile(rf"\b{re.escape(word.lower())}\b")
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
                print(f"Слово '{word}' знайдено у файлі '{file}' {occurrences} разів. Процес {name} ({pid}).")
            with lock:
                count.value += occurrences
        except Exception:
            # Пропускаємо проблемні файли, щоб не ламати весь процес
            continue

@click.command()
@click.option("--n", default=10, help="Number of processes")
@click.option("--input_dir", help="Input directory")
@click.option("-s", help="word to search")
def main(n: int, input_dir: str, s: str):
    search_dir = Path(input_dir)
    if not search_dir.exists():
        raise ValueError(f"Директорії {input_dir} не існує")
    if not search_dir.is_dir():
        raise ValueError(f"Шлях {input_dir} не директорія")

    files_q = multiprocessing.Queue()
    for file in search_dir.iterdir():
        if file.is_file():
            files_q.put(str(file))

    count = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    processes = []
    for _ in range(n):
        pr = Process(target=worker, args=(files_q, s, count, lock))
        pr.start()
        processes.append(pr)

    for pr in processes:
        pr.join()

    print(f"Слово '{s}' знайдено {count.value} раз(и) в папці '{input_dir}'")
    
if __name__ == "__main__":
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        pass
    main()
