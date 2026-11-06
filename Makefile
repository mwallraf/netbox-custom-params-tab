.DEFAULT_GOAL := check
.PHONY: env setup build up down logs shell migrate makemigrations check

env:
	@python3 scripts/sandbox.py env

setup:
	@python3 scripts/sandbox.py setup

build:
	@python3 scripts/sandbox.py compose build

up:
	@python3 scripts/sandbox.py compose up -d --wait --wait-timeout 600

down:
	@python3 scripts/sandbox.py compose down

logs:
	@python3 scripts/sandbox.py compose logs --tail 100

shell:
	@python3 scripts/sandbox.py compose exec netbox /bin/bash

migrate:
	@python3 scripts/sandbox.py compose exec -T netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate

makemigrations:
	@python3 scripts/sandbox.py compose exec -T netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py makemigrations netbox_custom_field_profiles

check:
	@python3 -m unittest discover -s tests/sandbox -v
	@python3 scripts/sandbox.py check

.PHONY: test smoke seed seed-check test-legacy reset lifecycle-check test-profiles
test: check smoke seed-check

test-profiles:
	@python3 scripts/test_profiles.py

smoke:
	@python3 scripts/sandbox.py smoke

seed:
	@python3 scripts/sandbox.py seed

seed-check:
	@python3 scripts/sandbox.py seed-check

test-legacy:
	@python3 scripts/legacy_tests.py

reset:
	@python3 scripts/sandbox.py reset

lifecycle-check:
	@python3 scripts/sandbox.py lifecycle-check
