from pyramid.view import view_config

from pynformatics.model.run import Run
from pynformatics.models import DBSession
from pynformatics.utils.exceptions import (
    RunNotFound,
)
from pynformatics.utils.validators import (
    IntParam,
    validate_params,
)

@view_config(route_name='notification.update_standings', renderer='json')
@validate_params(
    IntParam('contest_id', required=True),
    IntParam('run_id', required=True),
)
def notification_update_standings(request):
    """
    Обновляет таблицы результатов, в которых есть посылка
    """
    contest_id = int(request.params['contest_id'])
    run_id = int(request.params['run_id'])

    try:
        run = DBSession.query(Run).filter_by(
            contest_id=contest_id
        ).filter_by(
            run_id=run_id
        ).one()
    except Exception:
        raise RunNotFound

    if run.problem.standings:
        run.problem.standings.update(run.user)

    if (run.pynformatics_run
            and run.pynformatics_run.statement
            and run.pynformatics_run.statement.standings
    ):
        run.pynformatics_run.statement.standings.update(run)

    return {}
