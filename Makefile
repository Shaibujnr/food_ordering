SHELL := /bin/bash # Use bash syntax

install:
	pip install --upgrade pip && \
	pip install poetry && \
	poetry install

test:
	APP_ENV=test pytest --cov=foodie tests/

testd:
	APP_ENV=test pytest -s --cov=foodie tests/

build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

serve:
	docker-compose up -d && docker-compose logs -f foodie

migrate:
	docker-compose run foodie alembic upgrade head

bash:
	docker-compose run foodie bash


logs:
	docker-compose logs -f

reset:
	docker-compose rm -fsv
