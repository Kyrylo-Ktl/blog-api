include .env
export

up:
	docker-compose -f docker/docker-compose.yml up -d --build
down:
	docker-compose -f docker/docker-compose.yml down

migrate:
	docker-compose -f docker/docker-compose.yml exec web python manage.py makemigrations
	docker-compose -f docker/docker-compose.yml exec web python manage.py migrate

create-admin:
	docker-compose exec web python manage.py createsuperuser

logs-web:
	docker logs --tail 50 --follow --timestamps ${APP_NAME}
logs-db:
	docker logs --tail 50 --follow --timestamps ${APP_NAME}_db

db-console:
	docker-compose -f docker/docker-compose.yml exec db psql --username=${SQL_USER} --dbname=${SQL_DATABASE}

seed-db:
	docker-compose -f docker/docker-compose.yml exec web python manage.py runscript seed_db
clear-db:
	docker-compose -f docker/docker-compose.yml exec web python manage.py flush

test:
	docker-compose -f docker/docker-compose.yml exec web python manage.py test
coverage:
	docker-compose -f docker/docker-compose.yml exec web coverage report
coverage-erase:
	docker-compose -f docker/docker-compose.yml exec web coverage erase
