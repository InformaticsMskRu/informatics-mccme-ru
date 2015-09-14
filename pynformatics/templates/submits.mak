<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Посылки</title>
</head>
<body>
  <div id="content">
    <div align='center' width='100%' height='100%'>
      <div class="middle align-center">
        <table border="1" width="100%" height="100%">
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
                <td></td>
                <td>${submit["status"]}</td>
                <td>${submit["test_num"]}</td>
                <td>${submit["score"]}</td>
                <td></td>
            </tr>
          %endfor
        </table>
      </div>
    </div>
  </div>
</body>
</html>
