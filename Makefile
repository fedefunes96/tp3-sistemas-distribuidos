SHELL := /bin/bash
PWD := $(shell pwd)

all:

docker-image:
	docker build -f ./python_base_image/Dockerfile -t rabbitmq-python-base:0.0.1 .
	docker build -f ./rabbitmq/Dockerfile -t "rabbitmq:latest" .
	docker build -f ./master_controller/Dockerfile -t "master_controller:latest" .
	docker build -f ./map_worker/Dockerfile -t "map_worker:latest" .
	docker build -f ./resume_master_controller/Dockerfile -t "resume_master_controller:latest" .
	docker build -f ./top_cities_controller/Dockerfile -t "top_cities_controller:latest" .
	docker build -f ./cities_resume/Dockerfile -t "cities_resume:latest" .
	docker build -f ./summary_controller/Dockerfile -t "summary_controller:latest" .
	docker build -f ./date_redirector/Dockerfile -t "date_redirector_worker:latest" .
	docker build -f ./dates_resume/Dockerfile -t "dates_resume:latest" .
	docker build -f ./date_sorter/Dockerfile -t "date_sorter:latest" .
	docker build -f ./count_controller/Dockerfile -t "count_controller_worker:latest" .
	docker build -f ./count_summary_controller/Dockerfile -t "count_summary_controller:latest" .
.PHONY: docker-image

client-image:
	docker build -f ./python_base_image/Dockerfile -t rabbitmq-python-base:0.0.1 .
	docker build -f ./chunk_manager/Dockerfile -t "chunk_manager:latest" .
.PHONY: client-image

docker-compose-up: docker-image
	COMPOSE_PARALLEL_LIMIT=20 \
	COMPOSE_PROJECT_NAME=server \
	TOTAL_MAP_WORKERS=$(map_workers) \
	TOTAL_DATE_WORKERS=$(date_workers) \
	TOTAL_COUNT_WORKERS=$(count_workers) \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml up \
	--scale map_worker=$(map_workers) \
	--scale date_redirector_worker=$(date_workers) \
	--scale count_controller_worker=$(count_workers) \
	-d --build
.PHONY: docker-compose-up

client-run: client-image
	COMPOSE_PROJECT_NAME=client \
	SERVER_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-client.yaml up -d --build
.PHONY: client-run

client-stop:
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-client.yaml stop -t 1
	COMPOSE_PROJECT_NAME=client \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-client.yaml down
.PHONY: client-stop

client-logs:
	COMPOSE_PROJECT_NAME=client \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-client.yaml logs -f
.PHONY: client-logs

docker-compose-down:
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml stop -t 1
	COMPOSE_PROJECT_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml down
.PHONY: docker-compose-down

docker-compose-logs:
	COMPOSE_PROJECT_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs
