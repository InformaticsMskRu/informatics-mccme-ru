<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Посылки</title>
</head>
<body>
  <div id="content">
    <table border="1">
      <tr>
        <td>ID</td>
        <td>Название контеста</td>
        <td>Количество посылок</td>
      </tr>
      %for contest in contests:
        <tr>
            <td>${contest["contest_id"]}</td> 
            <td>${contest["name"]}</td> 
            <td>${contest["submits_count"]}</td> 
        </tr>
      %endfor
    </table>
  </div>
</body>
</html>
