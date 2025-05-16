# Stockholm

**⚠️ Educational use only! Do not use this on real systems.**

## Description

Stockholm simulates ransomware behavior. It encrypts specific files inside the `~/infection` folder using AES (via Fernet). Encrypted files get a `.ft` extension and can only be restored using the correct key.

## Features

- Works only inside `~/infection`
- Encrypts known WannaCry file types
- Adds `.ft` extension if not already present
- Decrypts with `--reverse` and a valid key
- CLI options:
  - `-h`, `--help` → show help
  - `-v`, `--version` → show version
  - `-r`, `--reverse <key>` → decrypt
  - `-s`, `--silent` → no output


## Usage (via Makefile)

```bash
make run        # Run encryption
make version    # Show version
make help       # Show help
make reverse    # Prompt for key to decrypt
make silent     # Run without output
```

## Notes

- Key is saved in `~/infection/wannaCry.key`
- Only the exact same key can decrypt the files
