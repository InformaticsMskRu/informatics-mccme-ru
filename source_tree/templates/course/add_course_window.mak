<!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]> <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]> <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width">
    %if not frame:
	<script src="http://informatics.mccme.ru/lib/jquery/2.0.0/jquery.min.js"></script>
	<link href="http://informatics.mccme.ru/bootstrap/css/bootstrap-combined.no-icons.min.css" rel="stylesheet">
    %endif
	<link href="http://informatics.mccme.ru/lib/fontawesome/css/font-awesome.css" rel="stylesheet">	
</head>


<style>

.tree ul.main_node {
    padding:  0px 0px 0px 0px;  
}

.tree li {
    margin: 0px 0;
    list-style-type: none;
    position: relative;
    padding: 5px 5px 0px 5px;
}
.tree li::before {
    content:'';
    position: absolute;
    top: 0;
    width: 1px;
    height: 100%;
    right: auto;
    left: -20px;
    border-left: 1px solid #ccc;
    bottom: 40px;
}
.tree li::after {
    content:'';
    position: absolute;
    top: 15px;
    width: 25px;
    height: 15px;
    right: auto;
    left: -20px;
    border-top: 1px solid #ccc;
}
.tree li a.node{
    display: inline-block;
    border: 1px solid #ccc;
    padding: 3px 5px;
    text-decoration: none;
    color: #666;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    border-radius: 3px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
}

.tree li a.add-course-link {
    display: inline-block;
    border: 1px solid #ccc;
    padding: 3px 5px;
    text-decoration: none;
    color: #884;
    font-weight: 900;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    border-radius: 3px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
}

.tree li a.add-course-link:hover {
    background: rgb(254, 249, 246);
    color: #000;
    border: 1px solid #94a0b4;
}

a.show_all_button{
    display: inline-block;
    border: 1px solid #ccc;
    padding: 3px 5px;
    text-decoration: none;
    color: #666;
    height: 18px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    border-radius: 3px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
}

.show_all_button:hover {
    background-color: #FEF6F0;
}

.tree li span {
    display: inline-block;
    border: 1px solid #ccc;
    padding: 1px 1px;
    text-decoration: none;
    color: #666;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    border-radius: 2px;
    -webkit-border-radius: 2px;
    -moz-border-radius: 2px;
}

/*Remove connectors before root*/
 .tree > ul > li::before, .tree > ul > li::after {
    border: 0;
}
/*Remove connectors after last child*/
 .tree li:last-child::before {
    height: 15px;
}
/*Time for some hover effects*/

/*We will apply the hover effect the the lineage of the element also*/
 .tree li a.node:hover, .tree li a.node:hover+ul li a.node {
    background: rgb(254, 249, 246);
    color: #000;
    border: 1px solid #94a0b4;
}
/*Connector styles on hover*/
 .tree li a.node:hover+ul li::after, .tree li a.node:hover+ul li::before, .tree li a.node:hover+ul::before, .tree li a.node:hover+ul ul::before {
    border-color: #94a0b4;
}

.starthidden { display:none; }

</style>

<script type="text/javascript">

function updateStorage(name, mode) {
//  alert(name);
    if (localStorage['regions']) {
        json = JSON.parse(localStorage['regions']);
    } else {
        json = JSON.parse('{}');
    }
    json['#' + name] = mode;
    localStorage['regions'] = JSON.stringify(json);
}

function node_off(name) {
    $(name + ' > ul > li').hide();
}

function node_on(name) {
    $(name).parents("li").show();
    $(name).parents("li").find("> ul > li").show();
    $(name).find("> ul > li").show();
    $(name).show();
}

$(function () {

    if (localStorage['regions']) {
        json = JSON.parse(localStorage['regions']);
    } else {
        json = JSON.parse('{}');
    }
    
    for (name in json) {
        if (json[name] == 1) {
            node_on(name);      
        }
    }
    
    for (name in json) {
        if (json[name] == 0) {
            node_off(name);
        }
    }

    $("li :visible :not(:has(> ul > li:visible))").find("> a.node > i").removeClass("icon-collapse-top");
    $("li :visible :not(:has(> ul > li:visible))").find("> a.node > i").addClass("icon-collapse");

    $("li :visible :has(> ul > li:visible)").find("> a.node > i").removeClass("icon-collapse");
    $("li :visible :has(> ul > li:visible)").find("> a.node > i").addClass("icon-collapse-top");

    jQuery('.tree a.add-course-link').on('click', function(e) {
        var parent = jQuery(jQuery(this).parent());
        var course_node_id = parent.find('> input.course_node_id').prop('value');
        parent.find('> div.add-course-desc').html('Loading...');
        jQuery.post("/py-source/course/add", {
            'name': '+++${course_raw.id}',
            'order': 'end',
            'parent_id': course_node_id,
        }, function(data) {
            parent.find('> div.add-course-desc').html(data.result == 'ok' ? 'OK' : ('Error: ' + data.content));
        });
    });

    jQuery('.tree a.node').on('click', function (e) {
        var p = jQuery(jQuery(this).parent());
        var id = p[0].id;
        var children = p.find('> ul > li');
        if (children.is(":visible")) {
            updateStorage(id, 0);       
            children.hide();
            p.find('> a.node > i').removeClass("icon-collapse-top");
            p.find('> a.node > i').addClass("icon-collapse");        
        } 
        else 
        {
            updateStorage(id, 1);       
            children.show();
            p.find('> a.node > i').removeClass("icon-collapse");
            p.find('> a.node > i').addClass("icon-collapse-top");        
        }
        
        e.stopPropagation();
        if (children.length > 0) {
            return false;
        }
    });

});     
</script>


<table class="categorylist"><tr><td>
	<div class="tree" style="margin-left: -10px;">
		<%def name="show_tree(course, depth=-1)">
			%if course.course:
				<a style="${"color: grey;" if not course.course.visible else ""}${"font-size: 1.2em;" if depth == 1 else ""}" href="/course/view.php?id=${course.course_id}">
                %if depth == 1:
                    <img src="/pix/i/course.gif" alt="">&nbsp;
                %endif
                    ${course.name if course.name else course.course.full_name}
                </a>
				%if course.course.password:
					<span style="position:relative; float:right;"><i class="icon-key"></i></span>
				%endif
				%if not course.course.visible:
					<span style="position:relative; float:right;"><i class="icon-eye-close"></i></span>
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
                    <li class="starthidden">
                        <input type="hidden" class="course_node_id" value="${course.id}">
                        <a class="add-course-link" href="#">
                            <i class="icon-plus"></i>
                            &nbsp;Прикрепить источник
                        </a>
                        <div style="display: inline-block;" class="add-course-desc">
                        </div>
                    </li>
					%for child in course.children:
						%if (not child.course_id or child.course) and (child.visible and (not child.course or child.course.visible)):	
							%if depth > 0:
								<li id="region${child.id}" class="starthidden">
							%else:
								<li id="region${child.id}">
							%endif
								${show_tree(child, depth + 1)}
							</li>
						%endif
					%endfor
				</ul>
			%endif	
		</%def>	
        <!--<a href="#" class="show_all_button" onClick="123node_on('a.node');" style="margin-left: 4px;">
            Развернуть все
        </a>-->
		${show_tree(course, 0)}
	</div>
</td></tr></table>


</body>
</html>

