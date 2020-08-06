SHELL := /bin/bash
PWD := $(shell pwd)

all:

docker-image:
	docker build -f ./python_base_image/Dockerfile -t rabbitmq-python-base:0.0.1 .
	docker build -f ./rabbitmq/Dockerfile -t "rabbitmq:latest" .
	docker build -f ./master_controller/Dockerfile -t "master_controller:latest" .
	docker build -f ./map_worker/Dockerfile -t "map_worker:latest" .
	docker build -f ./top_cities_controller/Dockerfile -t "top_cities_controller:latest" .
	docker build -f ./cities_resume/Dockerfile -t "cities_resume:latest" .
	docker build -f ./summary_controller/Dockerfile -t "summary_controller:latest" .
	docker build -f ./date_redirector/Dockerfile -t "date_redirector_worker:latest" .
	docker build -f ./dates_resume/Dockerfile -t "dates_resume:latest" .
	docker build -f ./date_sorter/Dockerfile -t "date_sorter:latest" .
	docker build -f ./count_controller/Dockerfile -t "count_controller_worker:latest" .
	docker build -f ./count_summary_controller/Dockerfile -t "count_summary_controller:latest" .
	docker build -f ./processor/Dockerfile -t "processor:latest" .
	docker build -f ./places_manager/Dockerfile -t "places_manager:latest" .
	docker build -f ./coordinator_manager/Dockerfile -t "coordinator_manager:latest" .
.PHONY: docker-image

client-image:
	docker build -f ./reader/Dockerfile -t "reader:latest" .
.PHONY: client-image

stopper-image:
	docker build -f ./python_base_image/Dockerfile -t rabbitmq-python-base:0.0.1 .
	docker build -f ./stopper/Dockerfile -t "stopper:latest" .
.PHONY: stopper-image

docker-compose-up: docker-image
	COMPOSE_PARALLEL_LIMIT=20 \
	COMPOSE_PROJECT_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml up \
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


stopper-run: stopper-image
	COMPOSE_PROJECT_NAME=client \
	SERVER_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-stop.yaml up -d --build
.PHONY: stopper-run

stopper-stop:
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-stop.yaml stop -t 1
	COMPOSE_PROJECT_NAME=client \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-stop.yaml down
.PHONY: stopper-stop

stopper-logs:
	COMPOSE_PROJECT_NAME=client \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-stop.yaml logs -f
.PHONY: stopper-logs

docker-compose-down:
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml stop -t 1
	COMPOSE_PROJECT_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml down
.PHONY: docker-compose-down

docker-compose-logs:
	COMPOSE_PROJECT_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs

node-image:
	docker build -f ./node_watcher/Dockerfile -t "node_watcher:latest" .
.PHONY: node-image

node-run: node-image
	COMPOSE_PROJECT_NAME=node \
	SERVER_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-node.yaml up -d --build
.PHONY: node-run

node-stop:
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-node.yaml stop -t 1
	COMPOSE_PROJECT_NAME=node \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-node.yaml down
.PHONY: node-run

node-logs:
	COMPOSE_PROJECT_NAME=node \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-node.yaml logs -f
.PHONY: node-logs

data-node-image:
	docker build -f ./cluster_manager/Dockerfile -t "data_node:latest" .
.PHONY: data-node-image

data-node-run: data-node-image
	COMPOSE_PROJECT_NAME=data_node \
	SERVER_NAME=server \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-cluster.yaml up -d --build
.PHONY: data-node-run

data-node-stop:
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-cluster.yaml stop -t 1
	COMPOSE_PROJECT_NAME=data_node \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-cluster.yaml down
.PHONY: data-node-stop

data-node-logs:
	COMPOSE_PROJECT_NAME=data_node \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-cluster.yaml logs -f
.PHONY: data-node-logs

system-run: docker-compose-up node-run data-node-run

.PHONY: system-run

system-stop: node-stop data-node-stop docker-compose-down

.PHONY: system-stop