test:
	pytest test/

install:
	poetry install

run:
	poetry run python -m main

# キャッシュの消去
clear:
	rm -rf ./cache