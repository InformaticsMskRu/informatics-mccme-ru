import transaction
import logging

from pynformatics.contest.ejudge.ejudge_proxy import submit
from pynformatics.models import DBSession
from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.utils.notify import notify_user


log = logging.getLogger(__name__)


class Submit:
    def __init__(self,
                 context,
                 file,
                 language_id,
                 ejudge_url,
                 ):
        self.context = context
        self.file = file
        self.language_id = language_id
        self.ejudge_url = ejudge_url

    @property
    def user(self):
        return self.context.user

    @property
    def problem(self):
        return self.context.problem

    @property
    def statement_id(self):
        if not self.context.statement_id:
            return None
        return self.context.statement_id

    def send(self):
        try:
            ejudge_response = submit(
                run_file=self.file.file,
                contest_id=self.problem.ejudge_contest_id,
                prob_id=self.problem.problem_id,
                lang_id=self.language_id,
                login=self.user.login,
                password=self.user.password,
                filename=self.file.filename,
                url=self.ejudge_url,
                user_id=self.user.id
            )
        except Exception:
            log.exception('Unknown Ejudge submit error')
            notify_user(
                user_id=self.user.id,
                data={
                    'ejudge_error': {
                        'code': None,
                        'message': 'Ошибка отправки задачи'
                    }
                }
            )
            return

        try:
            if ejudge_response['code'] != 0:
                notify_user(
                    user_id=self.user.id,
                    data={
                        'ejudge_error': {
                            'code': ejudge_response.get('code', ''),
                            'message': ejudge_response.get('message', ''),
                        }
                    }
                )
                return

            run_id = ejudge_response['run_id']
        except Exception:
            log.exception('ejudge_proxy.submit returned bad value')
            notify_user(
                user_id=self.user.id,
                data={
                    'ejudge_error': {
                        'code': None,
                        'message': 'Ошибка отправки задачи'
                    }
                }
            )
            return

        pynformatics_run = PynformaticsRun(
            run_id=run_id,
            contest_id=self.problem.ejudge_contest_id,
            statement_id=self.statement_id,
            source=self.file.value.decode('unicode_escape'),
        )
        pynformatics_run = DBSession.merge(pynformatics_run)
        DBSession.flush([pynformatics_run])
        DBSession.refresh(pynformatics_run.run)

        notify_user(
            user_id=self.user.id,
            runs=[pynformatics_run.run.serialize(self.context)],
        )

        transaction.commit()
