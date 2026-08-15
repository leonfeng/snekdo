.PHONY: lint test

lint:
	ruff check .

format:
	ruff format .

test:
	pytest