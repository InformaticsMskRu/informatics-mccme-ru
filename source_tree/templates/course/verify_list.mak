<html>
<head>
    <title>Дистанционная подготовка: Управление темами</title>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
    <link rel="stylesheet" href="/py-source/css/course/verify_list/main.css" type="text/css" media="screen" charset="utf-8" />
</head>

<script id="status_item" type="text/x-jsrender">
    <div class="status_bar_text" style="background-color: {{>color}}">
        {{:msg}}
    </div>
</script>

<script id="div_list_table_content" type="text/x-jsrender">
    <table id="div_list_table">
        <tr id="div_list_table_tr_main">
            <td>${"Курс" if not categories else "Новая категория"}</td>
            <td>${"Категория в дереве" if not categories else "Родитель"}</td>
            <td>Пользователь</td>
            <td>Дата</td>
            <td>Действие</td>
        </tr>
        {{:content}}
    </table>
</script>

<script id="subject_item" type="text/x-jsrender">
    <tr style="background-color: {{if even}}#F0F0F0{{else}}#F8F8F8{{/if}};">
        <td>
            %if not categories:
                <a href="/course/view.php?id={{>course.id}}">({{>course.id}}) {{>course.name}}</a>
            %else:
                {{>node.name}} 
            %endif
        </td>
        <td>{{>parent.full_name}}</td>
        <td><a href="/user/view.php?id={{>user.id}}&course=1">{{>user.firstname}} {{>user.lastname}}</a></td>
        <td>{{>node.time}}</td>
        <td>
            %if not categories:
                <a class="a_list_table_verify" href="javascript:verify({{>node.id}}, '{{>parent.name}}', '{{>course.name}}', '0');">Подтвердить</a>
                /
                <a class="a_list_table_verify" href="javascript:verify_cancel({{>node.id}}, '{{>parent.name}}', '{{>course.name}}');">Отменить</a>
            %else:
                <a class="a_list_table_verify" href="javascript:verify({{>node.id}}, '{{>parent.name}}', '', '0');">Подтвердить</a>
                /
                <a class="a_list_table_verify" href="javascript:verify({{>node.id}}, '{{>parent.name}}', '', '1');">Подтв. и дать полный доступ</a>
                /
                <a class="a_list_table_verify" href="javascript:verify_cancel({{>node.id}}, '{{>parent.name}}', '');">Отменить</a>
            %endif
        </td>
    </tr>
</script>

<body>

    <div id="status_bar">

    </div>

    
    <div id="div_main">
        <div id="div_title">
            Элементы в дереве курсов, требующие подтверждения:
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

    function verify(node_id, node_name, course_name, full_access) {
        result = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/course/verify/" + node_id + "?full_access=" + full_access, 
            async: false
        }).responseText);
        status_clear();
        if (result.result == "ok") {
            result.content = "Категория <b><i>" + node_name + "</i></b> к курсу <b><i>" + course_name + "</i></b> подтверждена";
        }
        else if (result.result == "error") {
            result.content = "<b>Ошибка: </b>" + result.content;
        }
        status_add(result.result, result.content);
        refresh();
    }

    function verify_cancel(node_id, node_name, course_name) {
        result = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/course/verify/" + node_id + "/cancel", 
            async: false
        }).responseText);
        status_clear();
        if (result.result == "ok") {
            result.content = "Категория <b><i>" + node_name + "</i></b> к курсу <b><i>" + course_name + "</i></b> отклонена";
        }
        else if (result.result == "error") {
            result.content = "<b>Ошибка: </b>" + result.content;
        }
        status_add(result.result, result.content);
        refresh();
    }

    function refresh() {
        jQuery.getJSON("/py-source/course/get/all/to_verify", {
            'categories': ${categories},
        }, function(subject_list) {
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
