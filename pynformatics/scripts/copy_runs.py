import click
import datetime
import logging
import time
import transaction
from pyramid.paster import (
    get_appsettings,
    setup_logging
)
from sqlalchemy import (
    Column,
    and_,
    engine_from_config,
    or_,
)
from sqlalchemy.types import (
    DateTime,
    Integer,
    String,
)
from zope.sqlalchemy import mark_changed

from pynformatics.models import DBSession
from pynformatics.model.run import Run
from pynformatics.model.meta import Base
from pynformatics.utils.functions import attrs_to_dict


log = logging.getLogger(__name__)


class TempRun(Base):
    __table_args__ = {'schema': 'ejudge'}
    __tablename__ = 'runs_innodb_scr'

    run_id = Column(Integer, primary_key=True)
    contest_id = Column(Integer, primary_key=True)
    size = Column(Integer)
    create_time = Column(DateTime)
    create_nsec = Column(Integer)
    user_id = Column(Integer)
    prob_id = Column(Integer)  # TODO: rename to problem_id
    lang_id = Column(Integer)
    status = Column(Integer)
    ssl_flag = Column(Integer)
    ip_version = Column(Integer)
    ip = Column(String)
    hash = Column(String)
    run_uuid = Column(String)
    score = Column(Integer)
    test_num = Column(Integer)
    score_adj = Column(Integer)
    locale_id = Column(Integer)
    judge_id = Column(Integer)
    variant = Column(Integer)
    pages = Column(Integer)
    is_imported = Column(Integer)
    is_hidden = Column(Integer)
    is_readonly = Column(Integer)
    is_examinable = Column(Integer)
    mime_type = Column(String)
    examiners0 = Column(Integer)
    examiners1 = Column(Integer)
    examiners2 = Column(Integer)
    exam_score0 = Column(Integer)
    exam_score1 = Column(Integer)
    exam_score2 = Column(Integer)
    last_change_time = Column(DateTime)
    last_change_nsec = Column(Integer)
    is_marked = Column(Integer)
    is_saved = Column(Integer)
    saved_status = Column(Integer)
    saved_score = Column(Integer)
    saved_test = Column(Integer)
    passed_mode = Column(Integer)
    eoln_type = Column(Integer)
    store_flags = Column(Integer)
    token_flags = Column(Integer)
    token_count = Column(Integer)


ALL_COLUMNS = (
    'run_id',
    'contest_id',
    'size',
    'create_time',
    'create_nsec',
    'user_id',
    'prob_id',
    'lang_id',
    'status',
    'ssl_flag',
    'ip_version',
    'ip',
    'hash',
    'run_uuid',
    'score',
    'test_num',
    'score_adj',
    'locale_id',

    'judge_id',
    'variant',
    'pages',
    'is_imported',
    'is_hidden',
    'is_readonly',
    'is_examinable',
    'mime_type',
    'examiners0',
    'examiners1',
    'examiners2',
    'exam_score0',
    'exam_score1',
    'exam_score2',
    'last_change_time',
    'last_change_nsec',
    'is_marked',
    'is_saved',
    'saved_status',
    'saved_score',
    'saved_test',
    'passed_mode',
    'eoln_type',
    'store_flags',
    'token_flags',
    'token_count',
)



def get_last_copied(session):
    return session.query(TempRun).order_by(
        TempRun.create_time.desc()
    ).first()


def get_first_not_copied(session):
    temp_run = get_last_copied(session)
    run_query = session.query(Run)
    if temp_run:
        run_query = run_query.filter(Run.create_time > temp_run.create_time)
    run = run_query.order_by(Run.create_time).first()
    return run


def get_day_to_copy(session):
    run = get_first_not_copied(session)
    if not run:
        return None
    return run.create_time.date()


def copy_day(session, day):
    next_day = day + datetime.timedelta(days=1)
    start_of_day = f'{day} 00:00:00'
    end_of_day = f'{next_day} 00:00:00'

    result = session.execute(
        f'''
        INSERT INTO ejudge.runs_innodb_scr
        SELECT * FROM ejudge.runs
        WHERE create_time >= '{start_of_day}' AND create_time < '{end_of_day}'
        ORDER BY create_time;
        '''
    )
    return result.rowcount


@click.command()
@click.argument('ini', required=True)
def main(ini):
    """
    Copies runs from ejudge.runs to a new table
    """
    setup_logging(ini)
    settings = get_appsettings(ini)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    total = 0
    while True:
        session = DBSession()
        day = get_day_to_copy(session)
        if not day:
            log.info('Done')
            return
        log.info(f'Copying runs from {day}')
        runs_copied = copy_day(session, day)
        total += runs_copied
        log.info('Insert runs: %s. Total: %s.', runs_copied, total)

        mark_changed(session)
        transaction.commit()

        time.sleep(8)
