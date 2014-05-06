%if not dump:
<!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]> <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]> <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width">
	<script src="/lib/jquery/2.0.0/jquery.min.js"></script>
	<link href="/bootstrap/css/bootstrap-combined.no-icons.min.css" rel="stylesheet">
	<link href="/lib/fontawesome/css/font-awesome.css" rel="stylesheet">	
	<link href="/ajax/css/tree.css" rel="stylesheet">	
	<script src="/ajax/js/tree/tree.js"></script>
</head>

%endif

<input type="hidden" id="default_storage" value='${default_storage | n}'>
<table class="categorylist"><tr><td>
	<div class="tree" style="position: relative; margin-left: -10px;">
		<%def name="show_tree(course, depth=-1)">
			%if course.course:
				<a style="${"color: grey;" if not course.course.visible else ""}${"font-size: 1.2em;" if depth == 1 else ""}" href="/course/view.php?id=${course.course_id}">
                %if depth == 1:
                    <img src="/pix/i/course.gif" alt="">&nbsp;
                %endif
                    ${course.name if course.name else course.course.fullname}
                    ${"(не подтв.)" if not course.verified else ""}
                </a>
				%if course.course.password:
					<span style="position:relative; float:right;"><i class="icon-key"></i></span>
				%endif
				%if not course.course.visible:
					<span style="position:relative; float:right;"><i class="icon-eye-close"></i></span>
				%endif
                %if not course.verified:
					<span style="position:relative; float:right;"><i class="icon-exclamation-sign"></i></span>
                %endif
			%else:
				%if depth > 0:
					<a href="#" class="node ${"category" if depth == 1 else ""}" style="${"font-size: 1.2em;" if depth == 1 else ""}">
                        %if depth == 1:
                            <img src="/pix/i/course.gif" alt="">&nbsp;
                        %endif
                        ${course.name}&nbsp;(${course_count[course]})&nbsp;
                    <i class="icon-collapse"></i></a>
                %endif
				<ul class="${"main_node" if depth == 0 else ""}">
					%for child in course.children:
						%if (not child.course_id or child.course) and (show_hidden or (child.visible and child.verified and (not child.course or child.course.visible))):	
							%if depth > 0:
								<li id="region${child.id}" class="starthidden">
							%else:
								<li id="region${child.id}">
							%endif
                                <input type="hidden" class="displayed" value="${int(child.displayed)}">
								${show_tree(child, depth + 1)}
							</li>
						%endif
					%endfor
				</ul>
			%endif	
		</%def>	
        <a href="#" class="show_all_button" style="position: absolute; right: 6px; top: 6px; z-index: 1000;">
            Развернуть всё
        </a>
		${show_tree(course, 0)}
	</div>
</td></tr></table>


%if not dump:
</body>
</html>

%endif
