#export DOCKER_DEFAULT_PLATFORM=linux/amd64

up:
	docker-compose -f docker-compose-local.yaml up -d

down:
	docker-compose -f docker-compose-local.yaml down --remove-orphans

up_ci:
	docker-compose -f docker-compose-ci.yaml up -d

up_ci_rebuild:
	docker-compose -f docker-compose-ci.yaml up --build -d

down_ci:
	docker-compose -f docker-compose-ci.yaml down --remove-orphans

migrate:
	alembic upgrade head

up_sentry:
	#docker-compose run --rm sentry config generate-secret-key
	docker-compose up -d
	docker-compose restart sentry
