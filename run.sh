#!/bin/sh

#echo "Running!"

#docker run --name map_worker_1 \
#map_worker:latest
#-e PYTHONUNBUFFERED=1 \
#-e RECV_QUEUE=map_city \
#-e SEND_QUEUE=cities_resume \
#-e MASTER_SEND_QUEUE=master_map \
#-e STATUS_QUEUE=worker_status_queue \
#-e TOPIC_PLACES=places \
#-e WORKERS=2 \
#--network test-network \
#--entrypoint python3 /main.py \
#map_worker:latest
make docker-compose-up

COMPOSE_PROJECT_NAME=node \
SERVER_NAME=server \
docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-node.yaml up -d --build
