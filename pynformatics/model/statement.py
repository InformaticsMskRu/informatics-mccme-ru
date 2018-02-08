import time
from jsonschema import Draft4Validator

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Text, Float, Unicode
from sqlalchemy.orm import relationship, backref, relation

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from pynformatics.model.meta import Base
from pynformatics.model.participant import Participant
from pynformatics.models import DBSession
from pynformatics.utils.constants import LANG_NAME_BY_ID
from pynformatics.utils.exceptions import (
    StatementCanOnlyStartOnce,
    StatementFinished,
    StatementNothingToFinish,
    StatementNotOlympiad,
    StatementNotVirtual,
    StatementNotStarted,
    StatementOnlyOneOngoing,
    StatementPasswordIsWrong,
    StatementSettingsValidationError,
)
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.json_type import JsonType


class Statement(Base):
    __tablename__ = 'mdl_statements'
    __table_args__ = {'schema': 'moodle'}
    id = Column(Integer, primary_key=True)
    course_id = Column('course', Integer, ForeignKey('moodle.mdl_course.id'))
    name = Column(Unicode)
    summary = Column(Unicode)
    numbering = Column(Integer)
    disable_printing = Column('disableprinting', Integer)
    custom_titles = Column('customtitles', Integer)
    time_created = Column('timecreated', Integer)
    time_modified = Column('timemodified', Integer)
    contest_id = Column(Integer)
    time_start = Column('timestart', Integer)
    time_stop = Column('timestop', Integer)
    olympiad = Column(Integer)
    virtual_olympiad = Column(Integer)
    virtual_duration = Column(Integer)
    settings = Column(JsonType)

    course = relationship('Course', backref=backref('statements', lazy='dynamic'))

    course_module = relationship(
        'CourseModule',
        primaryjoin='and_(Statement.id==CourseModule.instance, CourseModule.module==19)',
        foreign_keys=[id],
    )

