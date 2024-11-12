nvm:
	. ${NVM_DIR}/nvm.sh && nvm use 22.11.0

npm_version:
	@echo "npm version:" $(shell npm -v)

rebuild_frontend:
	make nvm
	cd radio_console/frontend/svelte/radio && npm run build

build:
	$(MAKE) rebuild_frontend
	docker-compose up --build

build_d:
	$(MAKE) rebuild_frontend
	docker-compose up --build -d

exec:
	docker exec -it $(C) bash


update_mirror:
	cd ../radio-mirror && git fetch -p origin && git push --mirror github