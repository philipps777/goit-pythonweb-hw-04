import asyncio
import argparse
import aiofiles
import shutil
import os
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, output_folder: Path):
    """Copies a file to a folder based on its extension."""
    ext_folder = output_folder / file_path.suffix[1:].lower()
    ext_folder.mkdir(parents=True, exist_ok=True)  

    output_file_path = ext_folder / file_path.name

    try:
        async with aiofiles.open(file_path, 'rb') as src, aiofiles.open(output_file_path, 'wb') as dst:
            await dst.write(await src.read()) 
        logging.info(f'Copied file: {file_path} to {output_file_path}')
    except Exception as e:
        logging.error(f'Error copying file {file_path} to {output_file_path}: {e}')

async def read_folder(source_folder: Path, output_folder: Path):
    """Recursively reads files from the source folder and copies them asynchronously."""
    tasks = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_folder))


    await asyncio.gather(*tasks)  

def parse_args():
    """Argument parser for command-line arguments."""
    parser = argparse.ArgumentParser(description="Asynchronous file sorting by extension")
    parser.add_argument("source_folder", type=str, help="Path to the source folder")
    parser.add_argument("output_folder", type=str, help="Path to the output folder")
    return parser.parse_args()

# class Args:
#     source_folder = "e:/GOIT/Fullstack/source"
#     output_folder = "e:/GOIT/Fullstack/output"

# args = Args()

async def main():
    args = parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("Source folder not found or is not a directory.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
