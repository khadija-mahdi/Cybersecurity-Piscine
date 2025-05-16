#!/usr/bin/env python3

import random
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import time
import argparse
import os
import hashlib

index = 0
visited = set()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Web spider to download images.')
    parser.add_argument('-r', action='store_true',
                        help='Enable recursive download.', required=True)
    parser.add_argument('-l', '--limit', type=int, default=5,
                        help='Maximum depth level for recursion.')
    parser.add_argument('-p', '--path', type=str, default='data/',
                        help='Path to save downloaded images.')
    parser.add_argument('url', help='The URL to start the spider.')
    return parser.parse_args()


def handle_saving_image(url, folder):
    global index
    try:
        response = requests.get(url)
        response.raise_for_status()
        if 'Content-Type' in response.headers:
            image_type = response.headers['Content-Type'].split('/')[1]
            if(image_type == 'jpeg' or image_type == 'jpg' or image_type == 'png' or image_type == 'gif' or image_type == 'bmp' ):
                file_name = os.path.join(folder, f'image_{index}.{image_type}')
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                print(f'Image {index} saved as {file_name}')
                index += 1
    except Exception as e:
        pass


def getDepth(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    if response.status_code != 200:
        return None
    return url


def get_images_url(url, folder, depth):
    global visited
    if depth == 0:
        exit()
    visited.add(url)
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        if 'Content-Type' in response.headers and response.headers['Content-Type'].startswith('image/'):
            handle_saving_image(url, folder)
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if img_url:
                absolute_url = urljoin(url, img_url)
                handle_saving_image(absolute_url, folder)
        for link_tag in soup.find_all('a', href=True):
            link_url = link_tag.get('href')
            full_url = urljoin(url, link_url)
            next_url = getDepth(full_url)
            if next_url and next_url not in visited:
                get_images_url(next_url, folder, depth - 1)

    except requests.exceptions.RequestException as e:
        return

if __name__ == '__main__':
    main() not os.path.exists(args.path):
            os.makedirs(args.path)
        get_images_url(args.url, args.path, args.limit)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()