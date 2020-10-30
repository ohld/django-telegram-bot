# django-telegram-bot
My sexy Django + python-telegram-bot + Celery + Redis + Postgres + Dokku + GitHub Actions template

## Local Testing

``` bash
python manage.py runserver
```

Probably you'll also need to run Celery workers & Redis. 

### .env

``` bash
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## Production 

All services that are going to be launched in production can be found in `Procfile` file. Dokku (open-source version of Heroku) uses `requirements.txt` to install everything and `Procfile` to run services afterwards. In `DOKKU_SCALE` you can find the number of processes to be launched (for load balancing).

**Postgres** and **Redis** are configured as Dokku plugins on a server. 

### Deploy on commit with Github Actions

Go to file .github/workflows/dokku.yml, enter your host name, deployed dokku app name and set SSH_PRIVATE_KEY secret variable via GitHub repo settings.