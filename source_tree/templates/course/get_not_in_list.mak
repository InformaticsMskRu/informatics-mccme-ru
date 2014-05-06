<html>
<head>
</head>

<body>
    %for course in courses:
        <a href="/course/view.php?id=${course.id}">${course.fullname}</a><br>
    %endfor
</body>

</html>
