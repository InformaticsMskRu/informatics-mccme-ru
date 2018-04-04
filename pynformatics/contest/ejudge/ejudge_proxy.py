import codecs
import json
import requests
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import json

DEFAULT_ERROR_STR = 'Ошибка отправки задачи'

STATUS_REPR = {
  0 : 'Задача отправлена на проверку', # NEW_SRV_ERR_NO_ERROR
120 : 'Отправка пустого файла',        # NEW_SRV_ERR_FILE_EMPTY
105 : 'Отправка бинарного файла',      # NEW_SRV_ERR_BINARY_FILE
 82 : 'Эта посылка является копией предыдущей',# NEW_SRV_ERR_DUPLICATE_SUBMIT
 37 : 'Этот язык не может быть использован для этой задачи. Обратитесь к администраторам.',
 83 : 'Задача уже решена',             # NEW_SRV_ERR_PROB_ALREADY_SOLVED
 78 : 'Отправляемый файл превышает допустимый размер (64K) или превышена квота на число посылок (обратитесь к админимтратору)', # NEW_SRV_ERR_RUN_QUOTA_EXCEEDED
113 : 'Отправляемый файл пустой', # SUBMIT_EMPTY 
1000: 'Отправляемый файл превышает допустимый размер. Требуется отправить исходный код или текстовый файл',
}


def report_error(code, login_data, submit_data, file, filename, user_id, addon = ''):
    t = str({'info' : addon, 'login_data' : login_data, 'submit_data' : submit_data, 'filename' : filename})
    log=codecs.open('/var/log/python.log', 'a', 'utf-8')
    log.write(t)
    log.write('\n---\n')
    log.close()


def submit(run_file, contest_id, prob_id, lang_id, login, password, filename, url, user_id):
    login_data = {
        'contest_id' : contest_id,
        'role' : '0',
        'login' : login,
        'password' : password,
        'locale_id' : '1',
    }

    c = requests.post(url, data = login_data)
    res = re.search('SID="([^"]*)";', c.text)

    if (res):
        SID = res.group(1)
    else:
        report_error(None, login_data, c.text, run_file, filename, user_id)
        return {
            'code': None,
            'message': DEFAULT_ERROR_STR
        }

    cookies = c.cookies
    files = {'file' : (filename, run_file)}

    submit_data = {
        'SID' : SID,
        'prob_id' : prob_id,
        'lang_id' : lang_id,
        'action_40' : 'action_40',
        'json' : 1,
    }

    c = requests.post(url, data=submit_data, cookies=cookies, files=files)

    resp = json.loads(c.text)

    if 'run_id' in resp:
        return {
            'code': 0,
            'message': STATUS_REPR[0],
            **resp
        }

    code = resp["error_code"]
    if code in STATUS_REPR:
        return {
            'code': code,
            'message': STATUS_REPR[code]
        }
    elif -code in STATUS_REPR:
        return {
            'code': -code,
            'message': STATUS_REPR[-code]
        }
    else:
        report_error(code, login_data, submit_data, run_file, filename, user_id, c.text)
        return {
            'code': None,
            'message': DEFAULT_ERROR_STR + " (" + str(code) + ")",
        }


def rejudge(contest_id, run_id, status_id, login, password, url):
    login_data = {
        'contest_id' : contest_id,
        'role' : '6',
        'login' : login,
        'password' : password,
        'locale_id' : '1',
    }

    c = requests.post(url, data = login_data, allow_redirects = True)

#    return c.text

    res = re.search("SID='([^']*)';", c.text)

    if (res):
        SID = res.group(1)
    else:
        return "login error " + c.text

    cookies = c.cookies

    submit_data = {
        'SID' : SID,
        'run_id' : run_id,
        'status' : status_id,
        'action_68' : 'action_68'
    }

    c = requests.post(url, data = submit_data, cookies = cookies, allow_redirects=True)

    if "method=\"post\"" in c.text:
        return "ok"

    ret_code = re.search('code\'\s\:\s(\d*)', c.text)

    if (ret_code):
        code = int(ret_code.group(1))
        if code in STATUS_REPR:
            return STATUS_REPR[code]
        else:
            return "error" + str(code)
    else:
        return "change error"

