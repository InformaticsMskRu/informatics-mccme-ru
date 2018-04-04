import html
import json
import traceback
import transaction
from pyramid.view import view_config
from sqlalchemy.orm.exc import (
    MultipleResultsFound,
    NoResultFound,
)

from pynformatics.model.user import User
from pynformatics.model.user_oauth_provider import UserOAuthProvider
from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.models import DBSession
from pynformatics.view.utils import *
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import (
    UserOAuthIdAlreadyUsed,
    UserNotFound,
)
from pynformatics.utils.oauth import get_oauth_id


@view_config(route_name='user_settings.add', request_method='POST', renderer='json')
def add(request):
    try:
        if (not RequestCheckUserCapability(request, 'moodle/ejudge_submits:comment')):
            raise Exception("Auth Error")
        run = EjudgeRun.get_by(run_id = request.params['run_id'], contest_id = request.params['contest_id'])
        if not run:
            raise Exception("Object not found")
        user = DBSession.query(User).filter(User.id == RequestGetUserId(request)).first()
        comment = Comment(run, user, html.escape(request.params['lines']), html.escape(request.params['comment']));
        with transaction.manager:
            DBSession.add(comment);
        return {"result" : "ok"}
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='user_settings.get', renderer='string')
def get(request):
    try:
        user_id = request.matchdict['user_id']
        if int(user_id) != int(RequestGetUserId(request)):
            raise Exception("Auth Error")
    except Exception as e:
        return json.dumps({"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()})


@view_config(route_name='user.set_oauth_id', renderer='json', request_method='POST')
@with_context(require_auth=True)
def user_set_oauth_id(request, context):
    provider = request.json_body.get('provider')
    code = request.json_body.get('code')
    oauth_id = get_oauth_id(provider, code)

    if DBSession.query(UserOAuthProvider).filter(
                UserOAuthProvider.provider == provider
            ).filter(
                UserOAuthProvider.oauth_id == oauth_id
            ).first():
        raise UserOAuthIdAlreadyUsed

    user_oauth_provider = context.user.oauth_ids.filter(UserOAuthProvider.provider == provider).first()
    if user_oauth_provider:
        user_oauth_provider.oauth_id = oauth_id
    else:
        user_oauth_provider = UserOAuthProvider(
            user_id=context.user.id,
            provider=provider,
            oauth_id=oauth_id,
        )
        DBSession.add(user_oauth_provider)
    return {}


@view_config(route_name='user.reset_password', renderer='json', request_method='POST')
@with_context(require_auth=True, require_roles='admin')
def user_reset_password(request, context):
    id = request.json_body.get('id')

    user = DBSession.query(User).filter(User.id == id).first()
    if not user:
        raise UserNotFound

    new_password = user.reset_password()
    return {
        'id': user.id,
        'password': new_password,
    }
