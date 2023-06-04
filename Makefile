PROJECT_NAME=eng
SERVICE_NAME=eng_project_service
TEST_CONTAINER_NAME=${SERVICE_NAME}_test
COVERAGE_FILE=coverage.xml

.PHONY: build
build:
	@docker-compose build --pull ${BUILD_ARGS}

.PHONY: infra-up
infra-up:
	docker-compose -f docker-compose.infra.yml -p ${PROJECT_NAME} up -d

.PHONY: infra-down
infra-down:
	docker-compose -f docker-compose.infra.yml -p ${PROJECT_NAME} down

.PHONY: test
test:
	@-docker rm -f ${TEST_CONTAINER_NAME} || true >/dev/null
	@docker-compose -p ${SERVICE_NAME} run -e MONGO_DATABASE_NAME=test --name ${TEST_CONTAINER_NAME} ${SERVICE_NAME} python -m pytest --cov --cov-report xml --cov-report html ${args}
	@-docker cp ${TEST_CONTAINER_NAME}:/app/${COVERAGE_FILE} ./${COVERAGE_FILE}
	@-docker rm -f ${TEST_CONTAINER_NAME} >/dev/null
