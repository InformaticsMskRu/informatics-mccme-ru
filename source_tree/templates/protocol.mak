<script>
    function test_show_info(test_num) {
        jQuery(".test_" + test_num + "_info").html("info");
    }
</script>

<table align="center" class="BlueTable" cellpadding="2" cellspacing="0" width="100%" height="100%">
<tr class="Caption">
    <td>Тест</td>
    <td>Статус</td>
    <td>Время работы</td>
    <td>Астрономическое время работы</td>
    <td>Используемая память</td>
    <td>Доп. инф.</td>
    <td>Баллы</td>
    <td>Действия</td>
</tr>
%for test in tests:
    <tr>
        <td>${loop.index + 1}</td>
        <td>${test['status']}</td>
        <td>${test['time']}</td>
        <td>${test['real-time']}</td>
        <td>${test['memory']}</td>
        <td>TODO</td>
        <td>${test['score']}(${test['nominal-score']})</td>
        <td><a href="javascript: test_show_info(${loop.index + 1});">Подробнее</a></td>
        <div class="test_${loop.index + 1}_info"></div>
    </tr> 
%endfor
</table>
