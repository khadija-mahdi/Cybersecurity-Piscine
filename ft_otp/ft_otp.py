#!/usr/bin/env python3

import time
import argparse
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib
import hmac


def parse_args():
    parser = argparse.ArgumentParser(
        description='Store a password securely and generate one-time passwords.')
    parser.add_argument('-g', '--generate', type=str,
                        help='Generate a key and store it in a file called ft_otp.key')
    parser.add_argument('-k', '--key', type=str,
                        help='Generate a new temporary password based on the key given as argument and prints it on the standard output.')
    return parser.parse_args()


def save_key_and_counter(encrypted_key, counter):
    try:
        with open('ft_otp.sec', 'wb') as f:
            f.write(encrypted_key + b'\n' + str(counter).encode())
    except Exception as e:
        print(f'Error saving key and counter: {e}')
        exit()


def read_key_and_counter():
    try:
        with open('ft_otp.sec', 'rb') as f:
            content = f.read().split(b'\n')
            encrypted_key = content[0]
            counter = int(content[1].decode())
        return encrypted_key, counter
    except FileNotFoundError:
        print("Key file not found. Please generate a key first.")
        exit()
    except Exception as e:
        print(f'Error reading key and counter: {e}')
        exit()


def generate_key(key):
    secret_key = Fernet.generate_key()
    save_key_and_counter(secret_key, counter=0)
    fernet = Fernet(secret_key)
    try:
        if len(key) >= 64 and all(c in '0123456789abcdef' for c in key):
            pass
        else:
            with open(key, 'r') as source_file:
                content = source_file.read()
            key = content
    except:
        print(f'error: key must be 64 hexadecimal characters.')
        exit()
    with open('ft_otp.key', 'wb') as f:
        f.write(fernet.encrypt(key.encode()))
        print("Key was successfully saved in ft_otp.key.")


def ft_hotp(key):
    try:
        fer, counter = read_key_and_counter()
        fernet = Fernet(fer)
        decrypted_key = ''
        with open(key, 'rb') as key_file:
            decrypted_key = fernet.decrypt(key_file.read()).decode()
        if decrypted_key:
            hmac_sha1 = hmac.new(bytes.fromhex(decrypted_key), counter.to_bytes(8, byteorder='big'), hashlib.sha1)
            hmac_result = hmac_sha1.digest()
            offset = hmac_result[-1] & 0x0F
            binary_code = hmac_result[offset:offset + 4]
            binary_code_int = int.from_bytes(binary_code, byteorder='big') & 0x7FFFFFFF
            otp = binary_code_int % 1000000
            print(otp)
            counter += 1
            save_key_and_counter(fer, counter)
    except Exception as e:
        print(f'please generate a key first')
        return


def main():
    args = parse_args()
    if args.generate:
        generate_key(args.generate)
    if args.key:
        ft_hotp(args.key)


if __name__ == '__main__':
    main()
