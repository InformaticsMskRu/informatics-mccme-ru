from pyramid.response import Response
import random
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pynformatics.model import SimpleUser, User, EjudgeContest, EjudgeRun, Comment, EjudgeProblem, Problem
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.contest.ejudge.ejudge_proxy import submit
from pynformatics.view.utils import *
import sys, traceback
#import jsonpickle, demjson
from phpserialize import *
from pynformatics.view.utils import *
from pynformatics.models import DBSession
import transaction
#import jsonpickle, demjson
import json
import os
import time
from pynformatics.models import DBSession
#from webhelpers.html import *
from xml.etree.ElementTree import ElementTree
import xmlrpc.client

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


def send_mail(send_to, subject, text, files=[]):
    msg = MIMEMultipart()
    msg['From'] = 'ejudge.submitter'
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files:
        file_part = MIMEBase('application', "octet-stream")
        file_part.set_payload(open(f, 'rb').read())
        encoders.encode_base64(file_part)
        file_part.add_header('Content-Disposition', 
            'attachment; filename="{0}"'.format(os.path.basename(f)))
        msg.attach(file_part) 

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail('ejudge.submitter', send_to, msg.as_string())
    smtp.close()


@view_config(route_name='region.submit')
def region_submit(request):
    try:
        fl = False

        try:
           if request.POST:
               if hasattr(request.POST.get('fileInput'), 'filename'):
                   input_file = request.POST.get('fileInput').file
                   filename = request.POST.get('fileInput').filename
                   fl = True
        except Exception as e:
            fl = False
        url = request.POST['linkInput']

        newpath = '/var/region_result/' + time.strftime("%Y%m%d-%H%M%S") + "." + str(random.randint(1,1000))

        os.mkdir(newpath)
        if fl:
           with open(newpath + '/' + filename, 'wb') as newFile:
              newFile.write(input_file.read())

        with open(newpath + '/link.txt', 'w', encoding='utf-8') as newFile:
           newFile.write(url)

        files = [newpath + '/' + filename] if fl else []
        send_mail('vrandik@gmail.com', 'Region results', 
            'URL: {0}'.format(url), files)

        return HTTPFound(location='/map/index.html')
    except Exception as e:
        return Response("Error: " + e.__str__())

