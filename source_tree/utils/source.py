from source_tree.models import db_session, Source, Problem, StatementProblem


class Basket:
    def __init__(self, contest_id, course_id):
        self.contest_id = contest_id
        self.course_id = course_id
        self.problems = []
        
    def add(self, problem_id):
        self.problems.append(problem_id)
    
    def erase(self, ind):
        del self.problems[ind]

    def move(self, ind, move_type):
        if move_type == 'up':
            ind -= 1
        self.problems[ind], self.problems[ind + 1] = \
            self.problems[ind + 1], self.problems[ind]


def source_add_by_dict(params):
    db_session.add(Source(
        name=params['name'], 
        parent_id=params['parent_id'], 
        order=params['order'],
        problem_id=params['problem_id'],
        author=params['author'],
        verified=params['verified']
    ))
    

def source_get_by_id(source_id):
    return db_session.query(Source).filter(Source.id == source_id).one()
    

def source_get_all_by_node(source, sources = None):
    if not sources:
        sources = []
    children = db_session.query(Source).filter(
        Source.parent_id == source.id,
        Source.problem_id == 0
    ).order_by(Source.order, Source.name).all()
    for child in children:
        sources.append(child)
        source_get_all_by_node(child, sources)
    return sources
    

def source_get_children_with_problems(source):
    return db_session.query(Source).filter(
        Source.parent_id == source.id,
        Source.problem_id > 0
    ).order_by(Source.order, Source.name).all()
    

def source_get_children_without_problems(source):
    return db_session.query(Source).filter(
        Source.parent_id == source.id,
        Source.problem_id == 0
    ).order_by(Source.order, Source.name).all()
    

def source_get_problems_all(source):
    tree = [source] + source_get_all_by_node(source)
    problems_id = set()
    for source_in_tree in tree:
        for child in source_get_children_with_problems(source_in_tree):
            if child.verified:
                problems_id.add(child.problem_id)
    return problems_id    
    

def source_get_root(source_type):
    return db_session.query(Source).filter(
        Source.parent_id == 1, 
        Source.name == '_' + source_type
    ).one()
