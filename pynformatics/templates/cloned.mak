<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Результат клонирования</title>
</head>
<body>
  <div id="content">
    %if result == "OK":
    Контест ${contest_id} удачно клонирован.<br/>
    ID копии - ${new_contest_id}.<br/>
    <b>Не забудьте стартовать контест копию!</b>
    %else:
    Произошла ошибка. <br/>
    status: ${status} <br/>
    message: ${message} <br/>
    %endif
  </div>
</body>
</html>
