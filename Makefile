PROJECT_NAME=eng

install:
	python3 -m pip install -r requirments.txt

.PHONY: infra-up
infra-up:
	docker-compose -f docker-compose.infra.yml -p ${PROJECT_NAME} up -d

.PHONY: infra-down
infra-down:
	docker-compose -f docker-compose.infra.yml -p ${PROJECT_NAME} down
