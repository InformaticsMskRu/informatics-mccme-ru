% if recommendations:
    % for pid in recommendations:
        <a href="/mod/statements/view3.php?chapterid=${pid[0]}">${pid[1]}</a><br>
    % endfor
% endif