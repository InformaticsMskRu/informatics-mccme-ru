%if not frame:
<head>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <link href="/py-source/css/bootstrap.css" rel="stylesheet">

	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width">
	<script src="http://informatics.msk.ru/lib/jquery/2.0.0/jquery.min.js"></script>
	<link href="http://informatics.msk.ru/bootstrap/css/bootstrap-combined.no-icons.min.css" rel="stylesheet">
	<link href="http://informatics.msk.ru/lib/fontawesome/css/font-awesome.css" rel="stylesheet">	
</head>

%endif

<script>
jQuery(function() {
    jQuery("#add_category").on('click', function(e) {
        jQuery("#adding-form").hide();
        jQuery(".reload-status").show();
        jQuery.post("/py-source/course/add", {
            parent_id: jQuery("#parent_categories").prop("value"),
            order: "end",
            name: jQuery("#category_name").prop("value"),
        }, function(data) {
            if (data.result == "error") {
                alert(data.content);
            }   
            document.location.reload(); 
        });
    });
});

function erase_category(category_id) {
    jQuery.post("/py-source/course/erase/" + category_id, {
    }, function(data) {
        if (data.result == "error") {
            alert(data.content);
        }   
        document.location.reload(); 
    });   
}
</script>

<script>
function updateStorage(name, mode) {
    if (localStorage['regions']) {
        json = JSON.parse(localStorage['regions']);
    } else {
        json = JSON.parse('{}');
    }
    json['#' + name] = mode;
    localStorage['regions'] = JSON.stringify(json);
}

function node_off(name) {
    jQuery(name + ' > ul > li').hide();
}

function node_on(name) {
    jQuery(name).parents("li").show();
    jQuery(name).parents("li").find("> ul > li").show();
    jQuery(name).find("> ul > li").show();
    jQuery(name).show();
}

