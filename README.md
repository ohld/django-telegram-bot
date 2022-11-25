# django-telegram-bot

<p align="center">
    <img src="https://user-images.githubusercontent.com/50623190/201977740-68ef4044-9cfa-45da-8897-2a90ecfa33ae.png" align="center" height="350px" weight="350px">
</p>

Sexy Django + python-telegram-bot + Celery + Redis + Postgres + Dokku + GitHub Actions template. Production-ready Telegram bot with database, admin panel and a bunch of useful built-in methods.


⭐ graph: 
[![Sparkline](https://stars.medv.io/ohld/django-telegram-bot.svg)](https://stars.medv.io/ohld/django-telegram-bot)


### Check the example bot that uses the code from Main branch: [t.me/djangotelegrambot](https://t.me/djangotelegrambot)

## Features

* Database: Postgres, Sqlite3, MySQL - you decide!
* Admin panel (thanks to [Django](https://docs.djangoproject.com/en/3.1/intro/tutorial01/))
* Background jobs using [Celery](https://docs.celeryproject.org/en/stable/)
* [Production-ready](https://github.com/ohld/django-telegram-bot/wiki/Production-Deployment-using-Dokku) deployment using [Dokku](https://dokku.com)
* Telegram API usage in polling or [webhook mode](https://core.telegram.org/bots/api#setwebhook)
* Export all users in `.csv`
* Native telegram [commands in menu](https://github.com/ohld/django-telegram-bot/blob/main/.github/imgs/bot_commands_example.jpg)
  * In order to edit or delete these commands you'll need to use `set_my_commands` bot's method just like in [tgbot.dispatcher.setup_my_commands](https://github.com/ohld/django-telegram-bot/blob/main/tgbot/dispatcher.py#L150-L156)

Built-in Telegram bot methods:
* `/broadcast` — send message to all users (admin command)
* `/export_users` — bot sends you info about your users in .csv file (admin command)
* `/stats` — show basic bot stats 
* `/ask_for_location` — log user location when received and reverse geocode it to get country, city, etc.


## Content

* [How to run locally](https://github.com/ohld/django-telegram-bot/edit/main/README.md#how-to-run)
   * [Quickstart with polling and SQLite](https://github.com/ohld/django-telegram-bot/edit/main/README.md#quickstart-polling--sqlite)
   * [Using docker-compose](https://github.com/ohld/django-telegram-bot/edit/main/README.md#run-locally-using-docker-compose)
* [Deploy to production](https://github.com/ohld/django-telegram-bot/edit/main/README.md#deploy-to-production)
   * [Using dokku](https://github.com/ohld/django-telegram-bot/edit/main/README.md#deploy-using-dokku-step-by-step)
   * [Telegram webhook](https://github.com/ohld/django-telegram-bot/edit/main/README.md#https--telegram-bot-webhook)


# How to run

## Quickstart: Polling & SQLite

The fastest way to run the bot is to run it in polling mode using SQLite database without all Celery workers for background jobs. This should be enough for quickstart:

``` bash
git clone https://github.com/ohld/django-telegram-bot
cd django-telegram-bot
```

Create virtual environment (optional)
``` bash
python3 -m venv dtb_venv
source dtb_venv/bin/activate
```

Install all requirements:
```
pip install -r requirements.txt
```

Create `.env` file in root directory and copy-paste this:
``` bash 
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
TELEGRAM_TOKEN=<ENTER YOUR TELEGRAM TOKEN HERE>
```

Run migrations to setup SQLite database:
``` bash
python manage.py migrate
```

Create superuser to get access to admin panel:
``` bash
python manage.py createsuperuser
```

Run bot in polling mode:
``` bash
python run_polling.py 
```

If you want to open Django admin panel which will be located on http://localhost:8000/tgadmin/:
``` bash
python manage.py runserver
```

## Run locally using docker-compose
If you want just to run all the things locally, you can use Docker-compose which will start all containers for you.

### Create .env file. 
You can switch to PostgreSQL just by uncommenting it's `DATABASE_URL` and commenting SQLite variable.
```bash
cp .env_example .env
```


### Docker-compose

To run all services (Django, Postgres, Redis, Celery) at once:
``` bash
docker-compose up -d --build
```

Check status of the containers.
``` bash
docker ps -a
```
It should look similar to this:
<p align="left">
    <img src="https://github.com/ohld/django-telegram-bot/raw/main/.github/imgs/containers_status.png">
</p>

Try visit <a href="http://0.0.0.0:8000/tgadmin">Django-admin panel</a>.

### Enter django shell:

``` bash
docker exec -it dtb_django bash
```

### Create superuser for Django admin panel

``` bash
python manage.py createsuperuser
```

### To see logs of the container:

``` bash
docker logs -f dtb_django
```


# Deploy to Production 

Production stack will include these technologies:

1) Postgres as main database for Django
2) Celery + Redis + easy scalable workers 
3) Dokku as PaaS (will build app from sources and deploy it with zero downtime)

All app's services that are going to be launched in production can be found in `Procfile` file. It includes Django webserver (Telegram event processing + admin panel) and Celery workers (background and periodic jobs).

## What is Dokku and how it works

[Dokku](https://dokku.com/) is an open-source version of Heroku. 

I really like Heroku deployment approach: 
1) you push commit to Main branch of your Repo
2) in couple minutes your new app is running
3) if something breaks during deployment - old app will not be shut down

You can achieve the same approach with Dokku + Github Actions (just to trigger deployment).

Dokku uses [buildpacks](https://buildpacks.io/) technology to create a Docker image from the code. No Dockerfile needed. Speaking about Python, it requires `requirements.txt`, `Procfile` files to run the things up. Also files `DOKKU_SCALE` and `runtime.txt` are useful to tweak configs to make the deployed app even better. E.g. in `DOKKU_SCALE` you can specify how many app instances should be run behind built-in load balancer.

One disadvantage of Dokku that you should be warned about is that it can work with one server only. You can't just scale your app up to 2 machines using only small config change. You still can use several servers by providing correct .env URLs to deployed apps (e.g. DATABASE_URL) but it will require more time to setup.

## Deploy using Dokku: step-by-step

I assume that you already have [Dokku installed](https://dokku.com/docs/getting-started/installation/) on your server. Let's also assume that the address of your server is *<YOURDOMAIN.COM>* (you will need a domain to setup HTTPs for Telegram webhook support). I'd recommend to have at least [2GB RAM and 2 CPU cores](https://m.do.co/c/260555f64021).

### Create Dokku app

``` bash
dokku apps:create dtb
```

You might need to added `.env` variables to app, e.g. to specify Telegram token:

``` bash
dokku config:set dtb TELEGRAM_TOKEN=.....
```

Let's explicitly specify python buildpack to not mess with `Dockerfile` which is used mostly for local testing right now.

``` bash
dokku config:set dtb BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python.git#v191
```

**Postgres** and **Redis** are configured as Dokku plugins on a server. They will automatically add REDIS_URL & DATABASE_URL .env vars to the app after being linked. You might need to install these Dokku plugins before. [Install Postgres](https://github.com/dokku/dokku-postgres), [install Redis](https://github.com/dokku/dokku-redis).

``` bash
dokku postgres:create dtb
dokku postgres:link dtb dtb

dokku redis:create dtb
dokku redis:link dtb dtb
```

### Deploy on commit with Github Actions

Go to file [.github/workflows/dokku.yml](https://github.com/ohld/django-telegram-bot/blob/main/.github/workflows/dokku.yml):

1. Enter your host name (address of your server), 
2. Deployed dokku app name (in our case this is `dtb`),
3. Set `SSH_PRIVATE_KEY` secret variable via GitHub repo settings. This private key should have the **root ssh access** to your server.

This will trigger Dokku's zero-downtime deployment. You would probably need to fork this repo to change file. 

After that you should see a green arrow ✅ at Github Actions tab that would mean your app is deployed successfully. If you see a red cross ❌ you can find the deployed logs in Github Actions tab and find out what went wrong.

## HTTPS & Telegram bot webhook

### Why you need to setup webhook

Basic polling approach is really handy and can speed up development of Telegram bots. But it doesn't scale. Better approach is to allow Telegram servers push events (webhook messages) to your server when something happens with your Telegram bot. You can use built-in Dokku load-balancer to parallel event processing.

### HTTPS using Letsencrypt plugin

For Telegram bot API webhook usage you'll need a **https** which can be setup using [Letsencrypt Dokku plugin](https://github.com/dokku/dokku-letsencrypt). You will need to attach a domain to your Django app before and specify a email (required by Letsencrypt) - you will receive notifications when certificates would become old. Make sure you achieved a successful deployment first (your app runs at <YOURDOMAIN.COM>, check in browser).

``` bash
dokku domains:add dtb <YOURDOMAIN.COM>
dokku config:set --global DOKKU_LETSENCRYPT_EMAIL=<YOUR@EMAIL.COM>
dokku letsencrypt:enable dtb
```

### Setup Telegram Bot API webhook URL

You need to tell Telegram servers where to send events of your Telegram bot. Just open in the browser:

```
https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://<YOURDOMAIN.COM>/super_secter_webhook/
```


### After deployment

You can be sure that your app is deployed successfully if you see a green arrow at the latest workflow at Github Actions tab.

You would need to create a superuser to access an admin panel at https://<YOURDOMAIN.COM>/tgadmin. This can be done using a standard way using django shell:


### Open shell in deployed app 
``` shell
dokku enter dtb web 
```

### Create Django super user
Being inside a container:
``` bash
python manage.py createsuperuser
```

After that you can open admin panel of your deployed app which is located at https://<YOURDOMAIN.COM>/tgadmin.

### Read app logs

``` bash
dokku logs dtb -t
```


----
