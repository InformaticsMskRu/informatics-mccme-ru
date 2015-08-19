<h1></h1>
% if hints:
<style>
.hint_table td{border:1px solid gray;padding:5px;}
</style>
    <table class="hint_table" style="border:1px solid gray;border-collapse:collapse;border-spacing:1px;">
	% for hint in hints:
	    <tr><td>${hint[0]}</td><td>${hint[1]}</td></tr>
	% endfor
	</table>
% else:
    <p>Для этой задачи нет подсказок</p>
% endif