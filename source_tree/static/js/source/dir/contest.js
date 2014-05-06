function get_json(url)
{
    return JSON.parse(jQuery.ajax({
        type: "GET",
        url: "/py-source/" + url,
        async: false
    }).responseText);
}


function show_new_contest_problems()
{
    jQuery.getJSON("/py-source/source/dir/contest/get_problems", {}, function(res) {
        if (res.result == "ok") {
            for (var i = 0; i < res.problems.length; ++i) {
                res.problems[i].ind = i;
                res.problems[i].up = i > 0;
                res.problems[i].down = i < res.problems.length - 1;
            }
            jQuery("#new-contest > .content").html(jQuery("#new-contest-problem-template").render(res.problems));
            if (res.problems.length) {
                jQuery("#new-contest").show();
            }
            else {
                jQuery("#new-contest").hide();
            }
        }
        else {
            jQuery("#new-contest").hide();
        }
    });
}


function new_contest_erase_problem(ind)
{
    jQuery.getJSON("/py-source/source/dir/contest/erase_problem/" + ind, {}, function(res) {
        show_new_contest_problems();
    });
}


function new_contest_move_problem(ind, move_type)
{
    jQuery.getJSON("/py-source/source/dir/contest/move_problem/" + ind + "/" + move_type, {}, function(res) {
        show_new_contest_problems();
    });
}


function new_contest_add_problem(id)
{
    jQuery.getJSON("/py-source/source/dir/contest/add_problem/" + id, {}, function(res) {
        show_new_contest_problems();
    });
}


function new_contest_clean()
{
    jQuery.getJSON("/py-source/source/dir/contest/clean", {}, function(res) {
        jQuery("#new-contest").hide();
        jQuery(".add-problem-button").hide();
    });
}


function new_contest_create()
{
    document.location.href = "/py-source/source/dir/contest/create";
}
