import os
import xml.dom.minidom
import xml
import gzip

contest_path = '/home/judges/'
protocols_path = 'var/archive/xmlreports'
audit_path = 'var/archive/audit'
sources_path = 'var/archive/runs'

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

def get_protocol_from_file(filename): 
    if os.path.isfile(filename):
        myopen = open
    else:
        filename += '.gz'
        myopen = gzip.open
    try:
        xml_file = myopen(filename, 'r')
        try:
            xml_file.readline()
            xml_file.readline()
            res = xml_file.read()
            try:
                return str(res, encoding='UTF-8')
            except TypeError:
                return res
        except:
            return ''
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
    }[s]

def submit_path(tp, contest_id, submit_id): #path to archive file with path to archive directory = tp, look up audit_path etc constants 
    return os.path.join(contest_path, '0' * (6 - len(str(contest_id))) + str(contest_id), tp, to32(submit_id // 32 // 32 // 32 % 32), 
    to32(submit_id // 32 // 32 % 32), to32(submit_id // 32 % 32), '0' * (6 - len(str(submit_id))) + str(submit_id))

def safe_open(path, tp):
    """ Funtion for open file with path is equal to parametr path. It tries to open as plain file,
        than as gz archive. Returnes filelike object.
    """
    try:
        file = open(path, tp)
    except FileNotFoundError as e:
        file = gzip.open(path + ".gz", tp)
    return file


def to32(num):
    if num < 10:
        return str(num)
    else:
        return chr(ord('A') + num - 10)