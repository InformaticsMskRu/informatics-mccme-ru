% if result:
    <div align="center">${user_name}<br>${problem_name}</div>
	% if hint:
	    ${hint}
	% else:
	    К сожалению, по этой посылке нет подсказок
	% endif
% else:
    ${message}
% endif