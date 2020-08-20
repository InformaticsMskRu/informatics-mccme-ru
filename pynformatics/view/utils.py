import sys, traceback
import codecs
import requests
from phpserialize import *

__all__ = ["RequestGetUserId", "RequestCheckUserCapability", "getContestStrId"]


def RequestGetUserId(request):
    """Returns <=2 if not authorised"""
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
    user_id = int(r.json()["user_id"])
    if user_id <= 0:
        user_id = -1
    return user_id

def RequestCheckUserCapability(request, capability):
    fh = None
    try:
        fh = codecs.open('/var/moodledata/sessions/sess_'+request.cookies['MoodleSession'], "r", "utf-8")
        str = fh.read(512000)
        user = loads(bytes(str[str.find('USER|') + 5:], 'UTF-8'), object_hook=phpobject, decode_strings=True)
        fh.close()
        return int(user.capabilities[1][capability]) >= 1
    except:
       if fh != None:
           fh.close()

    params = {
        'wstoken': request.registry.settings['moodle.token'],
        'wsfunction': 'local_pynformatics_has_capability',
        'moodlesid': request.cookies['MoodleSession'],
        'moodlewsrestformat': 'json',
        'capability': capability
    }
    headers = {'Host': request.registry.settings['moodle.host']}
    r = requests.post(request.registry.settings['moodle.url'], params=params, headers=headers)
    result = r.json()
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

