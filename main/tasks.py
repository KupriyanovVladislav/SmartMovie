import logging
from celery import task
from .utils import update_movie_table


# Get an instance of a logger
logger = logging.getLogger(__name__)


@task(ignore_result=True)
def adding_task(x, y):
    return x + y


@task(ignore_result=True)
def update_movie_table_task():
    update_movie_table()


@task(ignore_result=True)
def update_link_table_task():
    pass


@task(ignore_result=True)
def update_rating_table_task():
    pass


@task(ignore_result=True)
def update_tag_table_task():
    pass


@task(ignore_result=True)
def update_movie_tables_task():
    pass
