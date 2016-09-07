$(document).ready(function() {
    $('input#query').keyup(function(){
        var val = $(this).val();
        resp = es_dao.search_with_highlight(val, function(matches){
            $('#response').html('');
            console.log(matches);
            for (i=0; i<matches.length; i++) {
                var div = '<div> <h3>'+matches[i]['title']+ '</h3> <div class="content">'+ matches[i]['content'] +'</div> </div>';
                $('#response').append(div);
            }
        });
    });
});