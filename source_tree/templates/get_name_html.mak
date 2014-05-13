%for parents in source_list:
    <div class="source_path">
    %if source_type == 'subject':
        <a href="/py-source/source/dir/${parents[len(parents) - 2].id}">${parents[len(parents) - 2].name}</a>
    %else:
        %for i in range(len(parents)):
            %if i >= 2:
                %if i != len(parents) - 1: 
                    <a href="/py-source/source/dir/${parents[i].id}">${parents[i].name}</a>,
                %else:
                    ${parents[i].name}
                %endif
            %endif
        %endfor
    %endif
    </div>
%endfor
