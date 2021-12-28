include .env
export

up:
	docker-compose up -d --build
down:
	docker-compose down

migrate:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

create-admin:
	docker-compose exec web python manage.py createsuperuser

logs-web:
	docker logs --tail 50 --follow --timestamps ${APP_NAME}
logs-db:
	docker logs --tail 50 --follow --timestamps ${APP_NAME}_db

db-console:
	docker-compose exec db psql --username=${POSTGRES_USER} --dbname=${POSTGRES_DB}

seed-db:
	docker-compose exec web python manage.py runscript seed_db
clear-db:
	docker-compose exec web python manage.py flush

test:
	docker-compose exec web python manage.py test
coverage:
	docker-compose exec web coverage report
coverage-erase:
	docker-compose exec web coverage erase
