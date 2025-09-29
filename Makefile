# Makefile to manage Docker Compose
.PHONY: up down rebuild logs help

# Run containers in the background
up:
	docker compose up -d

# Stop and delete containers
down:
	docker compose down

# Rebuild and launch containers
rebuild: down
	docker compose up -d --build

# Show logs of all services
logs:
	docker compose logs -f


help:
	@echo "Available Commands:"
	@echo "  make up       - Run containers in the background"
	@echo "  make down     - Stop and delete containers"
	@echo "  make rebuild  - Rebuild and launch containers"
	@echo "  make logs     - Show logs of all services"
