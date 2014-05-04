from pyramid.view import view_config

from .models import (
    DBSession,
    Comment,
    )

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    one = DBSession.query(Comment).filter(Comment.author_user_id==469).first()
    return {'one':one, 'project':'Pynformatics'}