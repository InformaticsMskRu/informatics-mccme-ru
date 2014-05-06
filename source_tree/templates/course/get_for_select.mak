%for item in course_list:
    <option id="course_node_${item[1].id}" value="${item[1].id}">
        ${"&nbsp;" * item[0] * 2 | n}${item[1].name}
    </option>
%endfor
