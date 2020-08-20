from source_tree.model.role import Role, Context, RoleAssignment
from pynformatics.models import DBSession
from pynformatics.view.utils import RequestGetUserId
import sys

def check_global_role(roles):
    ''' decorator for view function
        roles = string or iterable of strings - shorttitle from mdl_roles 
        (admin, teascher, ejudge_teacher etc)

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
                if req.filter_by(roleid=roleid).all():
                    result = func(request, *args, **kwargs)
                    return result    

            result = {'result': 'autherror', 'message': 'You do not have permissions for this operation', "role": additional_message, "userid": userid}
            return result

        return tmp
    return wrapper

def is_admin(request):
    userid = RequestGetUserId(request)
    req = DBSession.query(RoleAssignment).filter_by(userid=userid)
    try:
        role_admin_id = DBSession.query(Role).filter(or_(Role.shortname=='admin', Role.shortname=='manager')).one().id
    except:
        return False
    return bool(req.filter_by(roleid=role_admin_id).all())

