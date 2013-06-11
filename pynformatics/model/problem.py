"""Problem model"""
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Text, Float, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, relation
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
import os

from pynformatics.model.meta import Base

class Problem(Base):
    __tablename__ = "mdl_problems"
    __table_args__ = {'schema':'moodle'}
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    content = Column(Unicode)
    review = Column(Unicode)
    hidden = Column(Integer)
    timelimit = Column(Float)
    memorylimit = Column(Integer)
    description = Column(Unicode)
    analysis = Column(Unicode)
    sample_tests = Column(Unicode)
    sample_tests_html = Column(Unicode)
    show_limits = Column(Boolean)
    output_only = Column(Boolean)
    pr_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_problem.id'))
#    ejudge_users = relation('EjudgeUser', backref="moodle.mdl_user", uselist=False)
#    ejudge_user = relation('EjudgeUser', backref = backref('moodle.mdl_user'), uselist=False, primaryjoin = "EjudgeUser.user_id == User.id")
    def __init__(self, name, timelimit, memorylimit, output_only, content='', review='', description='', analysis='', sample_tests='', sample_tests_html = ''):
        self.name = name
        self.content = content
        self.review = review
        self.description = description
        self.analysis = analysis
        self.hidden = 1
        self.timelimit = timelimit
        self.memorylimit = memorylimit
        self.show_limits = True
        self.output_only = output_only
        self.sample_tests = sample_tests
        self.sample_tests_html = sample_tests_html

#    def __repr__(self):
#        return "<spam(%d, '%s')" % (self.id, self.name)

class EjudgeProblem(Problem):
    __tablename__ = "mdl_ejudge_problem"
    __table_args__ = {'schema':'moodle'}
    __mapper_args__ = {'polymorphic_identity': 'ejudgeproblem'}
    
#    id = Column(Integer, ForeignKey('moodle.mdl_problems.pr_id'), primary_key=True)
    ejudge_prid = Column('id', Integer, primary_key=True)
    contest_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    ejudge_contest_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    problem_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    short_id = Column(String(100))
    ejudgeName = Column('name', String(100))
    runs = relation('Run', backref='runs', uselist=True)
 
    def __init__(self, name, timelimit, memorylimit, output_only, contest_id, problem_id, short_id, ejudge_contest_id, content='', review='', description='', analysis='', sample_tests='', sample_tests_html=''):
        self.name = name
        self.content = content
        self.review = review
        self.description = description
        self.analysis = analysis
        self.hidden = 1
        self.timelimit = timelimit
        self.memorylimit = memorylimit
        self.contest_id = contest_id
        self.ejudge_contest_id = ejudge_contest_id
        self.problem_id = problem_id
        self.short_id = short_id
        self.ejudgeName = name
        Problem.__init__(self, name, timelimit, memorylimit, output_only, content, review, description, analysis, sample_tests, sample_tests_html)
       
    def get_test(self, test_num):
        conf = EjudgeContestCfg(number = self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        test_file_name = (prob.tests_dir + prob.test_pat) % int(test_num)
        if os.path.exists(test_file_name):
            f = open(test_file_name)
            res = f.read(255)
        else:
            res = test_file_name
        return res
       
    def get_corr(self, test_num):
        conf = EjudgeContestCfg(number = self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        corr_file_name = (prob.tests_dir + prob.corr_pat) % int(test_num)
        if os.path.exists(corr_file_name):
            f = open(corr_file_name)
            res = f.read(255)
        else:
            res = corr_file_name
        return res       
       
    def generateSamples(self):
        res = ""
        if self.sample_tests != '':
            res = "<div class='problem-statement'><div class='sample-tests'><div class='section-title'>Примеры</div>"
        
            for i in self.sample_tests.split(","):
                res += "<div class='sample-test'>"
                res += "<div class='input'><div class='title'>Входные данные</div><pre class='content'>"
                res += self.get_test(i)
                res += "</pre></div><div class='output'><div class='title'>Выходные данные</div><pre class='content'>"
                res += self.get_corr(i)
                res += "</pre></div></div>"
        
            res += "</div></div>"

        self.sample_tests_html = res    
        return self.sample_tests