#    analysis = Column(Unicode)
#    pr_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_problem.id'))
#    ejudge_users = relation('EjudgeUser', backref="moodle.mdl_user", uselist=False)
#    ejudge_user = relation('EjudgeUser', backref = backref('moodle.mdl_user'), uselist=False, primaryjoin = "EjudgeUser.user_id == User.id")
    
    problems = association_proxy('StatementProblems', 'problem')
    user = association_proxy('StatementUsers1', 'user')

    SETTINGS_SCHEMA = {
        'type': 'object',
        'properties': {
            'allowed_languages': {
                'type': 'array',
                'uniqueItems': True,
                'items': {
                    'type': 'integer',
                    'enum': list(LANG_NAME_BY_ID.keys()),
                }
            },
            'type': {
                'oneOf': [
                    {
                        'type': 'null',
                    },
                    {
                        'type': 'string',
                        'enum': [
                            'olympiad',
                            'virtual',
                        ],
                    }
                ],
            },
            'group': {
                'type': 'integer',
            },
            'team': {
                'type': 'boolean',
            },
            'time_start': {
                'type': 'integer',
            },
            'time_stop': {
                'type': 'integer',
            },
            'freeze_time': {
                'type': 'integer',
            },
            'standings': {
                'type': 'boolean',
            },
            'test_only_samples': {
                'type': 'boolean',
            },
            'reset_submits_on_start': {
                'type': 'boolean',
            },
            'test_until_fail': {
                'type': 'boolean',
            },
            'start_from_scratch': {
                'type': 'boolean',
            },
            'restrict_view': {
                'type': 'boolean',
            }
        },
        'additionalProperties': False,
    }
    SETTINGS_SCHEMA_VALIDATOR = Draft4Validator(SETTINGS_SCHEMA)
    
    # def __init__(self, name, timelimit, memorylimit, content='', review='', description='', analysis=''):
    #     self.name = name
    #     self.content = content
    #     self.review = review
    #     self.description = description
    #     self.analysis = analysis
    #     self.hidden = 1
    #     self.timelimit = timelimit
    #     self.memorylimit = memorylimit

    def get_allowed_languages(self):
        if not (self.settings and 'allowed_languages' in self.settings):
            return None
        return self.settings['allowed_languages']

    def set_settings(self, settings):
        validation_error = next(self.SETTINGS_SCHEMA_VALIDATOR.iter_errors(settings), None)
        if validation_error:
            raise StatementSettingsValidationError(validation_error.message)
        self.settings = settings

        if settings.get('time_start'):
            self.time_start = settings['time_start']

        if settings.get('time_stop'):
            self.time_stop = settings['time_stop']

        if 'type' in settings:
            type_ = settings['type']
            if type_ == None:
                self.olympiad = False
                self.virtual_olympiad = False
            elif type_ == 'olympiad':
                self.olympiad = True
                self.virtual_olympiad = False
            else:
                self.olympiad = False
                self.virtual_olympiad = True

        self.time_modified = int(time.time())

    def start_participant(self,
                          user,
                          duration,
                          password=None,
                          ):
        if self.course \
                and self.course.require_password() \
                and password != self.course.password:
            raise StatementPasswordIsWrong

        if self.participants.filter(Participant.user_id == user.id).count():
            raise StatementCanOnlyStartOnce

        if user.get_active_participant():
            raise StatementOnlyOneOngoing

        new_participant = Participant(
            user_id=user.id,
            statement_id=self.id,
            start=int(time.time()),
            duration=duration,
        )
        DBSession.add(new_participant)

        return new_participant

    def finish_participant(self, user):
        active_participant = user.get_active_participant()
        if not active_participant or active_participant.statement_id != self.id:
            raise StatementNothingToFinish

        active_participant.duration = int(time.time() - active_participant.start)
        return active_participant

    def start(self,
              user,
              password=None,
              ):
        if not self.olympiad:
            raise StatementNotOlympiad

        now = time.time()
        if now < self.time_start:
            raise StatementNotStarted
        if now >= self.time_stop:
            raise StatementFinished

        return self.start_participant(
            user=user,
            duration=self.time_stop - int(time.time()),
            password=password,
        )

    def finish(self, user):
        if not self.olympiad:
            raise StatementNotOlympiad

        return self.finish_participant(user)

    def start_virtual(self, user, password=None):
        if not self.virtual_olympiad:
            raise StatementNotVirtual

        return self.start_participant(
            user=user,
            duration=self.virtual_duration,
            password=password,
        )

    def finish_virtual(self, user):
        if not self.virtual_olympiad:
            raise StatementNotVirtual

        return self.finish_participant(user)

    def serialize(self, context):
        serialized = attrs_to_dict(
            self,
            'id',
            'name',
            'olympiad',
            'settings',
            'time_start',
            'time_stop',
            'virtual_olympiad',
            'virtual_duration',
        )
        serialized['course_id'] = getattr(self.course, 'id', None)
        serialized['course_module_id'] = getattr(self.course_module, 'id', None)

        if self.course:
            serialized['require_password'] = self.course.require_password()
        else:
            serialized['require_password'] = False

        if self.olympiad or self.virtual_olympiad:
            if not context.user:
                return serialized

            try:
                participant = self.participants.filter(Participant.user_id==context.user_id).one()
            except NoResultFound:
                return serialized

            serialized['participant'] = participant.serialize(context)

        serialized['problems'] = {
            rank: {
                'id': statement_problem.problem.id,
                'name': statement_problem.problem.name,
            }
            for rank, statement_problem in self.StatementProblems.items()
            if statement_problem.problem and not statement_problem.hidden
        }
        return serialized


class StatementUser(Base):
    __tablename__ = 'mdl_olympiad'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)    
    statement_id = Column('contest_id', Integer, ForeignKey('moodle.mdl_statements.id'))
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))

#    statement = relationship("Statement", backref=backref("StatementUsers1", lazy="dynamic"), lazy="dynamic")
#    user = relationship("EjudgeUser", backref=backref("StatementUsers2", lazy="dynamic"), lazy="dynamic")             
        
class StatementProblem(Base):
    __tablename__ = 'mdl_statements_problems_correlation'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)    
    statement_id = Column(Integer, ForeignKey('moodle.mdl_statements.id'))
    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'))
    rank = Column('rank', Integer)
    hidden = Column('hidden', Integer)

    statement = relationship('Statement', backref=backref('StatementProblems', collection_class=attribute_mapped_collection("rank")))

    # reference to the "Keyword" object
    problem = relationship('Problem', backref=backref('StatementProblems'))
    
    def __init__(self, statement_id, problem_id, rank):
        self.statement_id = statement_id
        self.problem_id = problem_id
        self.rank = rank
        self.hidden = 0
