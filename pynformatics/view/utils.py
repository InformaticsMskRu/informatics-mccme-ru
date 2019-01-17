import sys, traceback
import codecs
from phpserialize import *

__all__ = ["RequestGetUserId", "RequestCheckUserCapability", "getContestStrId"]

def RequestGetUserId(request):
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
        return -1


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
#       raise       
       return False
       
def getContestStrId(id):
    res = str(id)
    while len(res) < 6:
        res = "0" + res
    return res


def del_keys(_dict, keys):
    for key in keys:
        try:
            del _dict[key]
        except KeyError:
            pass


        
#def RequestGetUserCapability(request, capability):
#    str = "+++"
#    try:
#        fh = open('/home/httpd/moodledata/sessions/sess_qim5co7v50o0bcmm203oludun3')
#        fh = open('/home/httpd/moodledata/sessions/sess_qe85bsigjr72lsp9kkf71rf9k1')
#        str = fh.read(512000)
#        user = loads(str[str.find('USER|') + 5:], object_hook=phpobject)
#        return "234"
#        fh.close()
#        return user.capabilities[1]
#    except ValueError as (e):
#        fh.close() 
#        return "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
#    except:
#        return "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
