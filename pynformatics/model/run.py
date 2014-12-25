"""Run model"""
from sqlalchemy import *
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import *

from pynformatics.model.meta import Base
from pynformatics.models import DBSession

import os
import xml.dom.minidom
import xml
import gzip

contest_path = '/home/judges/'
protocols_path = 'var/archive/xmlreports'
audit_path = 'var/archive/audit'

def get_protocol_from_file(filename): 
    if os.path.isfile(filename):
        myopen = open
    else:
        filename += '.gz'
        myopen = gzip.open
    try:
        xml_file = myopen(filename, 'rb')
        try:
            xml_file.readline()
            xml_file.readline()
            res = xml_file.read()
            try:
                return str(res, encoding='UTF-8')
            except TypeError:
                return res
        except Exception as e:
            return str(e)
    except IOError:
        return ''


def get_string_status(s):
    return {
        "OK" : "OK",
        "WA" : "Неправильный ответ",
        "ML" : "Превышение лимита памяти",
        "SE" : "Security error",
        "CF" : "Ошибка проверки,<br/>обратитесь к администраторам",
        "PE" : "Неправильный формат вывода",
        "RT" : "Ошибка во время выполнения программы",
        "TL" : "Превышено максимальное время работы",     
        "WT" : "Превышено максимальное общее время работы",     
        "SK" : "Пропущен",     
    }[s]

def to32(num):
    if num < 10:
        return str(num)
    else:
        return chr(ord('A') + num - 10)

def submit_protocol_path(contest, submit_id):
    return os.path.join(contest_path, '0' * (6 - len(str(contest))) + str(contest), protocols_path, to32(submit_id // 32 // 32 // 32 % 32), 
    to32(submit_id // 32 // 32 % 32), to32(submit_id // 32 % 32), '0' * (6 - len(str(submit_id))) + str(submit_id))

def submit_audit_path(contest, submit_id):
    return os.path.join(contest_path, '0' * (6 - len(str(contest))) + str(contest), audit_path, to32(submit_id // 32 // 32 // 32 % 32), 
    to32(submit_id // 32 // 32 % 32), to32(submit_id // 32 % 32), '0' * (6 - len(str(submit_id))) + str(submit_id))

class DoubleException(Exception):
    pass
    
def lazy(func):
        """ A decorator function designed to wrap attributes that need to be
        generated, but will not change. This is useful if the attribute is  
        used a lot, but also often never used, as it gives us speed in both
        situations."""
        def cached(self, *args):
            name = "_"+func.__name__
            try:
                return getattr(self, name)
            except AttributeError as e:
                pass
               
            value = func(self, *args)
            setattr(self, name, value)
            return value
        return cached

class Run(Base):
    __tablename__ = "runs"
    __table_args__ = (
        ForeignKeyConstraint(['contest_id', 'prob_id'], ['moodle.mdl_ejudge_problem.ejudge_contest_id', 'moodle.mdl_ejudge_problem.problem_id']),
        ForeignKeyConstraint(['user_id'], ['moodle.mdl_user.ej_id']),
        {'schema':'ejudge'}
        )

   
    run_id = Column(Integer, primary_key=True)
    size = Column(Integer)
    create_time = Column(DateTime)
    user_id = Column(Integer)
    user = relationship('SimpleUser', backref = backref('simpleuser'), uselist=False)
    comments = relation('Comment', backref = backref('comments'))
    contest_id = Column(Integer)
    prob_id = Column(Integer)
#    ForeignKeyConstraint(['contest_id', 'prob_id'], ['moodle.mdl_ejudge_problem.contest_id', 'moodle.mdl_ejudge_problem.problem_id'])
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
        self.user_id = user_id
        self.prob_id = prob_id
        self.lang_id = lang_id
        self.status = status
        self.score = score
        self.test_num = test_num

#    def __repr__(self):
#        return "Run(%s, %s, %s, '%s', %s, %s, %s, %s, %s, %s)" % (self.run_id, self.contest_id, self.size, self.create_time, self.user_id, \
#          self.prob_id, self.lang_id, self.status, self.score, self.test_num)
    
    @lazy      
    def _get_compilation_protocol(self): 
        filename = submit_protocol_path(self.contest_id, self.run_id)
#        return filename
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
        filename = submit_protocol_path(self.contest_id, self.run_id)
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

    @lazy
    def get_audit(self):
        return open(submit_audit_path(self.contest_id, self.run_id), "r").read();

    

    def parsetests(self):
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
                try:
                    inp = node.getElementsByTagName('input')[0].firstChild.nodeValue
                    outp = node.getElementsByTagName('output')[0].firstChild.nodeValue
                    corr = node.getElementsByTagName('correct')[0].firstChild.nodeValue
                    stderr = node.getElementsByTagName('stderr')[0].firstChild.nodeValue
                    checker = node.getElementsByTagName('checker')[0].firstChild.nodeValue
                    judge_info['input'] = inp
                    judge_info['checker'] = checker
                    judge_info['output'] = outp
                    judge_info['correct'] = corr
                    judge_info['stderr'] = stderr
                except:
                    pass

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
    
    tested_protocol = property(_get_tested_protocol_data)
    
    def get_by(run_id, contest_id):
        try:
            return DBSession.query(Run).filter(Run.run_id == int(run_id)).filter(Run.contest_id == int(contest_id)).first()            
        except:
            return None
    get_by = staticmethod(get_by)