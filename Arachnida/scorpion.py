#!/usr/bin/env python3
import argparse
from PIL import Image, ExifTags
import exifread
from prettytable import PrettyTable

CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m\033[4m'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Program to add Exif data to images.')
    parser.add_argument('images', nargs='+',
                        help='Images to add Exif data to.')
    return parser.parse_args()


# def ChangeExif(image, key, value):
#     with open(image, 'rb') as r:
#         tags = exifread.process_file(r)

#     tags[key] = value

#     with open(image, 'wb') as w:
#         exifread.write_exif(w, tags)


def ExifImage(image):
    print(f'\n{RED}Exif data for image: {image}{RESET}\n')
    f = open(image, 'rb')
    tags = exifread.process_file(f)
    if tags is None:
        return "{RED}Sorry, no Exif data found For this Image : " + image

    table = PrettyTable()
    table.field_names = [f"{GREEN}Tag{RESET}", f"{GREEN} Value{RESET}"]
    for tag in tags.keys():
        table.add_row([f"{CYAN}{tag}{RESET}", f"{tags[tag]}{RESET}"])
    print(table)


def main():
    args = parse_args()
    for i in range(len(args.images)):
        ExifImage(args.images[i])


if __name__ == '__main__':
    main()
