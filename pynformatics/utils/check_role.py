from pynformatics.model.role import Role, Context, RoleAssignment
from pynformatics.models import DBSession
from pynformatics.view.utils import RequestGetUserId
import sys

def check_global_role(roles):
    ''' decorator for view function
        roles = string or iterable of strings - shorttitle from mdl_roles 
        (admin, teacher, ejudge_teacher etc)

        If auth is ok, view function will not change. Otherwise it returns 
        dict {'result': 'autherror', message:'You do not have permissions for this operation'}
        and view function is not executed

        The first parameter of view should be request, containing the user info
    '''

    def wrapper(func):
        def tmp(request, *args, **kwargs):
            if type(roles) == str:
                roles_list = (roles, )
            else:
                roles_list = roles
            userid = RequestGetUserId(request)

            if userid == -1 and "guest" not in roles_list:
                return {'result': 'autherror', 'message': 'You do not have permissions for this operation'}
            
            req = DBSession.query(RoleAssignment).filter_by(userid=userid)
            additional_message = ""
            for role in roles_list:
                try:
                    roleid = DBSession.query(Role).filter_by(shortname=role).one().id
                    additional_message += role + "+ "
                except:
                    additional_message += role + "- "
                    continue
                if req.filter_by(roleid=roleid).all():
                    result = func(request, *args, **kwargs)
                    return result    

            result = {'result': 'autherror', 'message': 'You do not have permissions for this operation', "role": additional_message, "userid": userid}
            return result

        return tmp
    return wrapper

# Cached ids of the 'admin'/'manager' roles: role rows are seeded once and
# then static, so there is no need to hit mdl_role on every is_admin() call.
_admin_role_ids = None


def _get_admin_role_ids():
    global _admin_role_ids
    # Re-query while empty (roles may not be seeded yet); cache once populated.
    if not _admin_role_ids:
        _admin_role_ids = [
            r.id for r in DBSession.query(Role)
            .filter(Role.shortname.in_(('admin', 'manager')))
            .all()
        ]
    return _admin_role_ids


def is_admin(request):
    userid = RequestGetUserId(request)
    admin_role_ids = _get_admin_role_ids()
    if not admin_role_ids:
        return False
    return bool(
        DBSession.query(RoleAssignment)
        .filter(RoleAssignment.userid == userid)
        .filter(RoleAssignment.roleid.in_(admin_role_ids))
        .first()
    )

