.PHONY: help build up down restart logs test clean

# Makefile for common commands

help:
	@echo "Available commands:"
	@echo "  make build       - Build the Docker containers"
	@echo "  make up          - Start the application"
	@echo "  make down        - Stop and remove containers"
	@echo "  make restart     - Restart the application"
	@echo "  make logs        - View container logs"
	@echo "  make test        - Run tests"
	@echo "  make shell       - Open a shell in the web container"
	@echo "  make migrate     - Run database migrations"
	@echo "  make superuser   - Create a Django superuser"
	@echo "  make clean       - Remove Python cache and compiled files"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

test:
	docker-compose run --rm web pytest

shell:
	docker-compose exec web bash

migrate:
	docker-compose exec web python manage.py migrate

superuser:
	docker-compose exec web python manage.py createsuperuser

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name "*.py,cover" -delete
	rm -rf .coverage htmlcov/
