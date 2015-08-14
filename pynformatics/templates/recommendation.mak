% if recommendations:
    % for pid in recommendations:
        <a href="/mod/statements/view3.php?chapterid=${pid[0]}" target="_top">${pid[1]}</a><br>
    % endfor
% else:
    Рекомендаций пока нет
% endif