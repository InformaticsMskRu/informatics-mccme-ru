import logging
from sqlalchemy import (
    Column,
    ForeignKey,
    and_,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    backref,
    reconstructor,
    relationship,
)
from sqlalchemy.types import Integer

from pynformatics.model.meta import Base
from pynformatics.model.problem import EjudgeProblem
from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.model.run import Run
from pynformatics.model.user import SimpleUser
from pynformatics.models import DBSession
from pynformatics.utils.exceptions import RunNotFound
from pynformatics.utils.functions import (
    attrs_to_dict,
    index_of,
)
from pynformatics.utils.json_type import JsonType


log = logging.getLogger(__name__)


class StandingsMixin:
    __table_args__ = {'schema': 'pynformatics'}

    @declared_attr
    def json(cls):
        return Column('json', JsonType)

    def update(self, user):
        if not self.json:
            self.json = {}

        if user.id not in self.json:
            self.json[user.id] = {
                **attrs_to_dict(user, 'firstname', 'lastname'),
            }


class ProblemStandings(StandingsMixin, Base):
    __tablename__ = 'problem_standings'
    __table_args__ = {'schema': 'pynformatics'}


    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'), primary_key=True)
    problem = relationship('EjudgeProblem', backref=backref('standings', uselist=False, lazy='joined'))

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        DBSession.add(instance)

        # Flush, чтобы получить из базы problem
        DBSession.flush([instance])

        # Expire, чтобы у задачи стал доступен standings
        DBSession.expire(instance.problem)

        log.info('ProblemStandings(problem_id=%s) Created. Starting updates' % instance.problem_id)

        users = DBSession.query(SimpleUser).join(Run).filter(
            and_(
                Run.contest_id == instance.problem.ejudge_contest_id,
                Run.prob_id == instance.problem.problem_id
            )
        ).distinct().all()

        for user in users:
            instance.update(user)

        log.info('ProblemStandings(problem_id=%s) Updates finished.' % instance.problem_id)

        return instance

    def update(self, user):
        super(ProblemStandings, self).update(user)

        user_runs = self.problem.runs.filter_by(
            user_id=user.ejudge_id
        ).order_by(Run.create_time).all()

        processed = {
            'attempts': 0,
            'score': 0,
            'status': None,
        }
        for run in user_runs:
            processed['attempts'] += 1
            if run.score > processed['score']:
                processed['score'] = run.score
                processed['status'] = run.status

            if run.score == 100:
                break

        self.json[user.id].update(processed)

    def serialize(self, context):
        return self.json


class StatementStandings(StandingsMixin, Base):
    __tablename__ = 'statement_standings'

    statement_id = Column(Integer, ForeignKey('moodle.mdl_statements.id'), primary_key=True)
    statement = relationship('Statement', backref=backref('standings', uselist=False, lazy='joined'))

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        DBSession.add(instance)

        # Flush, чтобы получить из базы statement
        DBSession.flush([instance])

        # Expire, чтобы у statement стал доступен standings
        DBSession.expire(instance.statement)

        log.info('StatementStandings(statement_id=%s) Created. Starting updates' % instance.statement_id)

        pynformatics_runs = DBSession.query(PynformaticsRun).filter_by(
            statement_id=instance.statement_id
        ).all()

        for pynformatics_run in pynformatics_runs:
            instance.update(pynformatics_run.run)

        log.info('StatementStandings(statement_id=%s) Updates finished.' % instance.statement_id)

        return instance

    @staticmethod
    def serialize_run(run):
        serialized = attrs_to_dict(
            run,
            'run_id',
            'contest_id',
            'create_time',
            'score',
            'status'
        )
        serialized['create_time'] = serialized['create_time'].isoformat()
        serialized['problem_id'] = run.problem.id
        return serialized

    def update(self, run):
        user = run.user
        super(StatementStandings, self).update(user)

        user_data = self.json[user.id]
        if 'runs' not in user_data:
            user_data['runs'] = []

        replace_index = index_of(
            user_data['runs'],
            lambda run_json: run_json['run_id'] == run.run_id and run_json['contest_id'] == run.contest_id
        )
        if replace_index is not None:
            user_data['runs'][replace_index] = StatementStandings.serialize_run(run)
        else:
            insert_index = index_of(
                user_data['runs'],
                lambda run_json: run_json['create_time'] > run.create_time.isoformat(),
                len(user_data['runs'])
            )
            user_data['runs'].insert(insert_index, StatementStandings.serialize_run(run))

    # TODO: добавить обработку настроек контеста
    def serialize(self, context):
        return self.json
