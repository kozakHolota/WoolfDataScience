import shutil
from functools import lru_cache
from pathlib import Path

import click

@lru_cache(maxsize=None)
def rcopy_dir(source_dir: Path, target_dir: Path):
    if not target_dir.exists():
        target_dir.mkdir()
    for file in source_dir.iterdir():
        if file.is_dir():
            print(f"Наткнулись на директорію {file}... Рекурсуємо...")
            rcopy_dir(file, target_dir)
        else:
            extension = file.suffix[1:] if file.suffix else ""
            ext_dir = target_dir / extension
            if not ext_dir.exists():
                ext_dir.mkdir()
            try:
                print(f"Копіюємо файл {file} в {ext_dir / file.name}")
                shutil.copy2(file, ext_dir / file.name)
            except FileNotFoundError:
                print(f"Помилка: Файл {file} не знайдено")
            except PermissionError:
                print(f"Помилка: Немає прав доступу до {file} або {ext_dir / file.name}")
            except shutil.SameFileError:
                print(f"Помилка: {file} та {ext_dir / file.name} - це один і той самий файл")

@click.command()
@click.option("--src_dir", help="Source directory", required=True)
@click.option("--dst_dir", help="Destination directory", required=True)
def main(src_dir: str, dst_dir: str):
    rcopy_dir(
        Path(src_dir),
        Path(dst_dir)
    )

if __name__ == "__main__":
    main()