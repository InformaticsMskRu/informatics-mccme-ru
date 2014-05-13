function send_error()
{
    show_alert("send_error");
}

function get_children(id) {
    obj = jQuery("#node" + id + "_content");
    jQuery.getJSON(get_url() + '/course/get/' + id + '/children', {}, function(res) {
        obj.html('');
        if (res.children.length) {
            jQuery('#node' + id + '_a').show();
        }
        else {
            jQuery('#node' + id + '_a').hide();
        }
        var style = "";
        if (id == 1) {
            style = "padding-left: 0px;";
        }
        for (var i = 0; i < res.children.length; ++i) {
            obj.append(jQuery("#child_template").render({
                id: id, 
                child_id: res.children[i].id, 
                child_problem_id: res.children[i].problem_id,
                make_contest_link: jQuery("#make_contest_statement_id").prop("value") != -1,
                style: style,
                title: res.children[i].name,
                course_id: res.children[i].course_id,
                course_name: res.children[i].course_name,
                verified: res.children[i].verified
            }));
            if (res.children[i].is_leaf) {
                jQuery('#node' + res.children[i].id + '_a').hide();
            }
            jQuery("#node" + res.children[i].id).attr("open_", '0');
            jQuery("#node" + res.children[i].id).attr("name_", res.children[i].name);
        }
    })
    .fail(send_error);
    return 1;
}

/* UPDATE */

function update_source(id) {
    jQuery.getJSON(get_url() + '/course/get/' + id, {}, function(res) {
        res = res.course;
        jQuery("#update_id").html(res.id);
        // jQuery("#update_author").html(res.author);
        jQuery("#update_id_h").prop("value", res.id);
        jQuery("#update_name").prop("value", res.name);
        jQuery("#update_parent").attr("cur_parent", res.parent_id);
        jQuery("#update_parent").prop("value", res.parent_id);
        jQuery("#update_course").prop("value", res.course_id);
        jQuery("#update_order").prop("value", res.order);
        jQuery("#update_verified").prop("value", res.verified == true ? 1 : 0);
        jQuery("#update_displayed").prop("value", res.displayed == true ? 1 : 0);
        jQuery("#update_window").show();
    })
    .fail(send_error);
}

function update_source_submit() {
    jQuery.post(get_url() + '/course/update/' + jQuery("#update_id_h").prop("value"), {
        'name': jQuery("#update_name").prop("value"),
        'parent_id': jQuery("#update_parent").prop("value"),
        'course_id': jQuery("#update_course").prop("value"),
        'order': jQuery("#update_order").prop("value"),
        'verified': jQuery("#update_verified").prop("value"),
        'displayed': jQuery("#update_displayed").prop("value"),
    }, function(res) {
        switch (res.result) {
            case 'ok': 
                get_children(get_parent(jQuery("#update_id_h").prop("value")));
                break;
            default:
                break;
        }
        
        show_alert(res.result, res.content);
        jQuery("#update_window").hide();
    })
    .fail(send_error);
}

function update_source_cancel() {
    jQuery("#update_window").hide();
}

/* ADD */

function add_son(id, course_id) {
    jQuery("#add_name").prop("value", '');
    jQuery("#add_parent").prop("value", id);
    jQuery("#add_problem").prop("value", '0');

    jQuery.getJSON(get_url() + '/course/get/' + id + '/children', {}, function(res) {
        jQuery("#add_order").html('');
        if (res.children.length == 0) {
            var option = [{
                "last": "",
                "cur": "",
                "order": "0:10000000",
                "selected": "0"
            }];        
            jQuery("#add_order").append(jQuery("#source_children_option_template").render(option));
        }
        else {
            var option = [{
                "last": "",
                "cur": res.children[0].name,
                "order": "0:" + res.children[0].order,
                "selected": "0"
            }];        
            jQuery("#add_order").append(jQuery("#source_children_option_template").render(option));
            for (var i = 1; i < res.children.length; ++i) {
                var option = [{
                    "last": res.children[i - 1].name,
                    "cur": res.children[i].name,
                    "order": res.children[i - 1].order + ":" + res.children[i].order,
                    "selected": "0"
                }];        
                jQuery("#add_order").append(jQuery("#source_children_option_template").render(option));
            }

            option = [{
                "last": res.children[res.children.length - 1].name,
                "cur": "",
                "order": res.children[res.children.length - 1].order 
                    + ":" + (res.children[res.children.length - 1].order + 10000000), 
                "selected": "1"
            }];    
            jQuery("#add_order").append(jQuery("#source_children_option_template").render(option));
        }
        if (course_id) {
            jQuery("#add_name").prop("value", "+++" + course_id);
        }
        jQuery("#add_window").show();
    })
    .fail(send_error);    
}

