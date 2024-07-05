up_all:
	docker-compose up --build

restart_postgres:
	docker-compose up -d --force-recreate --no-deps --build postgres

restart_api:
	docker-compose up -d --force-recreate --no-deps --build api

restart_ezstream:
	docker-compose up -d --force-recreate --no-deps --build ezstream

restart_icecast:
	docker-compose up -d --force-recreate --no-deps --build icecast

bash_api:
	docker exec -it api bash

bash_ezstream:
	docker exec -it ezstream bash