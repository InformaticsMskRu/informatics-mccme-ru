<html>
<head>
    
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <script src="/moodle/lib/jsMath/easy/load.js"></script>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
    <script type="text/javascript" src="/py-source/js/source/dir/contest.js"></script>
    <script type="text/javascript" src="/py-source/js/source/dir/func.js"></script>

    <link rel="stylesheet" href="/moodle/mod/statements/polygon.css" type="text/css" charset="utf-8" />
    <!--<link rel="stylesheet" href="/moodle/mod/statements/statements_theme.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="/moodle/theme/standard/styles.php" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="/moodle/theme/formal_white/styles.php" type="text/css" media="screen" charset="utf-8" />
    -->
    <link rel="stylesheet" href="/py-source/css/source_dir/main.css" type="text/css" media="screen" charset="utf-8" />
</head>

<script id="new-contest-problem-template" type="text/x-jsrender">
    <div class="new-contest-item">
        <div class="buttons">
            <div class="erase-button button" onClick="new_contest_erase_problem({{>ind}})" style="color: #D00;">X</div>
        </div>
        <div class="name">
            {{>name}}
        </div>
        <div class="id">
            (id={{>id}})
        </div>
        <div class="buttons">
            <!--<div class="erase-button button" onClick="new_contest_erase_problem({{>ind}})" style="color: #D00;">удалить</div>-->
            {{if up}}
                <div class="move-up-button button" onClick="new_contest_move_problem({{>ind}}, 'up')">вверх</div>
            {{/if}}
            {{if down}}
                <div class="move-down-button button" onClick="new_contest_move_problem({{>ind}}, 'down')">вниз</div>
            {{/if}}
        </div>

    </div>
</script>

