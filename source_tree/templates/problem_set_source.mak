<html>
<head>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
    <link rel="stylesheet" href="/py-source/css/problem/set_subject/main.css" type="text/css" media="screen" charset="utf-8" />
</head>

<script id="subject_option" type="text/x-jsrender">
    <option id="subject_option_{{>id}}" value="{{>id}}" subject_name="{{>name}}">
        {{:shft}}&nbsp;{{>name}}
    </option>
</script>

<script id="cur_subject_item" type="text/x-jsrender">
    <div class="div_subject_cur" id="div_subject_cur_{{>source.id}}">
        {{if 
        %if source_type == 'subject':
            access.edit
        %else:
            access.admin
        %endif
        }}
        <span class="div_subject_cur_button">
            <a class="a_subject_cur_button" href="javascript:erase({{>source.id}}, '{{>parent.name}}');">удалить</a>
        </span>
        {{/if}}
        <span class="div_subject_cur_title">
        %if source_type == 'subject':
            {{:parent.name}}
        %else:
            {{:path}}
        %endif
        </span>
    </div>
</script>

<script id="cur_to_verify_subject_item" type="text/x-jsrender">
    <div class="div_subject_cur" id="div_subject_cur_{{>source.id}}" style="color: #A0A0A0;">
        {{if 
        %if source_type == 'subject':
            access.edit
        %else:
            access.admin
        %endif
        }}
        <span class="div_subject_cur_button">
            <a class="a_subject_cur_button" href="javascript:erase({{>source.id}}, '{{>parent.name}}');">удалить</a>
        </span>
        <span class="div_subject_cur_button">
            <a class="a_subject_cur_button" href="javascript:verify({{>source.id}}, '{{>parent.name}}');">добавить</a>
        </span>
        {{/if}}
        <span class="div_subject_cur_title">
        {{:parent.name}}
        </span>
    </div>
</script>


<script id="status_item" type="text/x-jsrender">
    <div class="status_bar_text" style="background-color: {{>color}}">
        {{:msg}}
    </div>
</script>

