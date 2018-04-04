from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import (
    DateTime,
    Integer,
    String,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.meta import Base
from pynformatics.models import DBSession
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.notify import notify_user


EJUDGE_COLUMNS = [
    'run_id',
    'contest_id',
    'run_uuid',
    'score',
    'status',
    'lang_id',
    'test_num',
    'create_time',
    'last_change_time',
]


class Run(Base):
    __table_args__ = (
        ForeignKeyConstraint(
            ['ej_run_id', 'ej_contest_id'],
            ['ejudge.runs.run_id', 'ejudge.runs.contest_id'],
        ),
        {'schema': 'pynformatics'},
    )
    __tablename__ = 'runs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'))
    statement_id = Column(Integer, ForeignKey('moodle.mdl_statements.id'))
    score = Column(Integer)
    create_time = Column(DateTime)

    user = relationship('SimpleUser', backref='runs')
    problem = relationship('EjudgeProblem', backref='runs2')
    statement = relationship('Statement', backref='runs')

    # Поля скопированные из ejudge.runs
    ejudge_run_id = Column('ej_run_id', Integer)
    ejudge_contest_id = Column('ej_contest_id', Integer)
    ejudge_run_uuid = Column('ej_run_uuid', String)

    ejudge_score = Column('ej_score', Integer)
    ejudge_status = Column('ej_status', Integer)
    ejudge_language_id = Column('ej_lang_id', Integer)
    ejudge_test_num = Column('ej_test_num', Integer)

    ejudge_create_time = Column('ej_create_time', DateTime)
    ejudge_last_change_time = Column('ej_last_change_time', DateTime)

    ejudge_run = relationship('EjudgeRun', backref='run')

    @property
    def status(self):
        return self.ejudge_status
    
    @property
    def language_id(self):
        return self.ejudge_language_id

    @staticmethod
    def pick_ejudge_columns(ejudge_run):
        return {
            'ejudge_run_id': ejudge_run.run_id,
            'ejudge_contest_id': ejudge_run.contest_id,
            'ejudge_run_uuid': ejudge_run.run_uuid,
            'ejudge_score': ejudge_run.score,
            'ejudge_status': ejudge_run.status,
            'ejudge_language_id': ejudge_run.lang_id,
            'ejudge_test_num': ejudge_run.test_num,
            'ejudge_create_time': ejudge_run.create_time,
            'ejudge_last_change_time': ejudge_run.last_change_time,
        }

    @staticmethod
    def from_ejudge_run(ejudge_run):
        run = Run(
            user=ejudge_run.user,
            problem=ejudge_run.problem,
            score=ejudge_run.score,
            **Run.pick_ejudge_columns(ejudge_run),
        )
        return run

    @staticmethod
    def sync(ejudge_run_id, ejudge_contest_id):
        ejudge_run = DBSession.query(EjudgeRun).filter_by(
            run_id=ejudge_run_id, 
            contest_id=ejudge_contest_id
        ).first()
        if not ejudge_run:
            return
        
        run = DBSession.query(Run).filter_by(
            ejudge_run_id=ejudge_run_id, 
            ejudge_contest_id=ejudge_contest_id,
        ).first()
        if run:
            run.score = ejudge_run.score
            for key, value in Run.pick_ejudge_columns(ejudge_run).items():
                setattr(run, key, value)
        else:
            run = Run.from_ejudge_run(ejudge_run)
            DBSession.add(run)

        return run
    
    def serialize(self, context, attributes=None):
        if attributes is None:
            attributes = (
                'id',
                'problem_id',
                'statement_id',
                'score',
                'status',
                'language_id',
                'create_time',
            )
        serialized = attrs_to_dict(self, *attributes)
        if 'create_time' in attributes:
            serialized['create_time'] = str(self.create_time)
        
        return serialized
