<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Посылки</title>
  <script type="text/javascript" src="/moodle/ajax/js/jquery-1.7.2.min.js"></script>
  <script type="text/javascript" src="/mod/statements/lib/jquery_pagination/jquery.pagination.js"></script>
  <link rel="stylesheet" type="text/css" href="http://informatics.mccme.ru/theme/standard/styles.php">
  <link rel="stylesheet" type="text/css" href="http://informatics.mccme.ru/theme/formal_white/styles.php">
  <style type="text/css">@import url(http://informatics.mccme.ru/mod/statements/statements_theme.css);</style>
  <style type="text/css">@import url(http://informatics.mccme.ru/mod/statements/statements_theme.css);</style>
  <link rel="stylesheet/less" href="/bootstrap/css/bootstrap.less">
</head>
<body>
  <div id="content">
    <div align="center" width="100%">   
      <div id="Pagination" class="pagination" align="center" width="100%">
      </div>
    </div>
    <table align="center" class="BlueTable" cellpadding="2" cellspacing="0" width="100%" height="100%">
      <tr class="Caption">
        <td>ID</td>
        <td>Участник</td>
        <td>Задача</td>
        <td>Дата</td>
        <td>Язык</td>
        <td>Статус</td>
        <td>Пройдено тестов</td>
        <td>Баллы</td>
        <td>Подробнее</td>
      </tr>
      %for submit in submits:
        <tr>
            <td>${str(submit["contest_id"]) + "-" + str(submit["problem_id"])}</td> 
            <td>${submit["user"]}</td> 
            <td>${submit["problem_name"]}</td> 
            <td>${submit["date"]}</td> 
            <td>${submit["lang_name"]}</td>
            <td>${submit["status"]}</td>
            <td>${submit["test_num"]}</td>
            <td>${submit["score"] if submit["score"] > 0 else ""}</td>
            <td></td>
        </tr>
      %endfor
    </table>
    <div id='user_id' style="display: none"> ${request_params["user_id"]} </div>
    <div id='group_id' style="display: none"> ${request_params["group_id"]} </div>
    <div id='problem_id' style="display: none"> ${request_params["problem_id"]} </div>
    <div id='contest_id' style="display: none"> ${request_params["contest_id"]} </div>
    <div id='count' style="display: none"> ${count} </div>
  </div>
</body>
</html>
