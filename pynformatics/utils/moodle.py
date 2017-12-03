import codecs
import requests
from phpserialize import loads, phpobject


def sign_in(username, password):
    url = 'http://localhost:8080/login/index.php'
    response = requests.post(
        url,
        {
            'username': username,
            'password': password,
        }
    )
    session_cookie = response.cookies.get('MoodleSession')
    user_id = get_user_id_by_session(session_cookie)
    return user_id, session_cookie


def get_user_id_by_session(session):
    fh = None
    try:
        fh = codecs.open('/var/moodledata/sessions/sess_%s' % session, 'r', 'utf-8')
        str = fh.read(512000)
        user = loads(bytes(str[str.find('USER|') + 5:], 'UTF-8'), object_hook=phpobject, decode_strings=True)
        fh.close()
        return user.id
    except:
        if fh:
            fh.close()
        return -1
