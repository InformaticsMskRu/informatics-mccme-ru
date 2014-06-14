% if result:
    % if problems:
        % for problem in problems:
            <p><a href="/mod/statements/view3.php?chapterid=${problem}">${problem}</a>
        % endfor
    % else:
        Нет нерассмотренных предложений
    % endif
% else:
    ${message}
% endif