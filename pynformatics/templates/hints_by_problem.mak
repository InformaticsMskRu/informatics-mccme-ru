<h1></h1>
% if hints:
    <script>(function($){$(function(){
	    $('.delete-hint').click(function(event){
		  id = event.target.id.slice(6);		  
		  $.post('/py/hint/delete', {"id":id}, function(response){ 
		    if(response.result='ok')
			  $('#row'+id).hide();
		   });
		   return false;
		});
	});})(jQuery)</script>
	<style>
	.hint_table td{border:1px solid gray;padding:5px;}
	</style>
    <table class="hint_table" style="border:1px solid gray;border-collapse:collapse;border-spacing:1px;">
	% for hint in hints:
	    <tr id="row${hint[0]}"><td><a href="javascript:return false"><img src="/pix/t/delete.gif" class="delete-hint" id="delete${hint[0]}"/></a> ${hint[1]}</td><td>${hint[2]}</td></tr>
	% endfor
	</table>
% else:
    <p>Для этой задачи нет подсказок</p>
% endif