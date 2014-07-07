from pynformatics.view.utils import RequestCheckUserCapability, RequestGetUserId


def check_capability(request, user_type):
    if not RequestCheckUserCapability(request, 'moodle/source_tree:' + user_type):
        raise Exception('Access denied')


def check_capability_ex(request, user_type):
    return RequestCheckUserCapability(request, 'moodle/source_tree:' + user_type)


def check_capability_course(request, user_type):
    if user_type == "teacher":
        return
    sec_key = request.params['sec_key'] if 'sec_key' in request.params else ''
    if sec_key != request.registry.settings['source_tree.course.sec_key'] \
            and not RequestCheckUserCapability(request, 'moodle/course_tree:' + user_type):
        raise Exception('Access denied')


def check_capability_ex_course(request, user_type):
    sec_key = request.params['sec_key'] if 'sec_key' in request.params else ''
    return sec_key == request.registry.settings['source_tree.course.sec_key'] \
        or RequestCheckUserCapability(request, 'moodle/course_tree:' + user_type)


