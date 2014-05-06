from source_tree.models import db_session, Source, Problem


def problem_get_by_id(problem_id):
    return db_session.query(Problem).filter(Problem.id == problem_id).one()
