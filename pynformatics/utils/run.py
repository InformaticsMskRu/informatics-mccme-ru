import os
import xml.dom.minidom
import xml
import gzip

__all__ = ['get_protocol_from_file']

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
