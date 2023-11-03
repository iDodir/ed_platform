up:
	docker-compose -f docker-compose-local.yaml up -d

down:
	docker-compose -f docker-compose-local.yaml down && docker network prune --force

migrate:
	alembic upgrade head

run:
	docker-compose -f docker-compose-ci.yaml up -d

sentry_run:
	#docker-compose run --rm sentry config generate-secret-key
	docker-compose up -d
	docker-compose restart sentry
