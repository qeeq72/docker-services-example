SHELL := /bin/bash

# 1. Сборка образа
build:
	@docker build -t dockerbasics_swarm_app:update .

rmi:
	@docker rmi dockerbasics_swarm_app:latest

# 2. Инициализация кластера
init:
	@docker swarm init
	@docker node update --label-add TAG=stage sirius-UbuntuPC

leave:
	@docker swarm leave --force

node-ls:
	@docker node ls

# 3. Запуск сервисов
deploy:
	@docker stack deploy -c ./docker-stack.yaml sirius-UbuntuPC --detach=false

destroy:
	@docker stack rm sirius-UbuntuPC

service-ls:
	@docker stack services sirius-UbuntuPC

# 4. Обновление сервисов
update:
	@docker service update --force --image dockerbasics_swarm_app:update sirius-UbuntuPC_app -d

rollback:
	@docker service update --rollback sirius-UbuntuPC_app -d
