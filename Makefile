DC = docker-compose
STORAGES_FILE = docker_compose/postgres.yaml
POSTGRES_BACKUP_FILE = docker_compose/backup.yaml
APP_FILE = docker_compose/app.yaml
EXEC = docker exec -it
LOGS = docker logs
ENV_FILE = --env-file .env
APP_CONTAINER = shop
DB_CONTAINER = ppostgres
INTO_BASH = /bin/bash
INTO_BASH_FOR_COMMANDS = /bin/bash -c
RUN_COLLECTSTATIC = python manage.py collectstatic --noinput
RUN_CREATESUPREUSER = python manage.py createsuperuser

.PHONY: storage
storage:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${POSTGRES_BACKUP_FILE} ${ENV_FILE} up -d

.PHONY: postgres_backup
postgres_backup:
	${DC} -f ${POSTGRES_BACKUP_FILE} ${ENV_FILE} up -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: appbash
appbash:
	${EXEC} ${APP_CONTAINER} ${INTO_BASH}

.PHONY: runtest
runtest:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} python manage.py migrate

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${INTO_BASH_FOR_COMMANDS} "${RUN_COLLECTSTATIC}"

.PHONY: createsuperuser
createsuperuser:
	${EXEC} ${APP_CONTAINER} ${INTO_BASH_FOR_COMMANDS} "${RUN_CREATESUPREUSER}"
