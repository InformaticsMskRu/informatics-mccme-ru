<!-- #22 -->
% if result:
    <table border="1">
    % for i, res in enumerate(result):
        <tr>
            <td>${i+1}</td>
            <td><a target="_blank" href="/user/view.php?id=${res.author_id}">${res.lastname} ${res.firstname}</a></td>
            <td>${res.sum}</td>
        </tr>
    % endfor
    </table>
% else:
    ${message}
% endif