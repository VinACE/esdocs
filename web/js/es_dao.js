EsDao = function() {



    this.search_with_highlight = function(query, success) {
        var host = 'http://localhost:9200';
        var index = 'test';
        var type = 'attachment';
        data = {
          "size" : 100,
          "query": {
            "match": {
              "file.content": query
            }
          },
          "highlight": {
            
            "pre_tags" : ["<mark>"],
            "post_tags" : ["</mark>"],
            "fields": {
              "file.content": {
                    "fragment_size" : 50,
                    "number_of_fragments" : 20
              }
            }
          }
        };
        url = host+'/'+index+'/'+type+'/_search'
        $.ajax({
            type: 'POST',
            url : url,
            dataType: 'json',
            data : JSON.stringify(data),
            success: function(resp){
                len = resp.hits.hits.length;
                elements = [];
                if (len > 0) {                    
                    // console.log(resp.hits.hits[0])
                    for (i=0; i<len; i++) {   

                        title = resp.hits.hits[i]['_source']['title'];
                        score = resp.hits.hits[i]['_score']
                        len2 = resp.hits.hits[i]['highlight']['file.content'].length;
                        highlights = []
                        content = ''
                        for (ii=0; ii<len2; ii++) {
                            partial_content = resp.hits.hits[i]['highlight']['file.content'][ii];
                            highlights.push(partial_content);
                            content += partial_content+'\r\n'
                        }
                        el = {
                            highlights: highlights,
                            content: content,
                            title: title,
                            score: score
                        }
                        elements.push(el);
                    }                    
                } 
                success(elements);
            },
            error: function(e) {
                console.error(e)
            }
        })
    }


    this.search_with_highlight_fuzzy = function(query, fuzziness, success) {
        var host = 'http://localhost:9200';
        var index = 'test';
        var type = 'attachment';
        data = {
          "query": {
            "fuzzy" : { 
              "file.content" : {
                "value" : query,
                "boost" : 1.0,
                "fuzziness" : fuzziness
              }
            }
          },
          "highlight": {
            "fields": {
              "file.content": {
              }
            }
          }
        };
        url = host+'/'+index+'/'+type+'/_search'
        $.ajax({
            type: 'POST',
            url : url,
            dataType: 'json',
            data : JSON.stringify(data),
            success: function(resp){
                console.log(resp);
                len = resp.hits.hits.length;
                elements = [];
                if (len > 0) {                    
                    for (i=0; i<len; i++) {
                        content = resp.hits.hits[i]['highlight']['file.content'][0];
                        title = resp.hits.hits[i]['_source']['title'];
                        el = {
                            content: content,
                            title: title
                        }
                        elements.push(el);
                    }                    
                } 
                success(elements);
            },
            error: function(e) {
                console.error(e)
            }
        })
    }
}


es_dao = new EsDao();