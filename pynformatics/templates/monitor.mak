<%
    TABLE_HEAD_PREFIX = ['N', 'Name', 'Sum']
    PREFIX_LEN = len(TABLE_HEAD_PREFIX)
    PROBLEM_LINK_PREFIX = '/mod/statements/view3.php?chapterid='
    USER_SUBMITS_PREFIX = '/submits/view.php?user_id='
%>

<p><% 
   if view_settings:
      show_login = view_settings["show_login"]
      if show_login:
          TABLE_HEAD_PREFIX.append("login")
      show_email = view_settings["show_email"]
      if show_email:
          TABLE_HEAD_PREFIX.append("email")
   else:
      show_login = False
      show_email = False 
%>
</p>

<table align="center" class="BlueTable" cellspacing="0" cellpadding="2">
    ${makeheadrow(problems)}

    % for i, c in enumerate(competitors, start=1):
    <%
        full_name = c.full_name
        c_id = c.id
        c_sum = c.sum()
        competitor_result = (c.full_stat_by_prob(p) for p in problems)
        if show_login:
            c_login = c.username
        if show_email:
            c_email = c.email
    %>
        <tr>
            <td>${i}</td>
            <td>
                <a href="${USER_SUBMITS_PREFIX}${c_id}">${full_name}</a>
            </td>
            <td>${c_sum}</td>
            %if show_login:
            <td>${c_login}</td>
            %endif
            %if show_email:
            <td>${c_email}</td>
            %endif
            ${makerow(competitor_result)}
        </tr>
    % endfor

    ${makeheadrow(problems)}
</table>
<br>
<table align='center' cellspacing="0" cellpadding="2" border="1">
    % for row in contests_table:
        ${make_contest_row(row)}
    % endfor
</table>


<%def name="makerow(competitor_result)">
    % for stat, status in competitor_result:
        <%
            html_color = status.html_color
        %>
        <td bgcolor=${html_color}>
            ${stat}
        </td>
        \
    % endfor
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
            attr = problem_attr(problem)
        %>
            <td>
                <a href="${PROBLEM_LINK_PREFIX}${problem_id}">${attr}</a>
            </td>
            \
        % endfor
    </tr>
</%def>

<%def name="make_contest_row(row)">
    <tr>
        % for name in row:
            <td>${name}</td>
            \
        % endfor
    </tr>
</%def>
