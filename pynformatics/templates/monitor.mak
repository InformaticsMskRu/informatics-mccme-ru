<%
    TABLE_HEAD_PREFIX = ['N', 'Name', 'Sum']
    PREFIX_LEN = len(TABLE_HEAD_PREFIX)
    PROBLEM_LINK_PREFIX = 'href=http://informatics.mccme.ru/mod/statements/view3.php?chapterid='
%>


<!DOCTYPE html>
<html lang="{{ '${request.locale_name}' }}">
<head>
    <meta charset="utf-8">
    <link rel="shortcut icon"
          href="${request.static_url('monitor_table:static/monitor-16x16.png')}">
    <title>Monitor table</title>

    <style>
        table {
            border: 1px solid #CCC;
            font-family: Verdana, serif;
            font-size: 11pt;
        }
    </style>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
</head>
<body>
<table cellspacing="0" cellpadding="2" border="1">
    ${makeheadrow(problems)}

    % for i, c in enumerate(competitors, start=1):
        <%
            competitor_result = [i, c.full_name, c.sum()]
            competitor_result.extend(c.full_stat_by_prob(p.name) for p in problems)
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
</body>
</html>

<%def name="makerow(competitor_result)">
    <tr>
        % for pre in competitor_result[:PREFIX_LEN]:
            <td>${pre}</td>
            \
        % endfor
        % for stat, issolved in competitor_result[PREFIX_LEN:]:
            <td
                % if issolved:
                    bgcolor="#e1f2e1"
                % endif
            >
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
