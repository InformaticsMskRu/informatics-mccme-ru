from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound

from pynformatics.model.user import User
from pynformatics.model.user_oauth_provider import UserOAuthProvider
from pynformatics.models import DBSession
from pynformatics.utils import moodle
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import (
    AuthOAuthUserNotFound,
    AuthWrongUsernameOrPassword,
)
from pynformatics.utils.functions import check_password
from pynformatics.utils.oauth import get_oauth_id


@view_config(route_name='auth.login', renderer='json', request_method='POST')
@with_context
def auth_login(request, context):
    if not context.user:
        username = request.json_body.get('username')
        password = request.json_body.get('password')
        try:
            user = DBSession.query(User).filter(
                User.username == username
            ).one()
        except NoResultFound:
            raise AuthWrongUsernameOrPassword
        if not check_password(password, user.password_md5):
            raise AuthWrongUsernameOrPassword

        # Сквозная авторизация в moodle. Бесполезна, потому что
        # moodle_user_id, moodle_session = moodle.sign_in(username=username, password=password)
        # if user.id == moodle_user_id:
        #     request.response.set_cookie('MoodleSession', moodle_session)
    else:
        user = context.user

    request.session['user_id'] = user.id
    return user.serialize(context)


@view_config(route_name='auth.logout', renderer='json', request_method='POST')
@with_context(require_auth=True)
def auth_logout(request, context):
    request.session['user_id'] = None
    request.response.set_cookie('MoodleSession', '')
    return {}


@view_config(route_name='auth.oauth_login', renderer='json', request_method='POST')
@with_context
def auth_oauth_login(request, context):
    provider = request.json_body.get('provider')
    code = request.json_body.get('code')
    oauth_id = get_oauth_id(provider, code)

    user_oauth_provider = DBSession.query(UserOAuthProvider).filter(
        UserOAuthProvider.provider == provider
    ).filter(
        UserOAuthProvider.oauth_id == oauth_id
    ).first()

    if not user_oauth_provider:
        raise AuthOAuthUserNotFound

    context.user_id = user_oauth_provider.user_id
    return auth_login(request, context)
