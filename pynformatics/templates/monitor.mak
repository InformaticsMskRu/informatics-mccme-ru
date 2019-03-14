<%
    TABLE_HEAD_PREFIX = ['N', 'Name', 'Sum']
    PREFIX_LEN = len(TABLE_HEAD_PREFIX)
    PROBLEM_LINK_PREFIX = 'href=http://informatics.mccme.ru/' \
                          'mod/statements/view3.php?chapterid='
%>


<table cellspacing="0" cellpadding="2" border="1">
    ${makeheadrow(problems)}

    % for i, c in enumerate(competitors, start=1):
        <%
            competitor_result = [i, c.full_name, c.sum()]
            competitor_result.extend(c.full_stat_by_prob(p) for p in problems)
        %>
        ${makerow(competitor_result)}
    % endfor

    ${makeheadrow(problems)}
</table>
<br>
<table cellspacing="0" cellpadding="2" border="1">
    % for row in contests_table:
        ${make_contest_row(row)}
    % endfor
</table>


<%def name="makerow(competitor_result)">
    <tr>
        % for pre in competitor_result[:PREFIX_LEN]:
            <td>${pre}</td>
            \
        % endfor
        % for stat, color in competitor_result[PREFIX_LEN:]:
            <%
                html_color = color.html_color
            %>
            <td bgcolor=${html_color}>
            ${stat}
            </td>
            \
        % endfor
    </tr>
</%def>

<%def name="makeheadrow(problems)">
    <tr>
        % for pre in TABLE_HEAD_PREFIX:
            <td>${pre}</td>
            \
        % endfor
        % for problem in problems:
        <%
            problem_id = problem.id
            problem_tag = problem.tag
        %>
            <td>
                <a ${PROBLEM_LINK_PREFIX}${problem_id}>${problem_tag}</a>
            </td>
            \
        % endfor
    </tr>
</%def>

<%def name="make_contest_row(row)">
    <tr>
    % for name in row:
        <td>${name}</td>\
    % endfor
    </tr>
</%def>
