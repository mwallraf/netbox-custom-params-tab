.DEFAULT_GOAL := help

.PHONY: help build up down restart logs shell nbshell migrate superuser clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Build (or rebuild) the dev Docker image
	docker compose build

up:  ## Start the full stack in the background
	docker compose up -d

down:  ## Stop and remove containers (data volumes are preserved)
	docker compose down

restart:  ## Restart all services
	docker compose restart

logs:  ## Tail logs from all services (Ctrl-C to stop)
	docker compose logs -f

shell:  ## Open a bash shell inside the netbox container
	docker compose exec netbox bash

nbshell:  ## Open NetBox's Django shell_plus inside the netbox container
	docker compose exec netbox python /opt/netbox/netbox/manage.py shell_plus

migrate:  ## Run pending database migrations inside the netbox container
	docker compose exec netbox python /opt/netbox/netbox/manage.py migrate

superuser:  ## Interactively create a Django superuser
	docker compose exec netbox python /opt/netbox/netbox/manage.py createsuperuser

clean:  ## Destroy containers, volumes, and the locally-built image
	docker compose down -v --rmi local
