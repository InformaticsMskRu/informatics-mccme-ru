"""Run model"""
from sqlalchemy import *
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import *

from pynformatics.model.meta import Base
from pynformatics.models import DBSession
from pynformatics.utils.run import *
from pynformatics.utils.ejudge_archive import EjudgeArchiveReader
from pynformatics.model.user import SimpleUser

import os
import xml.dom.minidom
import xml
import gzip

class Run(Base):
    __tablename__ = "runs"
    __table_args__ = (
        ForeignKeyConstraint(['contest_id', 'prob_id'], ['moodle.mdl_ejudge_problem.ejudge_contest_id', 'moodle.mdl_ejudge_problem.problem_id']),
        # ForeignKeyConstraint(['user_id'], ['moodle.mdl_user.ej_id']),
        {'schema':'ejudge'}
        )

    run_id = Column(Integer, primary_key=True)
    size = Column(Integer)
    create_time = Column(DateTime)
    # user_id = Column(Integer)
    # user = relationship('SimpleUser', backref = backref('simpleuser'), uselist=False)
    comments = relation('Comment', backref = backref('comments'))
    contest_id = Column(Integer, primary_key=True)
    prob_id = Column(Integer)
    problem = relationship('EjudgeProblem', backref = 'ejudgeproblem', uselist = False)
    lang_id = Column(Integer)
    status = Column(Integer)
    score = Column(Integer)
    test_num = Column(Integer)
    
    def __init__(self, run_id, contest_id, size, create_time, user_id, prob_id, lang_id, status, score, test_num):
        self.run_id = run_id
        self.contest_id = contest_id
        self.size = size
        self.create_time = create_time
        # self.user_id = user_id
        self.prob_id = prob_id
        self.lang_id = lang_id
        self.status = status
        self.score = score
        self.test_num = test_num

    @lazy
    def get_audit(self):
        data = safe_open(submit_path(audit_path, self.contest_id, self.run_id), "r").read()
        if type(data) == bytes:
            data = data.decode("ascii")
        return data
    @lazy
    def get_sources(self):
        data = safe_open(submit_path(sources_path, self.contest_id, self.run_id), "r").read()
        if type(data) == bytes:
            data = data.decode("ascii")
        return data

    def get_output_file(self, test_num, tp="o", size=None): #tp: o - output, e - stderr, c - checker
        data = self.get_output_archive().getfile("{0:06}.{1}".format(test_num, tp)).decode('ascii')
        if size is not None: 
            data = data[:size]
        return data

    def get_output_file_size(self, test_num, tp="o"): #tp: o - output, e - stderr, c - checker
        data = self.get_output_archive().getfile("{0:06}.{1}".format(test_num, tp)).decode('ascii')
        return len(data)


    def get_output_archive(self):
        if "output_archive" not in self.__dict__:
            self.output_archive = EjudgeArchiveReader(submit_path(output_path, self.contest_id, self.run_id))
        return self.output_archive

    def parsetests(self): #parse data from xml archive
        self.test_count = 0
        self.tests = {}
        self.judge_tests_info = {}
        self.status_string = None
        self.maxtime = None
        if self.xml:
            rep = self.xml.getElementsByTagName('testing-report')[0]
            self.tests_count = int(rep.getAttribute('run-tests'))
            self.status_string = rep.getAttribute('status')
            self.host = self.xml.getElementsByTagName('host')[0].firstChild.nodeValue
            try:
                self.compiler_output = self.xml.getElementsByTagName('compiler_output')[0].firstChild.nodeValue
            except:
                self.compiler_output = ""    
            for node in self.xml.getElementsByTagName('test'):
                number = node.getAttribute('num')
                status = node.getAttribute('status')
                time = node.getAttribute('time')
                real_time = node.getAttribute('real-time')
                max_memory_used = node.getAttribute('max-memory-used')
                self.test_count += 1
                try:
                   time = int(time)
                except ValueError:
                   time = 0

                try:
                   real_time = int(real_time)
                except ValueError:
                   real_time = 0
                   
                test = {'status': status, 
                        'string_status': get_string_status(status), 
                        'real_time': real_time, 
                        'time': time,
                        'max_memory_used' : max_memory_used
                       }
                judge_info = {}
            
                for _type in ('input', 'output', 'correct', 'stderr', 'checker'):
                    lst = node.getElementsByTagName(_type)
                    if lst and lst[0].firstChild:
                        judge_info[_type] = lst[0].firstChild.nodeValue
                    else:
                        judge_info[_type] = ""

                if node.hasAttribute('term-signal'):
                    judge_info['term-signal'] = int(node.getAttribute('term-signal'))
                if node.hasAttribute('exit-code'):
                    judge_info['exit-code'] = int(node.getAttribute('exit-code'))

                self.judge_tests_info[number] = judge_info
                self.tests[number] = test
            try:
                #print([test['time'] for test in self.tests.values()] + [test['real_time'] for test in self.tests.values()])
                self.maxtime = max([test['time'] for test in self.tests.values()] + [test['real_time'] for test in self.tests.values()])
            except ValueError:
                pass        
    
    
    def get_by(run_id, contest_id):
        try:
            return DBSession.query(Run).filter(Run.run_id == int(run_id)).filter(Run.contest_id == int(contest_id)).first()            
        except:
            return None

    @lazy      
    def _get_compilation_protocol(self): 
        filename = submit_path(protocols_path, self.contest_id, self.run_id)
        if filename:
            if os.path.isfile(filename):
                myopen = lambda x,y : open(x, y, encoding='utf-8')
            else:
                filename += '.gz'
                myopen = gzip.open
            try:
                xml_file = myopen(filename, 'r')
                try:
                    res = xml_file.read()
                    try:
                        res = res.decode('cp1251').encode('utf8')
                    except:
                        pass

                    try:
                        return str(res, encoding='UTF-8')
                    except TypeError:
                        try:
                            res = res.decode('cp1251').encode('utf8')
                        except Exception:
                            pass
                        return res
                except Exception as e:
                    return e
            except IOError as e:
                return e
        else:
            return ''
    
    @lazy      
    def _get_protocol(self): 
        filename = submit_path(protocols_path, self.contest_id, self.run_id)
        #filename = str((filename, protocols_path, self.contest_id, self.run_id))
        #return "<a>" + filename + "</a>"
        if filename != '':
            return get_protocol_from_file(filename)
        else:
            return '<a></a>'
            
    protocol = property(_get_protocol)
    compilation_protocol = property(_get_compilation_protocol)
    
    @lazy 
    def _get_tested_protocol_data(self):
        self.xml = xml.dom.minidom.parseString(str(self.protocol))
        self.parsetests()

    def _set_output_archive(self, val):
        self.output_archive = val

    tested_protocol = property(_get_tested_protocol_data)
    get_by = staticmethod(get_by)
