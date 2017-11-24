import datetime
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
from pynformatics.model.virtual_participant import VirtualParticipant
from pynformatics.models import DBSession
from pynformatics.utils.constants import LANG_NAME_BY_ID
from pynformatics.utils.exceptions import (
    BadRequest,
    StatementNothingToFinish,
    StatementNotVirtual,
    StatementOnlyOneOngoingVirtual,
    StatementVirtualCanOnlyStartOnce,
)
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.json_type import JsonType


class Statement(Base):
    __tablename__ = 'mdl_statements'
    __table_args__ = {'schema': 'moodle'}
    id = Column(Integer, primary_key=True)
    course = Column(Integer)
    name = Column(Unicode)
    summary = Column(Unicode)
    numbering = Column(Integer)
    disableprinting = Column(Integer)
    customtitles = Column(Integer)
    timecreated = Column(Integer)
    timemodified = Column(Integer)
    contest_id = Column(Integer)
    timestart = Column(Integer)
    timestop = Column(Integer)
    olympiad = Column(Integer)
    virtual_olympiad = Column(Integer)
    virtual_duration = Column(Integer)
    settings = Column(JsonType)

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
                    'type': 'string',
                    'enum': LANG_NAME_BY_ID.keys(),
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
        if not self.SETTINGS_SCHEMA_VALIDATOR.is_valid(settings):
            raise BadRequest('Bad settings format')
        if self.id == 11928:
            self.settings = settings
        return {}

    def start_virtual(self, user):
        if not self.virtual_olympiad:
            raise StatementNotVirtual

        if self.virtual_participants.filter(VirtualParticipant.user_id==user.id).count():
            raise StatementVirtualCanOnlyStartOnce

        if user.get_active_virtual_participant():
            raise StatementOnlyOneOngoingVirtual

        new_virtual_participant = VirtualParticipant(
            user_id=user.id,
            statement_id=self.id,
            start=int(time.time()),
            duration=self.virtual_duration,
        )
        DBSession.add(new_virtual_participant)

        return new_virtual_participant

    def finish_virtual(self, user):
        current_virtual = user.get_active_virtual_participant()
        if not current_virtual:
            raise StatementNothingToFinish

        actual_duration = datetime.datetime.now() - datetime.datetime.fromtimestamp(current_virtual.start)
        current_virtual.duration = int(actual_duration.total_seconds() // 60)
        return current_virtual

    def serialize(self, context):
        serialized = attrs_to_dict(
            self,
            'course',
            'name',
            'settings',
            'virtual_olympiad',
            'virtual_duration',
        )
        serialized['course_module_id'] = self.course_module.id

        if self.virtual_olympiad:
            if not context.user:
                return serialized

            try:
                virtual_participant = self.virtual_participants.filter(VirtualParticipant.user_id==context.user_id).one()
            except NoResultFound:
                return serialized

            serialized['virtual_participant'] = virtual_participant.serialize(context)

        serialized['problems'] = {
            rank: statement_problem.problem.id
            for rank, statement_problem in context.statement.StatementProblems.items()
            if not statement_problem.hidden
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
