import os
import codecs
import glob
from zipfile import ZipFile

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Float, Unicode, Boolean
from sqlalchemy.orm import reconstructor
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg

from pynformatics.model.meta import Base
from pynformatics.utils.run import read_file_unknown_encoding
from pynformatics.utils.json_type import JsonType


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
    sample_tests_json = Column(JsonType)
    show_limits = Column(Boolean)
    output_only = Column(Boolean)
    pr_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_problem.id'))
#    ejudge_users = relation('EjudgeUser', backref="moodle.mdl_user", uselist=False)
#    ejudge_user = relation('EjudgeUser', backref = backref('moodle.mdl_user'), uselist=False, primaryjoin = "EjudgeUser.user_id == User.id")
    def __init__(self, name, timelimit, memorylimit, output_only, content='', review='', description='', analysis='', sample_tests='', sample_tests_html='', pr_id=None):
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
        self.pr_id = pr_id
#    def __repr__(self):
#        return "<spam(%d, '%s')" % (self.id, self.name)

class EjudgeProblemDummy(Base):
    __tablename__ = "mdl_ejudge_problem"
    __table_args__ = {'schema':'moodle', 'extend_existing': True}

    ejudge_prid = Column('id', Integer, primary_key=True) #global id in ejudge
    contest_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    ejudge_contest_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    secondary_ejudge_contest_id = Column(Integer, nullable=True)
    problem_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False) #id in contest
    short_id = Column(String(100))
    ejudgeName = Column('name', String(100))
#    runs = relation('Run', backref='runs', uselist=True)
 
    def __init__(self, name, contest_id, problem_id, short_id, ejudge_contest_id):
        self.contest_id = contest_id
        self.ejudge_contest_id = ejudge_contest_id
        self.problem_id = problem_id
        self.short_id = short_id
        self.ejudgeName = name


class EjudgeProblem(Problem):
    __tablename__ = "mdl_ejudge_problem"
    __table_args__ = {'schema':'moodle', 'extend_existing': True}
    __mapper_args__ = {'polymorphic_identity': 'ejudgeproblem'}

#    id = Column(Integer, ForeignKey('moodle.mdl_problems.pr_id'), primary_key=True)
    ejudge_prid = Column('id', Integer, primary_key=True, autoincrement=True) #global id in ejudge
    contest_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    ejudge_contest_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    secondary_ejudge_contest_id = Column(Integer, nullable=True)
    problem_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False) #id in contest
    short_id = Column(String(100))
    ejudgeName = Column('name', String(100))
    # runs = relation('Run', backref='runs', uselist=True)
 
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

    def serialize(self, context):
        if self.sample_tests:
            self.generateSamplesJson(force_update=True)

        attrs = [
            'id',
            'name',
            'content',
            'timelimit',
            'memorylimit',
            'show_limits',
            'sample_tests_json',
            'output_only',
        ]
        problem_dict = {
            attr: getattr(self, attr, 'undefined')
            for attr in attrs
        }
        problem_dict['languages'] = context.get_allowed_languages()
        return problem_dict

    def get_test(self, test_num, size=255):
        conf = EjudgeContestCfg(number=self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        test_file_name = (prob.tests_dir + prob.test_pat) % int(test_num)
        error_str = None
        if os.path.exists(test_file_name):
            res = read_file_unknown_encoding(test_file_name, size)
        else:
            res = test_file_name
        return res

    def get_test_size(self, test_num):
        conf = EjudgeContestCfg(number=self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        test_file_name = (prob.tests_dir + prob.test_pat) % int(test_num)
        return os.stat(test_file_name).st_size
        
    def get_corr(self, test_num, size=255):
        conf = EjudgeContestCfg(number = self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        corr_file_name = (prob.tests_dir + prob.corr_pat) % int(test_num)
        error_str = None
        if os.path.exists(corr_file_name):
            res = read_file_unknown_encoding(corr_file_name, size)
        else:
            res = corr_file_name
        return res

    def get_test_full(self, test_num, size=255):
        """
        Возвращает словарь с полной информацией о тесте
        """
        test = {}
        if self.get_test_size(int(test_num)) <= 255:
            test["input"] = self.get_test(int(test_num), size=size)
            test["big_input"] = False
        else:
            test["input"] = self.get_test(int(test_num), size=size) + "...\n"
            test["big_input"] = True

        if self.get_corr_size(int(test_num)) <= 255:
            test["corr"] = self.get_corr(int(test_num), size=size)
            test["big_corr"] = False
        else:
            test["corr"] = self.get_corr(int(test_num), size=size) + "...\n"
            test["big_corr"] = True
        return test

    def get_corr_size(self, test_num):
        conf = EjudgeContestCfg(number = self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        corr_file_name = (prob.tests_dir + prob.corr_pat) % int(test_num)
        return os.stat(corr_file_name).st_size
        
    def get_checker(self):
        conf = EjudgeContestCfg(number = self.ejudge_contest_id)
        prob = conf.getProblem(self.problem_id)

        #generate dir with checker
        checker_dir = None
        if conf.advanced_layout:
            checker_dir = os.path.join(conf.contest_path, "problems", prob.internal_name)
        else:
            checker_dir = os.path.join(conf.contest_path, "checkers")

        #trying to find checker
        find_res = glob.glob(os.path.join(checker_dir, "check_{0}.*".format(prob.internal_name)))
        check_src = None
        checker_ext = None
        if find_res:
            check_src = open(find_res[0], "r").read()
            checker_ext = os.path.splitext(find_res[0])[1]
        
        #if checker not found then try polygon package
        downloads_dir = os.path.join(conf.contest_path, "download")
        if check_src is None and os.path.exists(downloads_dir):
            download_archive_mask = "{0}-*$linux.zip".format(prob.internal_name)
            find_archive_result = glob.glob(os.path.join(downloads_dir, download_archive_mask))
            download_archive_path = find_archive_result[0] if find_archive_result else None
            archive = None
            if download_archive_path is not None:
                archive = ZipFile(download_archive_path)
            if archive is not None:
                member_path = None
                for file in archive.namelist():
                    if file.startswith("check."):
                        member_path = file
                        break
                try:
                    check_src = archive.open(member_path).read()
                    checker_ext = os.path.splitext(member_path)[1]
                except KeyError:
                    check_src = None

        if check_src is None:
            check_src = "checker not found"

        return check_src, checker_ext

    def generateSamples(self):
        res = ""
        if self.sample_tests != '':
            res = "<div class='problem-statement'><div class='sample-tests'><div class='section-title'>Примеры</div>"
            
            for i in self.sample_tests.split(","):
                inp = self.get_test(i, 4096)
                if inp[-1] == '\n':
                    inp = inp[:-1]
                corr = self.get_corr(i, 4096)
                if corr[-1] == '\n':
                    corr = corr[:-1]
                res += "<div class='sample-test'>"
                res += "<div class='input'><div class='title'>Входные данные</div><pre class='content'>"
                res += inp
                res += "</pre></div><div class='output'><div class='title'>Выходные данные</div><pre class='content'>"
                res += corr
                res += "</pre></div></div>"
        
            res += "</div></div>"

        self.sample_tests_html = res    
        return self.sample_tests

    def generateSamplesJson(self, force_update=False):
        if self.sample_tests != '':
            if not self.sample_tests_json:
                self.sample_tests_json = {}
            for test in self.sample_tests.split(','):
                if not force_update and test in self.sample_tests_json:
                    continue

                test_input = self.get_test(test, 4096)
                test_correct = self.get_corr(test, 4096)

                self.sample_tests_json[test] = {
                    'input': test_input,
                    'correct': test_correct,
                }
