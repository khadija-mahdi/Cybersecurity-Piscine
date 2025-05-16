NAME = stockholm.py

run:
	@echo ""
	@echo "🚀 Running $(NAME)..."
	@echo ""
	python3 $(NAME) 

version:
	@python3 $(NAME) -v

help:
	@python3 $(NAME) -h

reverse:
	@read -p "Enter decryption key: " key; \
	python3 $(NAME) -r $$key

silent:
	@python3 $(NAME) -s

all:
	@echo "Available commands:"
	@echo "  make run       → Run the script normally"
	@echo "  make version   → Show version info"
	@echo "  make help      → Show help message"
	@echo "  make reverse   → Prompt for decryption key and run reverse mode"
	@echo "  make silent    → Run in silent mode"
