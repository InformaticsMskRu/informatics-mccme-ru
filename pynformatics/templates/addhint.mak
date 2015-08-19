<!DOCTYPE html>
<html><head><title>New hint</title></head>
<script src="/lib/jquery/2.0.0/jquery.min.js"></script>
<script>
$(function(){$('#runform').submit(loadRun);$('#hintform').submit(sendHint);});
function loadRun()
{
$.get("/py/hint/get_run?contest_id="+$('#contestid').val()+'&run_id='+$('#runid').val(), function(request){
  if(request.result != 'ok')
    return;
  $('input[name="contest_id"]').val(request.contest_id);
  $('input[name="problem_id"]').val(request.problem_id);
  $('input[name="signature"]').val(request.signature);
  $('#problem_link').attr('href', '/mod/statements/view3.php?chapterid=' + request.moodle_problem_id).text('Problem ' + request.moodle_problem_id);
  $('#code').text(request.code)
  $('#code_container').slideDown();
});
return false;
}
function sendHint()
{
    $.post("/py/hint/add", $("#hintform").serialize(), function(response){
	  if(response.result == 'ok')
	  {
	    $('#hintform input[type="text"]').val('');
		$('#code_container').slideUp();
	  }
	  else
	    alert(response.message + "\n" + response.stack);
	});
	return false;
}
</script>
<body>
<p>
<form id="runform">
<table>
<tr>
<td><input id="contestid"></td><td>Contest id</td></tr>
<tr><td><input id="runid"></td><td>Run id</td></tr>
<tr><td colspan="2"><button type="submit" style="width:100%">Get run info</button></td></tr>
</table>
</form>
</p>
<div id="code_container" style="display:none">
<p><a target="_blank" id="problem_link"></a></p>
Code:<br>
<pre id="code"></pre>
</div>
<p>
<form id="hintform">
<table>
<tr><td><input type="text" name="contest_id" style="width:99%"></td><td>Contest id</td></tr>
<tr><td><input type="text" name="problem_id" style="width:99%"></td><td>Problem id</td></tr>
<tr><td width="400px"><input type="text" name="signature" style="width:99%"></td><td>Signature</td></tr>
<tr><td><input type="text" name="comment" style="width:99%"></td><td>Comment</td></tr>
<tr><td colspan="2"><input type="submit" style="width:99%"></td></tr> 
</form></p>
</body></html>