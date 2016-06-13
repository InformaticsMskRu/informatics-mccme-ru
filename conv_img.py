from datetime import datetime
from pyramid.paster import get_appsettings
from pyramid.config import Configurator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
    sessionmaker,
)
import sys
import lxml.html, lxml.etree
from urllib.parse import urlparse
import os.path
import urllib.request

from source_tree.model.problem import Problem

DBSession = sessionmaker()

settings = get_appsettings('dev-source.ini', 'main')
engine = engine_from_config(settings, 'sqlalchemy.')
DBSession.configure(bind=engine)

Base = declarative_base()

Base.metadata.bind = engine
db_session = DBSession()



problems = db_session.query(Problem).all()

total = 0
for problem in problems:
    if not problem.content:
        continue
    content = problem.content
    doc = lxml.html.document_fromstring(content)
    ch = False
    for img in doc.cssselect("img"):
        total += 1
        url = img.get("src")
        parse_result = urlparse(url)
        netloc = parse_result.netloc
        path = parse_result.path
        if netloc not in ["informatics.mccme.ru", "www.informatics.ru", ""]:
            try:
                dir_name = "/var/www/moodle/problem_img/" + str(problem.id)
                file_name = path.split("/")[-1]
                file_path = dir_name + "/" + file_name
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                if not os.path.exists(file_path):
                    urllib.request.urlretrieve(url, file_path)
                print(problem.id, "|", netloc) 
                print(file_name)
                img.set("src", "http://informatics.mccme.ru/moodle/problem_img/%s/%s" % (problem.id, file_name))
                print("http://informatics.mccme.ru/moodle/problem_img/%s/%s" % (problem.id, file_name))
                ch = True
            except Exception as e:
                print(e.__str__())
    if ch:
        pass
        #new_content = lxml.etree.tostring(doc, encoding="utf-8").decode("utf-8")
        #problem.content = new_content

db_session.commit()
