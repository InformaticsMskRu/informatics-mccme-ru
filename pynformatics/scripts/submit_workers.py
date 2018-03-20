import click
from gevent import monkey
from gevent.pool import Group
from logging.config import fileConfig
from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config

from pynformatics.utils.redis import init_redis
from pynformatics.contest.ejudge.submit_queue.queue import SubmitQueue
from pynformatics.contest.ejudge.submit_queue.worker import SubmitWorker
from pynformatics.models import DBSession


monkey.patch_all()


@click.command()
@click.argument('ini', required=True)
@click.option('--workers', default=2)
def main(ini, workers):
    settings = get_appsettings(ini)
    fileConfig(settings['logging.config'], disable_existing_loggers=False)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    init_redis(settings)

    queue = SubmitQueue()
    worker_group = Group()
    for _ in range(workers):
        worker_group.start(SubmitWorker(queue))
    worker_group.join()
