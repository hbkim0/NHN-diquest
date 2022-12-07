DOCKER_COMPOSE_FILE=infra/docker-compose.yaml

all: infra

clean: infra-clean

infra:
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d
	@sleep 5
	@docker-compose -f ${DOCKER_COMPOSE_FILE} logs -t mongo-express

infra-clean:
	@docker-compose -f ${DOCKER_COMPOSE_FILE} down

.PHONY: clean infra infra-clean