#!/usr/bin/env python3
import argparse
from PIL import Image
import piexif
import os
from datetime import datetime

CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}

def parse_args():
    parser = argparse.ArgumentParser(description="Scorpion: Image Metadata Extractor")
    parser.add_argument("files", metavar="FILE", type=str, nargs="+",
                        help="Image files to parse metadata from")
    return parser.parse_args()

def is_supported(file_path):
    _, ext = os.path.splitext(file_path.lower())
    return ext in SUPPORTED_EXTENSIONS

def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)
        creation_time = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        file_size_kb = file_stats.st_size // 1024
        return {
            "Creation Date": creation_time,
            "Modification Date": modification_time,
            "File Size (KB)": file_size_kb
        }
    except Exception as e:
        print(f"{RED}Error retrieving file metadata for {file_path}: {e}{RESET}")
        return {}

def display_exif_data(exif_data):
    if exif_data:
        print(f"  {GREEN}- EXIF Data:{RESET}")
        for tag, value in exif_data.items():
            tag_name = piexif.TAGS.get(tag, {}).get("name", tag)
            print(f"      {CYAN}{tag_name}:{RESET} {value}")
    else:
        print(f"  {RED}- No EXIF data found.{RESET}")

def display_metadata(file_path):
    try:
        with Image.open(file_path) as img:
            print(f"\n{YELLOW}Metadata for {file_path}:{RESET}")
            print(f"  {CYAN}- Format:{RESET} {img.format}")
            print(f"  {CYAN}- Dimensions:{RESET} {img.size[0]}x{img.size[1]} pixels")
            print(f"  {CYAN}- Mode:{RESET} {img.mode}")

            file_metadata = get_file_metadata(file_path)
            for key, value in file_metadata.items():
                print(f"  {CYAN}- {key}:{RESET} {value}")
            
            exif_data = img._getexif()
            display_exif_data(exif_data)
    except Exception as e:
        print(f"{RED}Error reading {file_path}:{RESET} {e}")

def main():
    args = parse_args()
    for file in args.files:
        if is_supported(file):
            display_metadata(file)
        else:
            print(f"{RED}File {file} has an unsupported format and will be skipped.{RESET}")

if __name__ == "__main__":
    main()
