<html>
<head>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
</head>

<script id="subject_option" type="text/x-jsrender">
    <option id="subject_option_{{>id}}" value="{{>id}}" subject_name="{{>name}}">
        {{:shft}}&nbsp;{{>name}}
    </option>
</script>

<script id="status_item" type="text/x-jsrender">
    <div class="status_bar_text" style="background-color: {{>color}}">
        {{:msg}}
    </div>
</script>

<body>

    <div id="status_bar">

    </div>

    <div id="main_frame">
            <div id="div_add" class="div_window_content">
                
            </div>
                <input type="button" value="Добавить" onClick="save_changes();">
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

    function add_select(id, source_list) {
        var result = '';
        result += '<div><select id="subject_select_' + id + '" style="width: 300px;">';
        result += '<option value="-1">Выберите источник</option>';
        var parent_stack = new Array();
        var shft_cnt = 0;
        for (var i = 0; i < source_list.length; ++i) {
            if (i) {
                if (!parent_stack.length || source_list[i].parent_id != parent_stack[parent_stack.length - 1]) {
                    if (source_list[i - 1].id == source_list[i].parent_id) {
                        parent_stack.push(source_list[i - 1].id);
                        ++shft_cnt;
                    }
                    else {
                        while (parent_stack.length && source_list[i].parent_id != parent_stack[parent_stack.length - 1]) {
                            
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
                id: source_list[i].id,
                shft: shft,
                name: source_list[i].name
            };
            result += jQuery("#subject_option").render(option_render);
        }
        result += '</select></div>';
        return result;
    }

    function refresh() {
        var subject_all = JSON.parse(jQuery.ajax({
            type: "GET",
            url: "/py-source/source/get/all/source",
            async: false
        }).responseText);

        jQuery("#div_add").html(add_select(0, subject_all));
    }    

    function save_changes() {
        status_clear();
        for (var select_id = 0; select_id < 1; ++select_id) {
            var subject_id = jQuery("#subject_select_" + select_id).prop('value');
            if (subject_id == -1) {
                continue;
            }

            var result = JSON.parse(jQuery.ajax({
                type: "GET",
                url: "/py-source/contest/add/${contest_id}/source/" + subject_id,
                async: false
            }).responseText);
            var subject_name = jQuery("#subject_option_" + subject_id).attr('subject_name');
            if (result.result == 'ok') {
                result.content = "Источник <b><i>" + subject_name + "</i></b> добавлен";
            } 
            else if (result.result == 'error') {
                result.content = "Ошибка при добавлении добавлении источника <b><i>" + subject_name + "</i></b>: " + result.content;
            }
            status_add(result.result, result.content);
        }
        
        refresh();
    }

    refresh();

</script>

</html>