function add_source_submit() {
    jQuery.post(get_url() + '/course/add', {
        'name': jQuery("#add_name").prop("value"),
            'parent_id': jQuery("#add_parent").prop("value"),
        'order': jQuery("#add_order").prop("value"),
        'problem_id': '0'
    }, function(res) {
        show_alert(res.result, res.content);
        if (res.result == "error") {
            return;
        }
        parent_id = jQuery("#add_parent").prop("value");
        parent = jQuery("#node" + parent_id);
        if (parent) {
            if (parent.attr('open') == '0') {
                view(parent_id);
            }
            else {
                get_children(parent_id);
            }
        }
        jQuery("#add_window").hide();
    })
    .fail(send_error);
}

function add_source_cancel() {
    jQuery("#add_window").hide();
}

/* ERASE */

function erase_source(id) {
    resp = confirm("Вы уверены, что хотите удалить ("
        + id + ") " 
        + jQuery("#node" + id).attr("name_") 
        + "?");
    if (resp) {
        jQuery.post(get_url() + '/course/erase/' + id, {}, function(res){
            parent_id = get_parent(id);
            get_children(parent_id);
            show_alert(res.result, res.content);
        })
        .fail(send_error);
    }
}

function erase_source_all(id) {
    resp = confirm("Вы уверены, что хотите удалить все поддерево ("
        + id + ") " 
        + jQuery("#node" + id).attr("name_") 
        + "?");
    if (resp) {
        jQuery.post(get_url() + '/course/erase/' + id + '/all', {}, function(res) {
            parent_id = get_parent(id);
            get_children(parent_id);
            show_alert(res.result, res.content);
        })
        .fail(send_error);
    }
}

/* MAKE RELEATION*/

function make_relation(id) {
    jQuery("#problem_id").prop("value", id);
    jQuery.getJSON(get_url() + '/course/get/' + id, {}, function(res) {
        jQuery("#problem_problem").prop("value", res.problem_id);
        jQuery("#problem_window").show();
    })
    .fail(send_error);
}

function make_relation_submit() {
    jQuery.post(get_url() + '/course/update/' + jQuery("#problem_id").prop("value"), {
        'problem_id': jQuery("#problem_problem").prop("value")
    }, function(res) {
        get_children(get_parent(jQuery("#problem_id").prop("value")));
        jQuery("#problem_window").hide();    
        show_alert(res.result, res.content);
    })
    .fail(send_error);
}

function make_relation_cancel() {
    jQuery("#problem_window").hide()
}

/* MAKE CONTEST */

function make_contest(id) {
    resp = confirm("Добавить контест в ("
                + id + ") " 
                + jQuery("#node" + id).attr("name_") 
                + "?");
    if (resp) {
        var statement_id = jQuery("#make_contest_statement_id").prop("value");
        jQuery.post(get_url() + "/contest/add/" + statement_id + "/course/" + id, {}, function(res) {
            show_alert(res.result, res.content);
            get_children(id);
        })
        .fail(send_error);
    }
}

function make_contest_cancel() {
    jQuery("#course_tree_div").hide();
}
