function reload_page(block_num, source_id, subject_id)
{
    cnt = jQuery("#select_page_cnt_" + block_num).prop('value');
    document.location.href = '/py-source/source/dir/' + source_id + '-' + subject_id + '?cnt=' + cnt;
}
