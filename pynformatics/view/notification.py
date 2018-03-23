from pyramid.view import view_config

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.models import DBSession
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import (
    RunNotFound,
)
from pynformatics.utils.notify import notify_user
from pynformatics.utils.validators import (
    IntParam,
    validate_params,
)

@view_config(route_name='notification.update_standings', renderer='json')
@validate_params(
    IntParam('contest_id', required=True),
    IntParam('run_id', required=True),
)
@with_context
def notification_update_standings(request, context):
    """
    Обновляет таблицы результатов, в которых есть посылка
    """
    contest_id = int(request.params['contest_id'])
    run_id = int(request.params['run_id'])

    try:
        run = DBSession.query(EjudgeRun).filter_by(
            contest_id=contest_id
        ).filter_by(
            run_id=run_id
        ).one()
    except Exception:
        raise RunNotFound

    # if run.problem.standings:
    #     run.problem.standings.update(run.user)

    if (run.pynformatics_run
            and run.pynformatics_run.statement
            and run.pynformatics_run.statement.standings
    ):
        run.pynformatics_run.statement.standings.update(run)

    context.user_id = run.user.id
    notify_user(user_id=run.user.id, runs=[run.serialize(context)])

    return {}
