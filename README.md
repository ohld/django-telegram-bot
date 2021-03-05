# django-telegram-bot
My sexy Django + python-telegram-bot + Celery + Redis + Postgres + Dokku + GitHub Actions template

## Local Testing
### Create .env file

``` bash
#Telegram
TELEGRAM_TOKEN=bot_token

#DB
DB_USER=postgres
DB_USER_PASSWORD=postgres
DB_NAME=postgres
DATABASE_URL=postgres://${DB_USER}:${DB_USER_PASSWORD}@db:${DB_CONTAINER_PORT}/${DB_NAME}
```

### docker-compose

To run all services (django, postgres, redis, celery) at once:
``` bash
docker-compose up -d --build
```

Check status of the containers.
``` bash
docker ps -a
```
It should look similar to this:
<p align="left">
    <img src="./.github/imgs/containers_status.png">
</p>

Try visit <a href="http://0.0.0.0:8000/tgadmin">django-admin panel</a>

### Enter django shell if you are using docker

``` bash
docker exec -it django bash
```

### Create superuser

``` bash
python manage.py createsuperuser
```

## Production 

All services that are going to be launched in production can be found in `Procfile` file. Dokku (open-source version of Heroku) uses `requirements.txt` to install everything and `Procfile` to run services afterwards. In `DOKKU_SCALE` you can find the number of processes to be launched (for load balancing).

**Postgres** and **Redis** are configured as Dokku plugins on a server. 

### Deploy on commit with Github Actions

Go to file .github/workflows/dokku.yml, enter your host name, deployed dokku app name and set SSH_PRIVATE_KEY secret variable via GitHub repo settings.
