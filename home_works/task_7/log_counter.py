import re
import sys
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Union

def parse_log_line(line: str) -> dict:
    preparsed_line = re.match(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([A-Z]+)\s+(.+)", line)

    return {
        "timestamp": preparsed_line.group(1),
        "level": preparsed_line.group(2),
        "message": preparsed_line.group(3)
    }

def load_logs(file_path: Union[str, PathLike]) -> list:
    return [parse_log_line(line) for line in Path(file_path).read_text().splitlines()]

def get_log_levels(logs: list) -> set:
    return {entry["level"] for entry in logs}

def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log["level"] == level]

def count_logs_by_level(logs: list) -> dict:
    levels = get_log_levels(logs)

    return {level: len(filter_logs_by_level(logs, level)) for level in levels}

def display_log_counts(counts: dict) -> None:
    log_level_title = "Рівень логування"
    amount_title = "Кількість"
    log_level_title_len = len(log_level_title) + 2
    amount_title_len = len(amount_title) + 2
    row_border = f"{'-' * (amount_title_len + log_level_title_len)}\n"

    table_model = StringIO()
    table_model.write(row_border)
    table_model.write(f"{log_level_title.center(2)}")
    table_model.write(f"|")
    table_model.write(f"{amount_title.center(2)}\n")
    table_model.write(row_border)
    for level in counts:
        table_model.write(f"{level}{' ' * (log_level_title_len - len(level) - 2)}")
        table_model.write(f"|")
        table_model.write(f"{str(counts[level]).center((amount_title_len - len(str(counts[level]))) // 2)}\n")
        table_model.write(row_border)

    print(table_model.getvalue())

def main()-> None:
    if len(sys.argv) < 2:
        raise ValueError(f"Вкажіть шлях до логу: {__file__} /path/to/log.log")

    log_path = sys.argv[1]

    logs = load_logs(log_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

if __name__ == '__main__':
    main()
