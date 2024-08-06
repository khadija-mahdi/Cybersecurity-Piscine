#!/usr/bin/env python3

import time
import argparse
from cryptography.fernet import Fernet


def parse_args():
    parser = argparse.ArgumentParser(
        description='Store a password securely and generate one-time passwords.')
    parser.add_argument('-g', '--generate', type=str,
                        help='Generate a key and store it in a file called ft_otp.key')
    parser.add_argument('-k', '--key', type=str,
                        help='Generate a new temporary password based on the key given as argument and prints it on the standard output.')
    return parser.parse_args()

def get_generate_key(key):
    encryptedKey = ''
    if key:
        try :
            if len(key) >= 64 and all(c in '0123456789abcdef' for c in key):
                encryptedKey =  key
            else :
                with open(key, 'r') as source_file:
                    content = source_file.read()
                encryptedKey = content
            
        except Exception as e:
            print(f'error: key must be 64 hexadecimal characters.')
            exit()
            
        return 

def main():
    args = parse_args()
    key = get_generate_key(args.generate)
    print(key)





if __name__ == '__main__':
    main()
