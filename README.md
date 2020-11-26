# rest-app-api
cd rest-app-api

chmod +x entrypoint.sh

docker-compose up -d --build

docker-compose exec web python app/manage.py createsuperuser