<body>
    <!-- <div id="title_frame" class="div_window" style="width: 806px;">
        <div class="div_window_title">Задача:</div>
        <div class="div_window_content">
            <em> (${problem.id}) ${problem.name}</em>
        </div>
    </div> -->

    <div id="status_bar" style="font-family: \"verdana\"; font-size: 8px;">

    </div>

    <div>
        <div id="div_cur_frame" class="div_window" 
            %if source_type == 'subject':
                style='width: 400px;'
            %else:
                style='width: 800px;'
            %endif
            >
            <div class="div_window_title">
                %if source_type == 'subject':
                    Текущие темы:
                %else:
                    Текущие источники:
                %endif
            </div>
            <div id="div_cur" class="div_window_content">

            </div>
        </div>
        %if source_type == 'subject':
        <div id="div_cur_to_verify_frame" class="div_window" style="width: 400px;">
            <div class="div_window_title">Предложенные темы:</div>
            <div id="div_cur_to_verify" class="div_window_content">

            </div>
        </div>
        %endif
    </div>

    <div id="main_frame">
        <div id="div_add_frame" class="div_window">
            <div class="div_window_title">
            %if source_type == 'subject':
                Добавить темы:
            %else:
                Добавить источники:
            %endif
            </div>
            <!-- <br> -->
            <div id="div_add" class="div_window_content">
                
            </div>

            <div id="submit_frame">
                <input type="button" value="Добавить" onClick="save_changes();">
            </div>
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
        }
        var status_render = {
            color: color_dict[type],
            msg: msg
        };
        jQuery("#status_bar").append(jQuery("#status_item").render(status_render));
    }

    function add_select(id, subject_list) {
        var result = '';
        result += '<div><select id="subject_select_' + id + '" style="width: 300px;">';
        %if source_type == 'subject':
            result += '<option value="-1">Выберите тему</option>';
        %else:
            result += '<option value="-1">Выберите источник</option>';
        %endif
        var parent_stack = new Array();
        var shft_cnt = 0;
        for (var i = 0; i < subject_list.length; ++i) {
            if (i) {
                if (!parent_stack.length || subject_list[i].parent_id != parent_stack[parent_stack.length - 1]) {
                    if (subject_list[i - 1].id == subject_list[i].parent_id) {
                        parent_stack.push(subject_list[i - 1].id);
                        ++shft_cnt;
                    }
                    else {
                        while (parent_stack.length && subject_list[i].parent_id != parent_stack[parent_stack.length - 1]) {
                            
                            parent_stack.pop();
                            --shft_cnt;
                        }
                    }
                }
            }
            var shft = '';
            for (var j = 0; j < shft_cnt; ++j) {
                for (var jj = 0; jj < 4; ++jj) {
                    shft += '&nbsp;';
                }
            }
            var option_render = {
                id: subject_list[i].id,
                shft: shft,
                name: subject_list[i].name
            };
            result += jQuery("#subject_option").render(option_render);
        }
        result += '</select></div>';
        return result;
    }

    function refresh() {
        var access = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/access",
            async: false
        }).responseText);

        var subject_all = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/source/get/all/${source_type}",
            async: false
        }).responseText);

        var result = '';
        for (var select_id = 0; select_id < ${select_cnt}/*subject_cur.length + subject_cur_to_verify.length + 1*/; ++select_id) {
            result += add_select(select_id, subject_all);
        }
        jQuery("#div_add").html(result);

        jQuery.getJSON("/py-source/problem/get/${problem.id}/${source_type}", {}, function(subject_list) {
            for (var i = 0; i < subject_list.length; ++i) {
                subject_list[i].access = access;
            }
            if (subject_list.length) {
                jQuery("#div_cur").html(jQuery("#cur_subject_item").render(subject_list));
            }
            else {
                jQuery("#div_cur").html("<i>Нет</i>");
            }
        });

        %if source_type == 'subject':
            jQuery.getJSON("/py-source/problem/get/${problem.id}/subject/to_verify", {}, function(subject_list) {
                for (var i = 0; i < subject_list.length; ++i) {
                    subject_list[i].access = access;
                }
                if (subject_list.length) {
                    jQuery("#div_cur_to_verify").html(jQuery("#cur_to_verify_subject_item").render(subject_list));
                }
                else {
                    jQuery("#div_cur_to_verify").html("<i>Нет</i>");
                }
            });
        %endif
    }    

    function save_changes() {
        status_clear();
        for (var select_id = 0; select_id < ${select_cnt}; ++select_id) {
            var subject_id = jQuery("#subject_select_" + select_id).prop('value');
            if (subject_id == -1) {
                continue;
            }

            var result = JSON.parse(jQuery.ajax({
                type: "GET",
                url: "/py-source/problem/add/${problem.id}/source/" + subject_id,
                async: false
            }).responseText);
            var subject_name = jQuery("#subject_option_" + subject_id).attr('subject_name');
            if (result.result == 'ok') {
                var suff = "будет добавлена, после одобрения редактором";
                if (result.verified) {
                    %if source_type == 'subject':
                        suff = "добавлена";
                    %else:
                        suff = "добавлен";
                    %endif
                }
                %if source_type == 'subject':
                    result.content = "Тема <b><i>" + subject_name + "</i></b> " + suff;
                %else:
                    result.content = "Источник <b><i>" + subject_name + "</i></b> " + suff;
                %endif
            } 
            else if (result.result == 'error') {
                if (result.content == 'Already exists') {
                    %if source_type == 'subject':
                        result.content = 'Эта тема уже указана';
                    %else:
                        result.content = 'Этот источник уже указан';
                    %endif
                }
                result.content = "Ошибка при добавлении <b><i>" + subject_name + "</i></b>: " + result.content;
            }
            status_add(result.result, result.content);
        }
        
        refresh();
    }

    function erase(subject_id, subject_name) {
        status_clear();
        // var subject_name = jQuery("#subject_option_" + subject_id).attr('subject_name');
        var resp = confirm("Вы уверены, что хотите удалить \"" + subject_name + "\"?");
        if (resp) {
            var result = JSON.parse(jQuery.ajax({
                type: "GET",
                url: "/py-source/source/erase/" + subject_id,
                async: false
            }).responseText);        
            if (result.result == 'ok') {
                %if source_type == 'subject':
                    result.content = "Тема <b><i>" + subject_name + "</i></b> удалена";
                %else:
                    result.content = "Источник <b><i>" + subject_name + "</i></b> удален";
                %endif
            } 
            else if (result.result == 'error') {
                result.content = "Ошибка при удалении <b><i>" + subject_name + "</i></b>: " + result.content;
            }
            status_add(result.result, result.content);
        }
        refresh();
    }

    function verify(subject_id, subject_name) {
        status_clear();
        // var subject_name = jQuery("#subject_option_" + subject_id).attr('subject_name');
        var resp = confirm("Вы уверены, что хотите подтвердить тему \"" + subject_name + "\"?");
        if (resp) {
            var result = JSON.parse(jQuery.ajax({
                type: "GET",
                url: "/py-source/source/verify/" + subject_id,
                async: false
            }).responseText);        
            if (result.result == 'ok') {
                result.content = "Тема <b><i>" + subject_name + "</i></b> подтверждена";
            } 
            else if (result.result == 'error') {
                result.content = "Ошибка при подтверждении темы <b><i>" + subject_name + "</i></b>: " + result.content;
            }
            status_add(result.result, result.content);
        }
        refresh();
    }

    refresh();

</script>

</html>
