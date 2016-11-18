function content_from_highlights_ul(parts) {
    var div = "<ul>"
    // if (parts.length > 1) {
        for (var i=0; i < parts.length; i++) {
            var part = parts[i]
            div += "<li>" + part + "</li>"
        }
    // }
    div += "</ul>"
    return div;
}

function content_from_highlights_p(parts) {
    var div = "<p>"
    // if (parts.length > 1) {
        for (var i=0; i < parts.length; i++) {
            var part = parts[i]
            div += part + "(....)"
        }
    // }
    div += "</p>"
    return div;
}

$(document).ready(function() {

    $('.alert').hide()

    $('input#query').keyup(function(){
        $('.alert').hide()
        $('#info_loading').show();
        var high = 0.2
        var optimum = 0.5
        var low = 0.1

        var val = $(this).val();
        resp = es_dao.search_with_highlight(val, function(matches){
            $('#info_loading').hide();
            var found = (matches.length > 0);
            $("span#hit_count").text(matches.length)
            $('#info_no_matches').toggle(!found)
            $('#info_found').toggle(found)
            $('#response').html('');
            for (var i=0; i<matches.length; i++) {
                var highlights_content = content_from_highlights_p(matches[i]['highlights'])
                var score = matches[i]['score'];
                var div = '<div> <h3>'+matches[i]['title']+ '</h3>'+
                '<div class="score">'+score+'</div>'+
                '<meter low="'+low+'" high="'+high+'" optimum="'+optimum+'" value="'+score+'"></meter>' +
                '<div class="content">'+ highlights_content +'</div> ' +
                ' </div>';
                $('#response').append(div);
            }
        });
    });


    $('input#fuzzy_query').keyup(function(){
        var val = $(this).val();
        var fuzziness = $('#fuzziness').val();
        resp = es_dao.search_with_highlight_fuzzy(val, fuzziness, function(matches){
            $('#response').html('');
            console.log(matches);
            for (i=0; i<matches.length; i++) {
                var div = '<div> <h3>'+matches[i]['title']+ '</h3> <div class="content">'+ matches[i]['content'] +'</div> </div>';
                $('#response').append(div);
            }
        });
    });

});