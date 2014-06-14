% if is_admin:
    % if ok_runs:
        <h1></h1>
        Хотите предложить одно из своих решений в качестве образцового? 
        % for run in ok_runs:
            <a href="/py/ideal/add_form?problem_id=${problem_id}&run_id=${run.run_id}&contest_id=${run.contest_id}">${run.contest_id}-${run.run_id}</a>&nbsp;
        % endfor
    % endif
    % if ideals:
        % for ideal in ideals:
            <h1></h1>
            <span id="ideallink${ideal.id}">${ideal.lang} (<a href="/user/view.php?id=${ideal.author_id}">${ideal.author_name}</a>)</span>
            <pre class="prettyprint" lang="pascal">${ideal.code}</pre><p><i>${ideal.comment}</i>
        % endfor
    % else:
        <p>Для данной задачи пока не отмечено идеальных решений.
    % endif

    % if future_ideals:
        % for ideal in future_ideals:
            <h1></h1>
            <a href="/py/ideal/approve?id=${ideal.id}&status=1">Одобрить</a>
            <a href="/py/ideal/approve?id=${ideal.id}&status=-1">Отклонить</a>
            <span id="ideallink${ideal.id}">${ideal.lang} (<a href="/user/view.php?id=${ideal.author_id}">${ideal.author_name}</a>)</span>
            <pre class="prettyprint" lang="pascal">${ideal.code}</pre><p><i>${ideal.comment}</i>
        % endfor
    % else:
        <h1></h1>Для данной задачи нет неодобренных решений.
    % endif

% else:
    % if ok_runs:
        <h1></h1>
        Хотите предложить одно из своих решений в качестве образцового? 
        % for run in ok_runs:
            <a href="/py/ideal/add_form?problem_id=${problem_id}&run_id=${run.run_id}&contest_id=${run.contest_id}">${run.contest_id}-${run.run_id}</a>&nbsp;
        % endfor
        % if ideals:
            % for ideal in ideals:
                <h1></h1>
                <span id="ideallink${ideal.id}">${ideal.lang} (<a href="/user/view.php?id=${ideal.author_id}">${ideal.author_name}</a>)</span>
                <pre class="prettyprint" lang="pascal">${ideal.code}</pre><p><i>${ideal.comment}</i>
            % endfor
        % else:
            <p>Для данной задачи пока не отмечено идеальных решений.
        % endif

    % else:
        <h1></h1>
        Чтобы посмотреть код лучших решений, необходимо сначала сдать своё правильное решение
    % endif
% endif
