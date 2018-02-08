<html>
<head>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
    <script type="text/javascript" src="/py-source/js/bootstrap.js"></script>
    <link rel="stylesheet" href="/py-source/css/bootstrap.css" type="text/css" media="screen" charset="utf-8" />

    <script type="text/javascript" src="/py-source/js/course/adm/view_func.js"></script>
    <script type="text/javascript" src="/py-source/js/course/adm/adm_func.js"></script>
    <script type="text/javascript" src="/py-source/js/course/adm/event.js"></script>
    <link rel="stylesheet" href="/py-source/css/course/adm/main.css" type="text/css" media="screen" charset="utf-8" />
</head>
<script id="source_option_template" type="text/x-jsrender">
    {{if selected == "1"}}
        <option selected value="{{>id}}">({{>id}}){{>name}}</option>
    {{else}}
        <option value="{{>id}}">({{>id}}){{>name}}</option>
    {{/if}}
    
</script>

<script id="source_children_option_template" type="text/x-jsrender">
    {{if selected == "1"}}
        <option selected value="{{>order}}">{{>last}} __ {{>cur}}</option>
    {{else}}
        <option value="{{>order}}">{{>last}} __ {{>cur}}</option>
    {{/if}}
    
</script>

<script id="problem_option_template" type="text/x-jsrender">
    {{if selected == "1"}}
        <option selected value="{{>id}}">({{>id}}){{>name}}</option>
    {{else}}
        <option value="{{>id}}">({{>id}}){{>name}}</option>
    {{/if}}
    
</script>

<script id="child_template" type="text/x-jsrender">
    <div class="source_node" parent_id="{{>id}}" id="node{{>child_id}}" style="{{>style}}">
        <div class="source_node_head" node_id="{{>child_id}}" id="node{{>child_id}}_head">
            <div class="source_node_head_title">    
                <div class="btn-group">
                    <a class="btn btn-small" href="javascript:view({{>child_id}})" id="node{{>child_id}}_a">
                        <i class="icon-chevron-down"></i>
                    </a>
                    <a id="dropdown_btn_{{>child_id}}" class="btn btn-small dropdown-toggle" 
                        data-toggle="dropdown" 
                        href="#" 
                        onClick="jQuery('#dropdown_btn_{{>child_id}}').goTo('#source_tree_div_body')">
                        <i class="icon-wrench"></i>
                        <!-- <span class="caret"></span> -->
                    </a>
                    <ul class="dropdown-menu" style="font-size: 10px;">
                        %if course:
                            <li class="node_li">
                                <a tabindex="-1" href="javascript:add_son({{>child_id}}, ${course.id})">Прикрепить курс(${course.id}) к этому узлу
                                </a>
                            </li>
                        %endif
                        <li class="node_li">
                            <a tabindex="-1" href="javascript:add_son({{>child_id}})">Добавить дочерние курсы
                            </a>
                        </li>
                        <li class="node_li">
                            <a tabindex="-1" href="javascript:update_source({{>child_id}})">Редактировать</a>
                        </li>
                        <li class="node_li">
                            <a tabindex="-1" href="javascript:erase_source_all({{>child_id}})">
                                <font color="red">Удалить</font>
                            </a>
                        </li>
                    </ul>
                </div>
                <!--<div class="source_node_head_title_id">({{>child_id}})</div>-->
                {{if course_id}}
                    <a class="source_node_head_title_problem_id" href="http://informatics.mccme.ru/moodle/course/view.php?id={{>course_id}}">(курс: {{>course_name}})</a>
                {{/if}}
                {{if verified}}
                    <b>{{>title}}</b>
                {{else}}
                    <b style="color: #B0B0B0;"><i>(не подтв.)</i>{{>title}}</b>
                {{/if}}
            </div>
            <!-- <hr>
            <div class="source_node_head_buttons">
            </div>
             -->
        </div>
        <div class="source_node_content" id="node{{>child_id}}_content">
        </div>
    </div>
</script>    
    


