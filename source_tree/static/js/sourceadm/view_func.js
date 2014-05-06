(function($) {
    $.fn.goTo = function(main_window) {
        $(main_window).animate({
            scrollTop: $(this).offset().top - $(main_window).offset().top 
                + $(main_window).scrollTop() - 10,
            scrollLeft: $(this).offset().left - $(main_window).offset().left
                + $(main_window).scrollLeft() - 10
        }, 'fast');
        return this;
    }
})(jQuery);

function show_alert(alert_type, ext_info)
{
    var dict_content = {
        "ok": "Операция успешно выполнена.",
        "error": "<strong>Ошибка: </strong>" + ext_info, 
        // "auth_error": "Недостаточно доступа для выполнения операции.",
        // "server_error": "Ошибка сервера.", 
        "send_error": "Сервер недоступен.",
        "info": ext_info,
        "warning": "<strong>Предупреждение: </strong>" + ext_info
    }
    var dict_type = {
        "ok": "success",
        "error": "error",
        // "auth_error": "error",
        // "server_error": "error",
        "send_error": "error",
        "info": "info",
        "warning": "block"
    }
    
    // jQuery("#alert_window").html('123');
    jQuery("#source_tree_status").html(
        '<div id="status_bar_text"'
        + ' class="alert-' 
        + dict_type[alert_type]
        + '">'
        + dict_content[alert_type]
        + '</div>'
    );
    //jQuery("#alert_window").show();

}

function hide_alert()
{
    jQuery("#alert_window").html("");
    jQuery("#alert_window").hide();
}

function get_parent(id) {
    return document.getElementById("node" + id).getAttribute('parent_id');
}

function view(id) {
    cur = jQuery("#node" + id); 
    link = jQuery("#node" + id + '_a');
    content = jQuery("#node" + id + '_content');
    if (jQuery("#node" + id).attr("open_") != '1') {
        if (get_children(id)) {
            jQuery("#node" + id).attr("open_", '1');
            link.html('<i class="icon-chevron-up"></i>');
            jQuery("#node" + id + "_head").goTo("#source_tree_div_body");
        }
    }
    else {
        jQuery("#node" + id).attr("open_", '0');
        link.html('<i class="icon-chevron-down"></i>');
        content.html('');
        if (id != 1) {
            parent_id = get_parent(id);
            jQuery("#node" + parent_id + "_head").goTo("#source_tree_div_body");
        }
    }
}

function get_url() {
    return jQuery("#make_contest_current_url").prop("value");
}
