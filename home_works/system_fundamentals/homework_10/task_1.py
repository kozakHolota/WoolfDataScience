"""Module for processing files and organizing them by extensions."""

import asyncio
import shutil
from datetime import datetime
from pathlib import Path
from typing import Union

import click


class FolderReader:
    """Class for reading folders and organizing files by extensions."""

    def __init__(self) -> None:
        """Initialize FolderReader with initial timestamp and counters."""
        self.init_timestamp = datetime.now().timestamp()
        self.folders_count = 0
        self.files_count = 0

    def _ensure_directory_exists(self, directory: Path) -> None:
        """Create directory if it doesn't exist.
        
        Args:
            directory: Path to directory that needs to be created.
        """
        if not directory.exists():
            directory.mkdir(parents=True)

    async def write_file(self, file_path: Path, output_folder: Path) -> None:
        """Copy file to appropriate directory based on extension.
        
        Args:
            file_path: Path to source file.
            output_folder: Path to output directory.
        """
        ext = file_path.suffix[1:] if file_path.suffix else "other"
        target_directory = output_folder / ext

        try:
            self._ensure_directory_exists(target_directory)
            shutil.copy2(file_path, target_directory / file_path.name)
            print(f"Processing file {file_path} done...")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error processing file {file_path}: {e}")

    def collect_files_generator(self, folder_path: Path):
        """Generator for recursively reading files from all subfolders.
        
        Args:
            folder_path: Path to folder to process.
            
        Yields:
            Path: File paths found in the directory tree.
        """
        for item in folder_path.iterdir():
            if item.is_dir():
                self.folders_count += 1
                # Recursively process subdirectories
                yield from self.collect_files_generator(item)
            else:
                self.files_count += 1
                # Return file
                yield item

    async def process_folder(
        self, 
        folder_path: Path, 
        output_folder: Path
    ) -> None:
        """Process all files in folder using generator.
        
        Args:
            folder_path: Path to input folder.
            output_folder: Path to output folder.
        """
        # Use generator for efficient file reading
        for file_path in self.collect_files_generator(folder_path):
            await self.write_file(file_path, output_folder)

        print("=" * 10)
        elapsed_time = datetime.now().timestamp() - self.init_timestamp
        print(
            f"Processed {self.files_count} files in "
            f"{self.folders_count} folders in {elapsed_time:.2f} seconds"
        )


@click.command()
@click.option(
    "--folder_path", 
    required=True, 
    help="Path to folder to read",
    type=click.Path(exists=True, path_type=Path)
)
@click.option(
    "--output_folder", 
    required=True, 
    help="Path to folder to write",
    type=click.Path(path_type=Path)
)
def read_folder_cmd(folder_path: Path, output_folder: Path) -> None:
    """Command line interface for folder processing.
    
    Args:
        folder_path: Path to input folder.
        output_folder: Path to output folder.
    """
    folder_reader = FolderReader()
    asyncio.run(folder_reader.process_folder(folder_path, output_folder))


if __name__ == "__main__":
    read_folder_cmd()  # pylint: disable=no-value-for-parameter