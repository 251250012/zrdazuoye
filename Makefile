.PHONY: run test init-db

run:
	python app.py

test:
	python -m pytest tests/ -v

init-db:
	python -c "from db import init_db; init_db()"