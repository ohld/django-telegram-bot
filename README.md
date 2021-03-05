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

All services that are going to be launched in production can be found in `Procfile` file. Dokku (open-source version of Heroku which also uses `Buildpacks` technology) uses `requirements.txt` to install everything and `Procfile` to run services afterwards. In `DOKKU_SCALE` you can find the number of processes to be launched (for load balancing).

### Create Dokku app

``` bash
dokku apps:create dtb
```

You might need to added `.env` variables to app, e.g. Telegram token:

``` bash
dokku config:set dtb TELEGRAM_TOKEN=.....
```

Let's explicitly specify python buildpack to not mess with `Dockerfile` which is used mostly for local testing.

``` bash
dokku config:set dtb BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python.git#v191
```

**Postgres** and **Redis** are configured as Dokku plugins on a server. They will automatically add REDIS_URL & DATABASE_URL env vars to app. You might need to install these Dokku plugins before.

``` bash
dokku postgres:create dtb
dokku postgres:link dtb dtb

dokku redis:create dtb
dokku redis:link dtb dtb
```

### Deploy on commit with Github Actions

Go to file .github/workflows/dokku.yml, enter your host name, deployed dokku app name and set SSH_PRIVATE_KEY secret variable via GitHub repo settings. This will trigger Dokku's zero-downtime deployment.


### HTTPS & Telegram bot webhook

For Telegram bot API webhook usage you'll need a **https** which can be done using Letsencrypt dokku plugin. You will need to attach a domain to your Django app before and specify email (required by Letsencrypt). This will work only after a successfull deployment. 

``` bash
dokku domains:add dtb <YOURDOMAIN.COM>
dokku config:set --global DOKKU_LETSENCRYPT_EMAIL=<YOUR@EMAIL.COM>
dokku letsencrypt dtb
```


# Setup Telegram Bot API webhook

Just open in the browser:

```
https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://<YOURDOMAIN.COM>/super_secter_webhook/
```