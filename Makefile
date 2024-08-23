SHELL := /bin/bash


NETWORK_NAME := dockerbasics_compose_net


APP_IMAGE_NAME := dockerbasics_compose_app
APP_IMAGE_TAG := latest
APP_CONTAINER_NAME := app
APP_CONTAINER_PORT := 11111


DB_VOLUME_NAME := dockerbasics_compose_db_volume
DB_CONTAINER_NAME := db
DB_USER := user
DB_PASSWORD := password
DB_NAME := db


S3_VOLUME_NAME := dockerbasics_compose_s3_volume
S3_CONTAINER_NAME := s3
S3_ACCESS_KEY := user
S3_SECRET_KEY := password
S3_UI_PORT := 11112


# общее
rmi:
	@docker rmi $(APP_IMAGE_NAME):$(APP_IMAGE_TAG)

build:
	@docker build -t $(APP_IMAGE_NAME):$(APP_IMAGE_TAG) .

clear-unused-cache:
	@docker builder prune -f

create-net:
	@docker network create $(NETWORK_NAME)

# БД
run-db:
	@docker volume create $(DB_VOLUME_NAME)
	@docker run \
	--name $(DB_CONTAINER_NAME) \
	-d \
	--net=$(NETWORK_NAME) \
	-e POSTGRES_USER=user \
	-e POSTGRES_PASSWORD=password \
	-e POSTGRES_DB=db \
	-v $(DB_VOLUME_NAME):/var/lib/postgresql/data \
	postgres:16.4-alpine

stop-db:
	@docker stop $(DB_CONTAINER_NAME)

# Объектное хранилище
run-s3:
	@docker volume create $(S3_VOLUME_NAME)
	@docker run \
	--name $(S3_CONTAINER_NAME) \
	-d \
	-p $(S3_UI_PORT):9001 \
	--net=$(NETWORK_NAME) \
	-e MINIO_ACCESS_KEY=$(S3_ACCESS_KEY) \
	-e MINIO_SECRET_KEY=$(S3_SECRET_KEY) \
	-v $(S3_VOLUME_NAME):/data \
	minio/minio:RELEASE.2024-08-17T01-24-54Z \
	server /data --console-address ":9001"

stop-s3:
	@docker stop $(S3_CONTAINER_NAME)

# Приложение
run-app:
	@docker run --rm \
	--name $(APP_CONTAINER_NAME) \
	-p $(APP_CONTAINER_PORT):80 \
	--net=$(NETWORK_NAME) \
	-e DB_HOST=$(DB_CONTAINER_NAME) \
	-e DB_PORT=5432 \
	-e DB_USER=$(DB_USER) \
	-e DB_PASSWORD=$(DB_PASSWORD) \
	-e DB_NAME=$(DB_NAME) \
	-e S3_HOST=$(S3_CONTAINER_NAME) \
	-e S3_PORT=9000 \
	-e S3_ACCESS_KEY=$(S3_ACCESS_KEY) \
	-e S3_SECRET_KEY=$(S3_SECRET_KEY) \
	$(APP_IMAGE_NAME):$(APP_IMAGE_TAG)

stop-app:
	@docker stop $(APP_CONTAINER_NAME)
