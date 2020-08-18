import os
import sys
import requests
from sqlalchemy import engine_from_config

from pyramid.paster import (get_appsettings)

sys.path.append('/var/pynformatics3/dev')

from sqlalchemy.orm import sessionmaker
from pynformatics.model.meta import Base

DBSession = sessionmaker()

from source_tree.model.course import Course

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(rating-table: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def add_category(settings, name, parent=0):
    params = {
        'wstoken': settings['moodle.master_token'],
        'wsfunction': 'core_course_create_categories',
        'moodlewsrestformat': 'json',
    }
    if not name:
        name = "Empty name"
    data = {
        'categories[0][name]': name,
        'categories[0][parent]': parent,
        'categories[0][description]': 'description',
    }
    headers = {'Host': settings['moodle.host']}
    r = requests.post(settings['moodle.url'], params=params, data=data, headers=headers)
    print(r.json())
    return r.json()[0]["id"]

def move_course(settings, category_id, course_id):
    params = {
        'wstoken': settings['moodle.master_token'],
        'wsfunction': 'core_course_update_courses',
        'moodlewsrestformat': 'json',
    }
    data = {
        'courses[0][id]': course_id,
        'courses[0][categoryid]': category_id,
    }
    headers = {'Host': settings['moodle.host']}
    r = requests.post(settings['moodle.url'], params=params, data=data, headers=headers)
    print(r.json())

def rec(settings, tree, cat_map, moodle_mapping, v):
    if v not in tree:
        return
    for i in tree[v]:
        e = cat_map[i]

        parent_id = e.parent_id
        if parent_id in moodle_mapping:
            parent_id = moodle_mapping[parent_id]
        else:
            parent_id = 0

        moodle_id = add_category(settings, e.name, parent_id)
        moodle_mapping[e.id] = moodle_id
        rec(settings, tree, cat_map, moodle_mapping, e.id)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    settings = get_appsettings(config_uri)
    print(settings['moodle.token'])
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    r = DBSession().query(Course).all()
    i = 0
    tree = dict()
    cat_map = dict()
    for e in r:
        if e.course_id == 0:
            if e.parent_id not in tree:
                tree[e.parent_id] = []
            tree[e.parent_id].append(e.id)
            cat_map[e.id] = e

    for i in tree[1]:
        e = cat_map[i]
        print(e.id, e.name, e.course_id, e.parent_id)
    moodle_mapping = dict()
    rec(settings, tree, cat_map, moodle_mapping, 1)


    for e in r:
        print(e.id, e.name, e.course_id, e.parent_id)
        if e.course_id != 0:
            move_course(settings, moodle_mapping[e.parent_id], e.course_id)
    # add_category(settings, 'Тестовая категория')
    # add_category(settings, 'Тестоваое изучение языка', 10)
    #move_course(settings, 61, 1579)
    #move_course(settings, 60, 1191)
if __name__ == "__main__":
    main()
#    Base.metadata.create_all(engine)
#    with transaction.manager:
#        model = MyModel(name='one', value=1)
#        DBSession.add(model)
