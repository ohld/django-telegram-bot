from celery.decorators import task
from celery.utils.log import get_task_logger

from redtube.models import Pornstar

@task
def sync_redtube_data():
    Pornstar.sync_all_pornstars()
    Pornstar.sync_all_unknown_pornstars()