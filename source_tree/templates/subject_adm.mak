<html>
<head>
    <title>Дистанционная подготовка: Управление темами</title>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
    <link rel="stylesheet" href="/py-source/css/subjectadm/main.css" type="text/css" media="screen" charset="utf-8" />
</head>

<script id="status_item" type="text/x-jsrender">
    <div class="status_bar_text" style="background-color: {{>color}}">
        {{:msg}}
    </div>
</script>

<script id="div_list_table_content" type="text/x-jsrender">
    <table id="div_list_table">
        <tr id="div_list_table_tr_main">
            <td>Задача</td>
            <td>Тема</td>
            <td>Пользователь</td>
            <td>Дата</td>
            <td>Действие</td>
        </tr>
        {{:content}}
    </table>
</script>

<script id="subject_item" type="text/x-jsrender">
    <tr style="background-color: {{if even}}#F0F0F0{{else}}#FFFFE0{{/if}};">
        <td><a href="http://informatics.mccme.ru/moodle/mod/statements/view3.php?chapterid={{>problem.id}}">({{>problem.id}}) {{>problem.name}}</a></td>
        <td>{{>parent.name}}</td>
        <td><a href="http://informatics.mccme.ru/moodle/user/view.php?id={{>user.id}}&course=1">{{>user.firstname}} {{>user.lastname}}</a></td>
        <td>{{>source.time}}</td>
        <td><a class="a_list_table_verify" href="javascript:verify({{>source.id}}, '{{>parent.name}}', '{{>problem.name}}');">Подтвердить</a>
        /
        <a class="a_list_table_verify" href="javascript:verify_cancel({{>source.id}}, '{{>parent.name}}', '{{>problem.name}}');">Отменить</a></td>
    </tr>
</script>

<body>
    <a href="/moodle">На главную</a>

    <div id="status_bar">

    </div>

    
    <div id="div_main">
        <div id="div_title">
            Темы, требующие подтверждения:
        </div>
        <div id="div_list">

        </div>
    </div>
</body>

<script>
    function status_clear() {
        jQuery("#status_bar").html('');
    }

    function status_add(type, msg) {
        var color_dict = {
            'none': '#C0C0C0',
            'ok': '#C0FFC0',
            'error': '#FFC0C0'
        };
        var title_dict = {
            'none': '',
            'ok': '',
            'error': 'Ошибка'
        };

        jQuery("#status_bar").append(jQuery("#status_item").render({
            color: color_dict[type],
            msg: msg
        }));
    }

    function verify(source_id, source_name, problem_name) {
        result = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/source/verify/" + source_id, 
            async: false
        }).responseText);
        status_clear();
        if (result.result == "ok") {
            result.content = "Тема <b><i>" + source_name + "</i></b> к задаче <b><i>" + problem_name + "</i></b> подтверждена";
        }
        else if (result.result == "error") {
            result.content = "<b>Ошибка: </b>" + result.content;
        }
        status_add(result.result, result.content);
        refresh();
    }

    function verify_cancel(source_id, source_name, problem_name) {
        result = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/source/verify/" + source_id + "/cancel", 
            async: false
        }).responseText);
        status_clear();
        if (result.result == "ok") {
            result.content = "Тема <b><i>" + source_name + "</i></b> к задаче <b><i>" + problem_name + "</i></b> отклонена";
        }
        else if (result.result == "error") {
            result.content = "<b>Ошибка: </b>" + result.content;
        }
        status_add(result.result, result.content);
        refresh();
    }

    function refresh() {
        jQuery.getJSON("/py-source/source/get/all/subject/to_verify", {}, function(subject_list) {
            for (var i = 0; i < subject_list.length; ++i) {
                subject_list[i].even = i % 2;
            }
            content = jQuery("#subject_item").render(subject_list);
            jQuery("#div_list").html(jQuery("#div_list_table_content").render({
                content: content
            }));
        });
    }

    refresh();
</script>
</html>