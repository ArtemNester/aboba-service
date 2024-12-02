run-staging:
	docker-compose -f docker-compose-staging.yml --env-file .env.staging up -d --build --force-recreate
	docker-compose -f docker-compose-staging.yml exec api python manage.py makemigrations accounts
	docker-compose -f docker-compose-staging.yml exec api python manage.py migrate
	docker-compose -f docker-compose-staging.yml exec api python manage.py collectstatic --noinput

stop-staging:
	docker-compose -f docker-compose-staging.yml down -v --remove-orphans
