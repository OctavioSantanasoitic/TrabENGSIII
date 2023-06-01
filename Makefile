PROJECT_NAME=eng

install:
	python3 -m pip install -r requirments.txt

infra-up:
	docker-compose -p ${PROJECT_NAME} up -d

infra-down:
	docker-compose -p ${PROJECT_NAME} down
