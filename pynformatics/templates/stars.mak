## -*- coding: utf-8 -*- 
    <i><b>Избранное:</b> 
        % for star in stars:
            <a href='${star["link"]}'>${star["title"]}</a><img class="star" width="10" id='${star["link"]}' src="/pix/stars/yellow-star.png" onclick="toggle(this);">
        % endfor        
    </i>