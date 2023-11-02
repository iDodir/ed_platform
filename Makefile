up:
	#docker-compose -f docker-compose-local.yaml up -d
	docker-compose up -d

down:
	#docker-compose -f docker-compose-local.yaml down && docker network prune --force
	docker-compose down && docker network prune --force

migrate:
	alembic upgrade head

run:
	docker-compose -f docker-compose-ci.yaml up -d
