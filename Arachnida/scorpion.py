#!/usr/bin/env python3
import argparse
import os
import time
from PIL import Image, ExifTags
import exifread
from prettytable import PrettyTable

# ANSI color codes for formatting
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'

def parse_args():
    parser = argparse.ArgumentParser(
        description='Program to parse images for EXIF and metadata information.')
    parser.add_argument('images', nargs='+',
                        help='Images to parse for EXIF and metadata.')
    return parser.parse_args()

# Check if file exists and get its metadata like creation date
def get_file_metadata(image_path):
    if not os.path.isfile(image_path):
        return f"{RED}File not found: {image_path}{RESET}"

    metadata = {}
    metadata['Creation Date'] = time.ctime(os.path.getctime(image_path))
    metadata['File Size (KB)'] = os.path.getsize(image_path) // 1024
    return metadata

# Function to check image format compatibility (e.g., JPEG, PNG, etc.)
def check_image_format(image):
    try:
        img = Image.open(image)
        format = img.format
        return format
    except Exception as e:
        return None

# Extract EXIF data from the image (only for compatible formats like JPEG, TIFF)
def get_exif_data(image):
    try:
        with open(image, 'rb') as f:
            tags = exifread.process_file(f)

        if not tags:
            return f"{RED}No EXIF data found for image: {image}{RESET}"

        # Create a PrettyTable for EXIF data
        table = PrettyTable()
        table.field_names = [f"{GREEN}Tag{RESET}", f"{GREEN}Value{RESET}"]

        for tag in tags.keys():
            table.add_row([f"{CYAN}{tag}{RESET}", f"{tags[tag]}{RESET}"])

        return table
    except Exception as e:
        return f"{RED}Error processing EXIF for {image}: {e}{RESET}"

def process_image(image):
    image_format = check_image_format(image)
    
    if image_format is None:
        return f"{RED}File format not recognized or not supported: {image}{RESET}"
    
    print(f"\n{YELLOW}Processing image: {image}{RESET}\n")
    
    # Get and print basic metadata (creation date, file size)
    metadata = get_file_metadata(image)
    print(f"{GREEN}Basic File Metadata:{RESET}")
    for key, value in metadata.items():
        print(f"{CYAN}{key}: {YELLOW}{value}{RESET}")
    
    # Only try to get EXIF data if format is JPEG or TIFF
    if image_format in ["JPEG", "TIFF"]:
        print(f"\n{GREEN}EXIF Data:{RESET}")
        exif_data = get_exif_data(image)
        print(exif_data)
    else:
        print(f"{RED}{image_format} format does not support EXIF data.{RESET}")

def main():
    args = parse_args()
    for image in args.images:
        process_image(image)

if __name__ == '__main__':
    main()
