#!/usr/bin/env python3
import argparse
import exifread
import piexif
from PIL import Image
import tkinter as tk
from prettytable import PrettyTable
from tkinter import messagebox
import os

def parse_args():
    parser = argparse.ArgumentParser(
        description='Program to add, modify, or remove Exif data in images.')
    parser.add_argument('images', nargs='+',
                        help='Images to modify Exif data in.')
    return parser.parse_args()

def ExifImage(image):
    print(f'\nExif data for image: {image}\n')
    with open(image, 'rb') as f:
        tags = exifread.process_file(f)
    
    if not tags:
        print(f"Sorry, no Exif data found for image: {image}")
        return None

    table = PrettyTable()
    table.field_names = ["Tag", "Value"]
    for tag in tags.keys():
        table.add_row([tag, tags[tag]])
    print(table)
    return tags

def modify_exif(image_path, updates):
    img = Image.open(image_path)
    exif_dict = piexif.load(img.info.get('exif', b''))

    if not exif_dict:
        print(f"No Exif data found in {image_path}")
        return

    for tag, new_value in updates.items():
        updated = False
        for ifd in exif_dict:
            if tag in exif_dict[ifd]:
                exif_dict[ifd][tag] = new_value.encode()  # Update with new value
                updated = True
                break
        if not updated:
            print(f"Tag {tag} not found in {image_path}")

    exif_bytes = piexif.dump(exif_dict)
    img_format = img.format  # Get the original image format
    img.save(image_path, format=img_format, exif=exif_bytes)
    print(f"Modified Exif data in {image_path}")

def create_table(tags, root, image_path):
    entries = {}
    for i, (tag, value) in enumerate(tags.items()):
        tag_entry = tk.Entry(root, width=30, fg='blue', font=('Arial', 12, 'bold'))
        tag_entry.grid(row=i, column=0)
        tag_entry.insert(tk.END, tag)
        tag_entry.config(state='readonly')
        
        value_entry = tk.Entry(root, width=30, fg='black', font=('Arial', 12))
        value_entry.grid(row=i, column=1)
        value_entry.insert(tk.END, value)

        entries[tag] = value_entry

    def on_done():
        updates = {tag: entry.get() for tag, entry in entries.items()}
        modify_exif(image_path, updates)
        messagebox.showinfo("Done", "Exif data updated successfully!")
        root.destroy()

    done_button = tk.Button(root, text="Done", command=on_done)
    done_button.grid(row=len(tags), columnspan=2, pady=10)

def main():
    args = parse_args()
    
    for image in args.images:
        tags = ExifImage(image)
        if tags:
            root = tk.Tk()
            root.title(f"Exif Data for {image}")
            create_table(tags, root, image)
            root.mainloop()

if __name__ == '__main__':
    main()
