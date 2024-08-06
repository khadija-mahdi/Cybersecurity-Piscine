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
    group = parser.add_argument_group('Exif modification')
    group.add_argument('-k', '--key', type=str, help='Exif key to modify.')
    group.add_argument('-v', '--value', type=str,
                       help='Value for the Exif key.')

    group.required = True
    return parser.parse_args()


# def ChangeExif(image, key, value):
#     with open(image, 'rb') as r:
#         tags = exifread.process_file(r)

#     tags[key] = value

#     with open(image, 'wb') as w:
#         exifread.write_exif(w, tags)


def ExifImage(image, key, value):
    print(f'\n{RED}Exif data for image: {image}{RESET}\n')
    # if value is not None and key is not None:
    #     ChangeExif(image, key, value)
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
        ExifImage(args.images[i], args.key, args.value)


if __name__ == '__main__':
    main()
