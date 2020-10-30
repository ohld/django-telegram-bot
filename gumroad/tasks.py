from celery.decorators import task
from celery.utils.log import get_task_logger

from gumroad.models import Sale, Product, Subscriber


@task(ignore_result=True)  # periodical task
def sync_data_with_gumroad():
    """ Syncs / pulls data from Gumroad """
    Product.update()
    Sale.update()
    Subscriber.update()