jQuery(function () {
    var displayed_nodes = {};
    if (localStorage['regions']) {
        displayed_nodes = JSON.parse(localStorage['regions']);
    } else {
        //displayed_nodes = JSON.parse('{}');
        displayed_nodes = JSON.parse(jQuery('#default_storage').prop('value'));
        localStorage['regions'] = JSON.stringify(displayed_nodes);
    }
    
    for (name in displayed_nodes) {
        if (displayed_nodes[name] == 1) {
            node_on(name);      
        }
    }
    
    for (name in displayed_nodes) {
        if (displayed_nodes[name] == 0) {
            node_off(name);
        }
    }
    
    jQuery("li:visible > ul > li:visible").parent().parent().find("> a.node > i").removeClass("icon-collapse");
    jQuery("li:visible > ul > li:visible").parent().parent().find("> a.node > i").addClass("icon-collapse-top");

    jQuery('.tree a.show_all_button').on('click', function(e) {
        if (typeof this.show_all == 'undefined') {
            this.show_all = 1;
        }
        else {
            this.show_all = !this.show_all;
        }

        jQuery('a.show_all_button').html(this.show_all ? "Обратно" : "Развернуть всё");

        if (this.show_all) {
            jQuery('.tree li').show();
        }
        else {
            jQuery('.tree > ul > li li').hide();
            var displayed_nodes = {};
            if (localStorage['regions']) {
                displayed_nodes = JSON.parse(localStorage['regions']);
            }
            
            for (name in displayed_nodes) {
                if (displayed_nodes[name] == 1) {
                    node_on(name);      
                }
            }
            
            for (name in displayed_nodes) {
                if (displayed_nodes[name] == 0) {
                    node_off(name);
                }
            }
        }
        e.stopPropagation();
    });
    
    jQuery('.tree a.node').on('click', function(e) {
        var p = jQuery(jQuery(this).parent());
        var id = p[0].id;
        var children = p.find('> ul > li');
        if (children.is(":visible")) {
            updateStorage(id, 0);       
            children.hide();
            p.find('> a.node > i').removeClass("icon-collapse-top");
            p.find('> a.node > i').addClass("icon-collapse");        
        } 
        else {
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

    jQuery('.tree a.action-add').on('click', function(e) {
        var p = jQuery(jQuery(this).parent());
        var add_son_bar = p.find('> div.add-son');
        if (add_son_bar.is(':visible')) {
            add_son_bar.hide();
        }
        else {
            add_son_bar.show();
        }
    });

    jQuery('.tree a.action-edit').on('click', function(e) {
        var p = jQuery(jQuery(this).parent());
        var action_bar = p.find('> div.actions');
        if (action_bar.is(':visible')) {
            action_bar.hide();
        }
        else {
            action_bar.show();
        }
    });

    jQuery('.tree a.action-erase').on('click', function(e) {
        var p = jQuery(jQuery(this).parent());
        var node_id = p.find('> .node-id').prop('value');
        if (confirm("Вы уверены?")) {
            jQuery.post("/py-source/course/erase/" + node_id, {
            }, function(data) {
                if (data.result == "error") {
                    alert(data.content);
                }   
                document.location.reload(); 
            });   
        }
    });

    jQuery('.tree div.add-son > a.action-add').on('click', function(e) {
        var p = jQuery(jQuery(this).parent().parent());
        var node_id = p.find('> .node-id').prop('value');
        jQuery.post("/py-source/course/add", {
            'parent_id': node_id,
            'name': p.find('> div.add-son > .node-name').prop('value'),
            'order': 'end',
        }, function(data) {
            if (data.result == "error") {
                alert(data.content);
            }   
            document.location.reload(); 
        });   

    });

    jQuery('.tree div.actions > a.action-save').on('click', function(e) {
        var p = jQuery(jQuery(this).parent().parent());
        var node_id = p.find('> .node-id').prop('value');
        jQuery.post("/py-source/course/update/" + node_id, {
            'name': p.find('> div.actions > .node-name').prop('value'),
        }, function(data) {
            if (data.result == "error") {
                alert(data.content);
            }   
            document.location.reload(); 
        });   
    });
}); 

</script>

<style>
.tree {
    padding: 0px 0px 0px 20px;
}

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
a.show_all_button{
    display: inline-block;
    border: 1px solid #ccc;
    padding: 3px 5px;
    text-decoration: none;
    color: #666;
    height: 18px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    font-weight: 900;
    border-radius: 3px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
}

a.show_all_button:hover {
    background-color: #FEF6F0;
}

div.actions {
    padding: 6px 10px;
    border-radius: 3px;
    background-color: #f8f8ff;
}

div.add-son {
    padding: 6px 10px;
    border-radius: 3px;
    background-color: #f8f8ff;
}

a.act-button {
    display: inline-block;
    border: 1px solid #ccc;
    padding: 0px 2px;
    text-decoration: none;
    color: #666;
    background-color: #efe;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    font-weight: 900;
    border-radius: 3px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
}

a.act-button:hover {
    background-color: #ffd;
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

li > a.action {
}

li > a.action:hover {
    text-decoration: none;
}

li > a.action > i:hover {
    color: #880;
}

li > div.actions {
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

<input type="hidden" id="default_storage" value='${default_storage | n}'>
	<div class="tree" style="position: relative; margin-left: -10px;">
		<%def name="show_tree(course, depth=-1)">
			%if course.course:
                <li>
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
                </li>
			%else:
                <li id="region${course.id}"
                    %if depth > 0:
                        class="starthidden"
                    %endif
                >
                    <input type="hidden" class="displayed" value="${int(course.displayed)}">
                    <input type="hidden" class="node-id" value="${course.id}">
                    <a href="#" class="node ${"category" if depth == 0 else ""}" style="${"font-size: 1.2em;" if depth == 0 else ""}">
                        %if depth == 0:
                            <img src="/pix/i/course.gif" alt="">&nbsp;
                        %endif
                        ${course.name}&nbsp;&nbsp;
                    <i class="icon-collapse"></i></a>
                    <a href="#" class="action action-add" style="color: #a20;">
                        <i class="icon-plus"></i>
                    </a>
                    <a href="#" class="action action-edit" style="color: #c40;">
                        <i class="icon-edit"></i>
                    </a>
                    <a href="#" class="action action-erase" style="color: #f00;" onClick="erase_category(${course.id});">
                        <i class="icon-minus-sign"></i>
                    </a>
                    <div class="actions" style="display: none;">
                        <input type="text" class="node-name" value="${course.name}">
                        <br>
                        <a href="#" class="act-button action-save">Сохранить</a>
                    </div>
                    <div class="add-son" style="display: none;">
                        <label>Добавить раздел</label>
                        <input type="text" class="node-name" value="" placeholder="Имя дочернего раздела">
                        <br>
                        <a href="#" class="act-button action-add">Добавить</a>
                    </div>
                    <div class="loading" style="display: none;">
                    </div>
                    <ul class="${"main_node" if depth == 0 else ""}">
                        %for child in course.children:
                            %if (not child.course_id or child.course) and (show_hidden or (child.visible and child.verified and (not child.course or child.course.visible))):	
                                    ${show_tree(child, depth + 1)}
                            %endif
                        %endfor
                    </ul>
                </li>
			%endif	
		</%def>	
        <!--
        <a href="#" class="show_all_button" style="position: absolute; right: 6px; top: 6px; z-index: 1000;">
            Развернуть всё
        </a>
        -->
        %for node in root_nodes:
            <div>
                ${show_tree(node, 0)}
            </div>
        %endfor
	</div>




<div class="bootstrap">
    <div>
        <label>
            Мои неподтвержденные разделы:
        </label>
        <div slass="unverified-nodes-list">
            %for node in my_unverified_nodes:
                <div class="unverified-node">
                    <span style="padding: 4px 4px; background-color: #eee;">
                        ${node.full_name()}
                    </span>
                    <span>
                        <a href="#">Удалить</a>
                    </span>
                </div>
            %endfor
        </div>
    </div>
    <div id="adding-form">
        <div>
            Имя раздела:
            <input type="text" id="category_name" value="">
        </div>
        <div>
            Добавить в:
            <select id="parent_categories">
                %for item in course_list:
                    <option id="course_node_${item[1].id}" value="${item[1].id}">
                        ${"&nbsp;" * item[0] * 2 | n}${item[1].name}
                    </option>
                %endfor
            </select>
        </div>
        <div>
            <a id="add_category" class="btn" href="#">Добавить</a>
        </div>
    </div>
    <div class="reload-status progress progress-striped active" style="display: none;">
        <div class="bar bar-warning" style="width: 100%;">Загрузка...</div>
    </div>
<div>

