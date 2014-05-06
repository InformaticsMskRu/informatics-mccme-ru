<html>
<head>
    <script type="text/javascript" src="/py-source/js/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="/py-source/js/jsrender.js"></script>
    <script type="text/javascript" src="/py-source/js/bootstrap.js"></script>
    <link rel="stylesheet" href="/py-source/css/bootstrap.css" type="text/css" media="screen" charset="utf-8" />
</head>


<style>
</style>

<script type="text/javascript">

function make_source_show() {
    jQuery.post("/py-source/source/adm/form", {}, function(data) {
        jQuery("#source_tree_div_body").html(data);
        document.getElementById("make_contest_statement_id").value = -1;
        // jQuery("#source_tree_div").show();
    });
}

make_source_show();

</script>

<body>
    <div id="source_tree_status">

    </div>
    <div id="source_tree_div_body" style="position: absolute; left: 0px; right: 0px;
                bottom: 0px; top: 20px; overflow: scroll;">

    </div>
</body>
</html>
