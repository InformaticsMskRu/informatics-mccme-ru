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
from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.meta import Base
from pynformatics.model.run import (
    EJUDGE_COLUMNS,
    Run,
)
from pynformatics.utils.functions import attrs_to_dict


log = logging.getLogger(__name__)


def get_last_copied(session, run_model, create_time='create_time'):
    return session.query(run_model).order_by(
        getattr(run_model, create_time).desc()
    ).first()


def get_first_not_copied(session, run_model, create_time='create_time'):
    temp_run = get_last_copied(session, run_model, create_time)
    run_query = session.query(EjudgeRun)
    if temp_run:
        run_query = run_query.filter(
            EjudgeRun.create_time > getattr(temp_run, create_time)
        )
    run = run_query.order_by(EjudgeRun.create_time).first()
    return run


def get_day_to_copy(session, run_model, create_time='create_time'):
    run = get_first_not_copied(session, run_model, create_time)
    if not run:
        return None
    return run.create_time.date()


def copy_day(destination, session, day, run_model, create_time='create_time'):
    next_day = day + datetime.timedelta(days=1)
    start_of_day = f'{day} 00:00:00'
    end_of_day = f'{next_day} 00:00:00'

    result = session.execute(
        f'''
        INSERT INTO {destination}
        SELECT * FROM ejudge.runs
        WHERE create_time >= '{start_of_day}' AND create_time < '{end_of_day}'
        ORDER BY create_time;
        '''
    )
    return result.rowcount 


def copy_day2(destination, session, day, run_model):
    next_day = day + datetime.timedelta(days=1)
    start_of_day = f'{day} 00:00:00'
    end_of_day = f'{next_day} 00:00:00'

    columns = ',\n'.join(EJUDGE_COLUMNS)
    ej_columns = ',\n'.join(['ej_' + column for column in EJUDGE_COLUMNS])

    result = session.execute(
        f'''
        INSERT INTO {destination} (
            {ej_columns}
        )
        SELECT
            {columns}
        FROM ejudge.runs
        WHERE create_time >= '{start_of_day}' AND create_time < '{end_of_day}'
        ORDER BY create_time;
        '''
    )
    return result.rowcount 

def copy_day3(destination, session, day, run_model):
    next_day = day + datetime.timedelta(days=1)
    start_of_day = f'{day} 00:00:00'
    end_of_day = f'{next_day} 00:00:00'

    columns = ',\n'.join(EJUDGE_COLUMNS)
    ej_columns = ',\n'.join(['ej_' + column for column in EJUDGE_COLUMNS])
    runs_columns = ',\n'.join(['runs.' + column for column in EJUDGE_COLUMNS])
    
    result = session.execute(
        f'''
        INSERT INTO {destination} (
            user_id,
            problem_id,
            {ej_columns}
        )
        SELECT
            users.id,
            problems.id,
            {runs_columns}
        FROM
        (
            SELECT 
                user_id, 
                prob_id,
                {columns} 
            FROM ejudge.runs
            WHERE create_time >= '{start_of_day}' AND create_time < '{end_of_day}'
        ) runs
        LEFT JOIN moodle.mdl_user users 
            ON runs.user_id = users.ej_id
        LEFT JOIN moodle.mdl_ejudge_problem ej_problems
            ON runs.contest_id = ej_problems.ejudge_contest_id AND runs.prob_id = ej_problems.problem_id
        LEFT JOIN moodle.mdl_problems problems
            ON problems.pr_id = ej_problems.id
        ;
        '''
    )
    return result.rowcount 


@click.command()
@click.argument('ini', required=True)
def main(ini):
    """
    Copies runs from ejudge.runs to a new table
    """
    return
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


@click.command()
@click.argument('ini', required=True)
def duplicate(ini):
    setup_logging(ini)
    settings = get_appsettings(ini)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    total = 0
    while True:
        session = DBSession()
        day = get_day_to_copy(session, Run, create_time='ejudge_create_time')
        if not day:
            log.info('Done')
            return
        log.info(f'Copying runs from {day}')
        runs_copied = copy_day3(
            destination='pynformatics.runs',
            session=session,
            day=day,
            run_model=Run
        )
        mark_changed(session)
        transaction.commit()

@click.command()
@click.argument('ini', required=True)
def duplicate2(ini):
    setup_logging(ini)
    settings = get_appsettings(ini)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    total = 0
    while True:
        session = DBSession()
        day = get_day_to_copy(session, Run, create_time='ejudge_create_time')
        if not day:
            log.info('Done')
            return
        log.info(f'Copying runs from {day}')
        runs_copied = copy_day2(
            destination='pynformatics.runs',
            session=session,
            day=day,
            run_model=Run
        )
        mark_changed(session)
        transaction.commit()
