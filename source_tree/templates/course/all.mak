<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>

<style type="text/css">
    table.courses {
    }
    
    table.courses tr {
        border: 1px solid #A0A0A0;
    }

    table.courses tr td {
        font-size: 11pt;
        padding: 6px;
    }

    table.courses thead {
        font-weight: 900;
    }
</style>

<body>
    <table class="courses">
        <thead>
            <tr>
                <td>Имя курсa</td>
                <td>Категории в дереве</td>
                <td>Учителя</td>
                <td>Есть пароль</td>
            </tr>
        </thead>
        <tbody>
            %for item in courses:
                <tr style="background-color: ${"#fff" if loop.index % 2 else "#f0f0f0"}">
                    <td>
                        <a href="/course/view.php?id=${item['course'].id}">${item['course'].full_name}</a>
                    </td>
                    <td>
                        %for path in item['paths']:
                            <div>
                                ${path}
                            </div>
                        %endfor
                    </td>
                    <td>
                        %for author in item['authors']:
                            <div>
                                <a href="/user/view.php?id=${author.id}">${"{0} {1}".format(author.firstname, author.lastname)}</a>
                            </div>
                        %endfor
                    </td>
                    <td>
                        ${"есть пароль" if item['course'].password else ""}
                    </td>
                </tr>
            %endfor
        </tbody>
    </table>
</body>

</html>
