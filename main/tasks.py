import logging
from celery import chain
from main.utils.utils import update_movie_table, update_link_table,\
    update_rating_table, update_tag_table

from SmartMovie.celery import celery_app


# Get an instance of a logger
logger = logging.getLogger(__name__)


@celery_app.task(ignore_result=True)
def adding_task(x, y):
    return x + y


@celery_app.task(ignore_result=True)
def update_movie_table_task():
    update_movie_table()


@celery_app.task(ignore_result=True)
def update_link_table_task():
    update_link_table()


@celery_app.task(ignore_result=True)
def update_rating_table_task():
    update_rating_table()


@celery_app.task(ignore_result=True)
def update_tag_table_task():
    update_tag_table()


@celery_app.task(ignore_result=True)
def update_movie_tables_task():
    update_movie_table_task()
    chain(
        update_link_table_task(),
        update_rating_table_task(),
        update_tag_table_task()
    ).apply_async()
