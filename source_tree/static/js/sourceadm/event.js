$(document).ready(function() {
    $(document).keyup(function() {
        if (event.keyCode == 27) {
            update_source_cancel();
            add_source_cancel();
            make_relation_cancel();
        }
    });

    $("#update_window").keyup(function(event) {
        if(event.keyCode == 13) {
            update_source_submit();
        }
    });

    /*$("#add_window").keyup(function(event) {
        if(event.keyCode == 13) {
            add_source_submit();
        }
    });
    */

    $("#problem_window").keyup(function(event) {
        if(event.keyCode == 13) {
            make_relation_submit();
        }
    });
});
