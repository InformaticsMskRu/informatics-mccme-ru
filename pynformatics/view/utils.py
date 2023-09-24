import sys, traceback
import codecs
import requests
from phpserialize import *

CONTEXT_SHIFT = 100000

__all__ = ["RequestGetUserId", "RequestCheckUserCapability", "getContestStrId", "GetUserIds", "GetUserCourseContextParams", "CONTEXT_SHIFT"]

def GetUserIds(request, cmid, moodle_group_id = 0):
    params = {
        'wstoken': request.registry.settings['moodle.master_token'],
        'wsfunction': 'core_course_get_enrolled_users_by_cmid',
        'cmid': cmid,
        'groupid': moodle_group_id,
        'moodlewsrestformat': 'json',
    }
    headers = {'Host': request.registry.settings['moodle.host']}
    r = requests.post(request.registry.settings['moodle.url'], params=params, headers=headers)
    result = r.json()
    if "users" not in result:
        return []
    return [e["id"] for e in result["users"]]

def RequestGetUserId(request):
    """Returns <=2 if not authorised"""

    if 'MoodleSession' not in request.cookies:
        return -1

    fh = None
    try:
        fh = codecs.open('/var/moodledata/sessions/sess_'+request.cookies['MoodleSession'], "r", "utf-8")
        str = fh.read(512000)
        user = loads(bytes(str[str.find('USER|') + 5:], 'UTF-8'), object_hook = phpobject, decode_strings = True)
        fh.close()
        return user.id
    except:
        if fh != None:
            fh.close()
        
    params = {
        'wstoken': request.registry.settings['moodle.token'],
        'wsfunction': 'local_pynformatics_has_capability',
        'moodlesid': request.cookies['MoodleSession'],
        'moodlewsrestformat': 'json',
        'capability': ''
    }
    headers = {'Host': request.registry.settings['moodle.host']}
    r = requests.post(request.registry.settings['moodle.url'], params=params, headers=headers)
    if "user_id" not in r.json():
        return -1
    user_id = int(r.json()["user_id"])
    if user_id <= 0:
        user_id = -1
    return user_id

def RequestCheckUserCapability(request, capability, courseid = 0):
    fh = None
    if 'MoodleSession' not in request.cookies:
        return False

    #try:
    #    fh = codecs.open('/var/moodledata/sessions/sess_'+request.cookies['MoodleSession'], "r", "utf-8")
    #    str = fh.read(512000)
    #    user = loads(bytes(str[str.find('USER|') + 5:], 'UTF-8'), object_hook=phpobject, decode_strings=True)
    #    fh.close()
    #    return int(user.capabilities[1][capability]) >= 1
    #except:
    #   if fh != None:
    #       fh.close()

    params = {
        'wstoken': request.registry.settings['moodle.token'],
        'wsfunction': 'local_pynformatics_has_capability',
        'moodlesid': request.cookies['MoodleSession'],
        'moodlewsrestformat': 'json',
        'capability': capability,
        'courseid': courseid,
    }
    headers = {'Host': request.registry.settings['moodle.host']}
    r = requests.post(request.registry.settings['moodle.url'], params=params, headers=headers)
    result = r.json()
    if "user_id" not in result:
        return False
    user_id = int(result["user_id"])
    if user_id <= 0:
        return False

    return result['capability']['status']

def getContestStrId(id):
    res = str(id)
    while len(res) < 6:
        res = "0" + res
    return res


def is_authorized_id(user_id):
    return int(user_id) > 2

def GetUserCourseContextParams(request, course_role, admin_role):

    user_id = RequestGetUserId(request)
    if not is_authorized_id(user_id):
        return None

    is_admin = RequestCheckUserCapability(request, admin_role)

    is_teacher = False
    course_id = 0
    if "course_id" in request.params and len(request.params["course_id"]) > 0:
        course_id = int(request.params["course_id"])

    if course_id > 0:
        is_teacher = RequestCheckUserCapability(request, course_role, course_id)

    params = {
        'is_admin': is_admin,
        'user_id': user_id,
    }

    if is_teacher > 0:
        params['context_source'] = course_id + CONTEXT_SHIFT

    return params
