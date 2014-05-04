<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>The Pyramid Web Application Development Framework</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
</head>
<body>
  <div id="wrap">
    <div id="middle">
      <div class="middle align-center">
        <p class="app-welcome">
          % if status:
          ${tmp}
          <table border="1">
            <tr>
              <th>lang</th><th>option</th>
              %for a in contests:
                <th>${a}</th>
              % endfor
            </tr>
            %for a in langs:
                %for b in options:
                    <tr>
                        <td>${a}</td><td>${b}</td>
                        %for c in contests:
                        <td>${result[a][b][c]}</td>
                        % endfor
                    </tr>
                % endfor
             % endfor
          </table>
          % else:
            <p>${message}</p>
            <pre>${stack}</pre>
          % endif
        </p>
      </div>
    </div>
  </div>
</body>
</html>