<body>
    <%def name = "show_paging(block_num)">
        <div class="pages">
            Страница: 
            %if cur_page > 1:
                <a href="/py-source/source/dir/${source.id}-${subject.id}?page=${cur_page - 1}&cnt=${page_size}">&lt;&lt;</a>
            %endif
            %for page in page_list:
                %if page + 1 != cur_page:
                    <a href="/py-source/source/dir/${source.id}-${subject.id}?page=${page + 1}&cnt=${page_size}">${page + 1}</a>
                %else:
                    <b>${page + 1}</b>
                %endif
            %endfor
            %if cur_page != page_list[len(page_list) - 1] + 1:
                <a href="/py-source/source/dir/${source.id}-${subject.id}?page=${cur_page + 1}&cnt=${page_size}">&gt;&gt;</a>
            %endif
            Отображать по:
            <select id="select_page_cnt_${block_num}" onchange="reload_page(${block_num}, ${source.id}, ${subject.id})">
                %for cnt in [1, 2, 5, 10, 20, 50, 100]:
                    <option 
                        %if cnt == page_size:
                            selected
                        %endif
                        value="${cnt}">
                        
                        ${cnt}
                    </option>
                %endfor
            </select>
        </div>
    </%def>
    <%def name = "show_directory(source, source_path, source_children, other_source, other_source_children, side_align, title)"><!--
        --><div style="display: inline-block; width: 40%; vertical-align: top;">
            <div class="directory-window" 
                %if side_align == 'left':
                    style="margin: 0px 2px 0px 0px;"
                %elif side_align == 'right':
                    style="margin: 0px 0px 2px 0px;"
                %endif
            >
                <div class="path">
                    %for parent in source_path[:-1]:
                        <b><a href="/py-source/source/dir/${other_source.id}-${parent.id}">
                            %if parent.parent_id == 1:
                                ${title}
                            %else:
                                ${parent.name}
                            %endif
                        </a></b> 
                        -->
                    %endfor
                    %if source.parent_id == 1:
                        <b>${title}</b>
                    %else:
                        <b>${source.name}</b>
                    %endif
                </div>
                <div class="children">
                    %for child in source_children:
                        ${"&nbsp;" * 4 | n}<a href="/py-source/source/dir/${other_source.id}-${child.id}" class="child-link">${child.name}</a>(${sources_cnt[child]} задач)<br>
                    %endfor
                    %if len(source_children) < len(other_source_children):
                            %for i in range(len(source_children) - len(source_children)):
                            <a href="hidden" style="visibility: hidden"; class="child-link">hidden</a> <br>
                        %endfor
                    %endif
                </div>
    
            </div>
        </div><!--
    --></%def>
    <div id="div-center">
        <div id="filter" class="div-window">
            <!--
            <div class="title">
                <%
                    filter_title = subject.name + " & " + source.name \
                        if not source.is_root() and not subject.is_root() \
                        else source.name if not source.is_root() \
                        else subject.name if not subject.name \
                        else "Темы"
                %>
                <b>Фильтр</b> (${filter_title})
            </div>
            -->
            <div class="content">
                <div id="directories">
                    ${show_directory(subject, subject_path, subject_children, source, source_children, 'left', 'Темы')}<!--
                    --><div class="directory-split-window" style="display: inline-block; width: 20%;">
                        <div id="problems-cnt"><font color="#909090">---></font> 
                            <b>${problems_cnt} задач</b> 
                        <font color="#909090"><---</font></div>
                    </div><!--
                    -->${show_directory(source, source_path, source_children, subject, subject_children, 'right', 'Источники')}           

                </div>
            </div>
        </div>
        
        <div id="problem-list" class="div-window">
            <!--
            <div class="title">
                    <b>Задачи</b> (Всего: ${problems_cnt})
            </div>
            -->
            <div class="content">
                <div><div><div><div><div><div><div><div><div><div><div><div><div><div><div><div><div><div><div><div> <!-- FOR BAD HTML IN STATEMENTS -->    
                ${show_paging(0)}
                %for problem in problems:
                    <div class="problem-window">
                        <div class="title">
                            <div class="id">
                                #${problem.id}
                            </div>
                            <div class="link">
                                <a target="_top" href="http://informatics.mccme.ru/moodle/mod/statements/view.php?chapterid=${problem.id}"><b>${problem.name}</b></a>
                            </div>
                            &nbsp;&nbsp;
                
                            <div class="subjects">
                                <div>
                                %if problems_subjects[problem]:
                                    <b>Темы:</b>
                                    %for pr_subject in problems_subjects[problem]:
                                        [<a class="subject-link" href="/py-source/source/dir/${pr_subject.parent.id}">${pr_subject.parent.name}</a>]
                                    %endfor
                                %endif
                                </div>
                                <div>
                                    %if problems_sources[problem]:
                                        <div class="sources">
                                            <b>Источники:</b> 
                                            %for pr_source in problems_sources[problem]:
                                                [
                                                    %for parent_source in pr_source.get_path()[2:-1]:
                                                        <a href="/py-source/source/dir/${parent_source.id}">${parent_source.name}</a>, 
                                                    %endfor
                                                    ${pr_source.get_path()[-1:][0].name}
                                                ]
                                            %endfor
                                        </div>
                                    %endif

                                </div>
                            </div>
                            %if contest_add:
                                <div class="add-problem-button" onClick="new_contest_add_problem(${problem.id})">Добавить в контест</div>
                            %endif

                        </div>
                        <div class="content">
                            %if problem.show_limits:
                                <div class="problem-statement">
                                <div class="header">
                                    <div class="time-limit">
                                        <div class="property-title">ограничение по времени на тест</div>
                                        ${problem.timelimit} second;
                                    <!--</div>
                                    <div class="memory-limit">-->
                                        <div class="property-title">ограничение по памяти на тест</div>
                                        ${problem.memorylimit // 2**20} megabytes
                                    </div>
                                </div>
                            %endif
                            
                            %if problem.description: 
                                ${problem.description | n}
                            %endif
                            ${problem.content | n}
                            ${problem.sample_tests_html | n}
                            
                            %if problem.show_limits:
                                </div>
                            %endif

                        </div>
                    </div>
                %endfor
                <hr>
                ${show_paging(1)}
            </div>
        </div>
        
    </div>    

    <div id="new-contest" class="div-window">
        <div class="title">
            <div><b>Выбрано</b></div>:
            <div class="new-contest-title-button" onClick="new_contest_clean()">Отменить</div>|
            <div class="new-contest-title-button" onClick="new_contest_create()">Добавить в контест</div>
        </div>
        <div class="content">
                
        </div>
    </div>
</body>

<script>
    jQuery("#new-contest").hide();
    %if contest_add:
        show_new_contest_problems();
    %endif
</script>

</html>
