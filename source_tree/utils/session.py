from phpserialize import *
import codecs


def get_session_object(request, session_type, session_dir, object_name):
    fh = None
    try:
        fh = codecs.open(session_dir + "/sess_" + request.cookies[session_type], "r", "utf-8")
        str = fh.read(512000)
        obj = loads(bytes(str[str.find(object_name + "|") + len(object_name) + 1:], 'UTF-8'), object_hook=phpobject, decode_strings=True)
        fh.close()
        return obj
    except:
        if fh:
            fh.close()
        return None


def get_php_session_object(request, object_name):
    return get_session_object(request, 'PHPSESSID', '/tmp/sessions', object_name)


def get_moodle_session_object(request, object_name):
    return get_session_object(request, 'MoodleSession', '/var/moodledata/sessions', object_name)


''' DEPRECATED, sometimes it works incorrect!'''
def update_session_object(request, session_type, session_dir, object_name, obj):
    fh = None
    try:
        fh = codecs.open(session_dir + "/sess_" + request.cookies[session_type], "r", "utf-8")
        str = fh.read(512000)
        fh.close()
        fh = codecs.open(session_dir + "/sess_" + request.cookies[session_type], "w", "utf-8")
        obj_len = len(dumps(loads(bytes(str[str.find(object_name + "|") + len(object_name) + 1:], \
                'UTF-8'), object_hook=phpobject, decode_strings=True), object_hook=phpobject))
        start_pos = str.find(object_name + "|") + len(object_name) + 1
        list_by_str = list(str)
        list_by_str[start_pos:start_pos + obj_len] = list(dumps(obj, object_hook=phpobject).decode('utf-8'))
        fh.write(''.join(list_by_str))
        fh.close()
    except:
        if fh:
            fh.close()

''' DEPRECATED '''
def update_php_session_object(request, object_name, obj):
    update_session_object(request, 'PHPSESSID', '/tmp/sessions', object_name, obj)


''' DEPRECATED '''
def update_moodle_session_object(request, object_name, obj):
    update_session_object(request, 'MoodleSession', '/var/moodledata/sessions', object_name, obj)


def rollback_on_request_finished(_):
    # We have to use local import because db_session is monkey patch
    # of source_tree.models and this object is not exists when current file imported
    from source_tree.models import db_session
    if db_session.is_active:
        db_session.rollback()


def subscribe_rollback_on_request_finished(request):
    request.request.add_finished_callback(rollback_on_request_finished)

