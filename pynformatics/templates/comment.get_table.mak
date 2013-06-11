## -*- coding: utf-8 -*- 
<div class="bootstrap">
    % if len(comment) > 0:
    <table class="table table-striped table-condensed">
        <tbody>
        <%!
            from time import strptime, strftime
        %>
        % for elem in comment:
            <tr>
                <td>
                    % if elem["is_read"] == False:
                        <b>
                    % endif
                    <small>${strftime('%Y.%m.%d %H:%M', strptime(elem["date"],'%Y-%m-%d %H:%M:%S'))}</small>
                    % if elem["is_read"] == False:
                        </b>                    
                    % endif                    
                    <br/>
                    <a href="/moodle/mod/statements/view3.php?chapterid=${elem["problem_id"]}&run_id=${elem["contest_id"]}r${elem["run_id"]}">${elem["problem_name"]}</a>
                </td>
            </tr>
        % endfor        
    %else:
      Нет непрочитанных комментариев
    %endif
<!--            
                <td>74-40758</td>
                <td><a href="http://informatics.mccme.ru/moodle/mod/statements/view3.php?chapterid=104">104. Текст</a></td>
            </tr>
            <tr>
                <td>74-40758</td>
                <td><a href="http://informatics.mccme.ru/moodle/mod/statements/view3.php?chapterid=104">104. Текст</a></td>
            </tr>-->
        </tbody>
    </table>
</div>