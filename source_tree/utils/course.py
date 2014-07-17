from source_tree.models import (
    db_session, 
    Course,
    CourseRaw,
    CourseTreeCap,
    Role,
    RoleAssignment,
    Context,
    User,
)


def course_add_by_dict(params):
    course = Course(
        name=params['name'], 
        parent_id=params['parent_id'], 
        order=params['order'],
        author=params['author'],
        course_id=params['course_id'],
        verified=params['verified']
    )
    db_session.add(course)
    db_session.flush()
    return course.id
 

def course_get_by_id(course_id):
    return db_session.query(Course).filter(
        Course.id == course_id
    ).one()

    
def course_get_by_user(user_id):
    user_id = int(user_id)
    if user_id < 0:
        return []
    contextlevel = 50
    role = db_session.query(Role).filter(Role.shortname == 'editingteacher').one() 
    role_assignments = db_session.query(RoleAssignment).filter(
        RoleAssignment.userid == user_id, 
        RoleAssignment.roleid == role.id,
    ).all()
    courses_id = [item.context.instanceid for item in role_assignments \
        if item.context.contextlevel == contextlevel]
    courses = db_session.query(CourseRaw).filter(CourseRaw.id.in_(courses_id)).all()
    return courses
    

def course_get_users(course_id):
    course_id = int(course_id)
    contextlevel = 50
    role = db_session.query(Role).filter(Role.shortname == 'editingteacher').one() 
    contexts = db_session.query(Context).filter(
        Context.contextlevel == contextlevel,
        Context.instanceid == course_id,
    ).all()
    contexts_id = [item.id for item in contexts]
    role_assignments = db_session.query(RoleAssignment).filter(
        RoleAssignment.roleid == role.id,
        RoleAssignment.contextid.in_(contexts_id),
    ).all()
    users_id = [item.userid for item in role_assignments]
    users = db_session.query(User).filter(User.id.in_(users_id)).all()
    return users
    
    
def course_check_owner(course_id, user_id):
    if user_id < 0:
        return False
    contextlevel = 50
    role = db_session.query(Role).filter(Role.shortname == 'editingteacher').one() 
    role_assignments = db_session.query(RoleAssignment).filter(
        RoleAssignment.userid == user_id, 
        RoleAssignment.roleid == role.id,
    ).all()
    for role_assignment in role_assignments:
        if role_assignment.context.contextlevel == contextlevel\
                and role_assignment.context.instanceid == course_id:
            return True
    return False

    
def course_tree_check_owner(node_id, user_id):
    node_id = int(node_id)
    user_id = int(user_id)
    node = db_session.query(Course).filter(Course.id == node_id).one()
    cap = db_session.query(CourseTreeCap).filter(
        CourseTreeCap.node_id.in_(node.parents()),
        CourseTreeCap.user_id == user_id,
    ).all()
    acc_node = db_session.query(Course).filter(Course.id == cap[0].node_id).one() \
                if cap else None
    return acc_node

    
def course_tree_get_user_nodes(user_id):
    user_id = int(user_id)
    caps = db_session.query(CourseTreeCap).filter(
        CourseTreeCap.user_id == user_id,
    ).all()
    nodes = set()
    for cap in caps:
        node = db_session.query(Course).filter(
            Course.id == cap.node_id,
        ).one()
        nodes |= set(item for item in node.get_subtree_nodes() if not item.course_id)
    authored_nodes = db_session.query(Course).filter(
        Course.course_id == 0,
        Course.author == user_id,
    ).all()
    nodes |= set(authored_nodes)
    ordered_nodes = sorted(list(nodes), key=lambda course: course.id)
    return ordered_nodes

    
def course_tree_get_root_nodes(user_id):
    user_id = int(user_id)
    caps = db_session.query(CourseTreeCap).filter(
        CourseTreeCap.user_id == user_id,
    ).all()
    root_nodes = db_session.query(Course).filter(
        Course.id.in_([cap.node_id for cap in caps]),
    )
    return root_nodes

    
def GetNodeUsers(nodeId):
    node = db_session.query(Course).filter(Course.id == nodeId).one()
    parents = node.parents()
    users = []
    for parentNodeId in parents:
        caps = db_session.query(CourseTreeCap).filter(
            CourseTreeCap.node_id == parentNodeId,
        ).all()
        currentUsers = db_session.query(User).filter(
            User.id.in_([cap.user_id for cap in caps]),
        ).all()
        users += currentUsers
    users = list(set(users))
    return users
