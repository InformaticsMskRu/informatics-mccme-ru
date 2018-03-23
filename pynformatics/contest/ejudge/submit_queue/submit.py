import transaction
import logging

from pynformatics.contest.ejudge.ejudge_proxy import submit
from pynformatics.models import DBSession
from pynformatics.model.run import Run
from pynformatics.utils.context import Context
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.notify import notify_user


log = logging.getLogger('submit_queue')


def ejudge_error_notification(ejudge_response=None):
    code = None
    message = 'Ошибка отправки задачи'
    try:
        code = ejudge_response['code']
        message = ejudge_response['message']
    except Exception:
        pass
    return {
        'ejudge_error': {
            'code': code,
            'message': message,
        }
    }


class Submit:
    def __init__(self,
                 id,
                 context,
                 create_time,
                 file,
                 language_id,
                 ejudge_url,
                 ):
        self.id = id
        self.context = context
        self.create_time = create_time
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
    def source(self):
        if not hasattr(self, '_source'):
            self._source = self.file.file.read().decode('utf-8')
            self.file.file.seek(0)
        return self._source

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
                message=ejudge_error_notification(),
            )
            return

        try:
            if ejudge_response['code'] != 0:
                notify_user(
                    user_id=self.user.id,
                    message=ejudge_error_notification(ejudge_response)
                )
                return

            run_id = ejudge_response['run_id']
        except Exception:
            log.exception('ejudge_proxy.submit returned bad value')
            notify_user(
                user_id=self.user.id,
                message=ejudge_error_notification(),
            )
            return

        run = Run(
            user=self.user,
            problem=self.problem,
            statement_id=self.statement_id,
            create_time=self.create_time,
            ejudge_language_id=self.language_id,
        )
        DBSession.add(run)
        DBSession.flush([run])

        notify_user(
            user_id=self.user.id,
            runs=[run.serialize(self.context)],
            event={
                'type': 'RUN_CREATED_FROM_SUBMIT',
                'submit_id': self.id,
            }
        )

        transaction.commit()

    def encode(self):
        return {
            'id': self.id,
            'context': self.context.encode(),
            'create_time': self.create_time,
            'file': self.file,
            'language_id': self.language_id,
            'ejudge_url': self.ejudge_url,
        }

    @staticmethod
    def decode(encoded):
        context = Context.decode(encoded['context'])
        return Submit(
            id=encoded['id'],
            context=context,
            create_time=encoded['create_time'],
            file=encoded['file'],
            language_id=encoded['language_id'],
            ejudge_url=encoded['ejudge_url'],
        )
    
    def serialize(self, context, attributes=None):
        if attributes is None:
            attributes = (
                'id',
                'user_id',
                'problem_id',
                'source',
                'language_id',
            )
        serialized = attrs_to_dict(self, *attributes)
        if 'user_id' in attributes:
            serialized['user_id'] = self.user.id
        if 'problem_id' in attributes:
            serialized['problem_id'] = self.problem.id
        return serialized