<body>
    <div id="source_tree_status">

    </div>
    <div id="source_tree_div_body" style="position: absolute; left: 0px; right: 0px;
                bottom: 0px; top: 20px; overflow: scroll;">
        <div id="main_div">
            <!-- <div id="status_bar">
            
            </div> -->
            %if course:
                <div style="margin-left: 30px;">
                    <a href="/moodle/course/view.php?id=${course.id}">Назад к курсу <b>${course.full_name}</b></a>
                </div>
            %endif

            <div class="source_node" id="node1">
                <div class="source_node_head" node_id="1" id="node1_head" style="height: 20px">
                    <div class="source_node_head_buttons">
                        <div class="btn btn-mini" onClick="add_son(1)">
                            Добавить корневой курс</div>
                    </div>
                </div>
                <div class="source_node_content" id="node1_content">
                </div>
            </div>


            <div class="popup_window" id="add_window">
                <div class="popup_window_title">
                    Добавить курсы (по одному в строке)
                </div>
                <div id="add_window_edit_block">
                    <div class="popup_window_edit_field" style="height: 110px;">
                        <div class="popup_window_edit_label">Имя:</div>
                        <textarea class="popup_window_edit" id="add_name" autofocus="1" rows="5"></textarea><br>
                    </div>
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Родитель:</div>
                        <input class="popup_window_edit" type="edit" id="add_parent">
                        <!-- <select class="popup_window_edit" id="add_parent" disabled="1">

                        </select> -->
                        <br>
                    </div>
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Порядок:</div>
                        <!-- <input class="popup_window_edit" type="edit" id="add_order"> -->
                        <select class="popup_window_edit" id="add_order">

                        </select>
                        <br>
                    </div>
                </div>

                <div id="add_window_button_block">
                    <input type="button" value="OK" onClick="add_source_submit()">
                    <input type="button" value="Отмена" onClick="add_source_cancel()">
                </div>
            </div>

            <div class="popup_window" id="update_window">
                <div class="popup_window_title">
                    Изменить узел
                </div>
                <div id="update_window_edit_block">
                    <input id="update_id_h" type="hidden">
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">ID:</div>
                        <div class="popup_window_edit" id="update_id"></div><br>
                    </div>
                    <!-- <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Последнее изменение:</div>
                        <div class="popup_window_edit" id="update_author"></div><br>
                    </div> -->
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Имя:</div>
                        <input class="popup_window_edit" type="edit" id="update_name"><br>
                    </div>
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Родитель:</div>
                        <input class="popup_window_edit" type="edit" id="update_parent">
                        <!-- <select class="popup_window_edit" id="update_parent" disabled="1">

                        </select> -->
                        <br>
                    </div>
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Курс:</div>
                        <input class="popup_window_edit" type="edit" id="update_course">
                        <br>
                    </div>
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Порядок:</div>
                        <input class="popup_window_edit" type="edit" id="update_order">
                        <br>
                    </div>
                    
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_label">Подтв.:</div>
                        <input class="popup_window_edit" type="edit" id="update_verified">
                        <br>
                    </div>

                    <div class="popup_window_edit_field" style="margin-top: 10px;">
                        <div class="popup_window_edit_label">Всегда отобр.:</div>
                        <input class="popup_window_edit" type="edit" id="update_displayed">
                        <br>
                    </div>
                </div>

                <div id="update_window_button_block">
                    <input type="button" value="OK" onClick="update_source_submit()">
                    <input type="button" value="Отмена" onClick="update_source_cancel()">
                </div>
            </div>

            <div class="popup_window" id="problem_window">
                <div class="popup_window_title">
                    Привязать задачу
                </div>

                <div id="problem_window_edit_block">
                    <div class="popup_window_edit_field">
                        <div class="popup_window_edit_field">
                            <div class="popup_window_edit_label">ID:</div>
                            <input class="popup_window_edit" id="problem_id" type="edit" disabled="1"><br>
                        </div>
                        <div class="popup_window_edit_label">Задача:</div>
                        <!-- <select class="popup_window_edit" id="problem_problem">

                        </select> -->
                        <input class="popup_window_edit" id="problem_problem" type="edit">
                        <br>
                    </div>
                </div>

                <div id="problem_window_button_block">
                    <input type="button" value="OK" onClick="make_relation_submit()">
                    <input type="button" value="Отмена" onClick="make_relation_cancel()">
                </div>
            </div>

            <div id="alert_window" style="display: none;">
                <!-- ALERT WINDOW -->
                
                <!-- <div id="alert_bs" class="alert" style="width: 300px;">
                    <button type="button" class="close" onClick="hide_alert();">&times;</button>
                    Операция выполнена успешно.
                </div> -->
            </div>
        </div>
        <input type="hidden" id="make_contest_current_url" value="/py-source">
        <input type="hidden" id="make_contest_statement_id" value="">

    </div>
</body>
<script type="text/javascript">
    get_children(1);
</script>
</html>
