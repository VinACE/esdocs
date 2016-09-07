EsDao = function() {



    this.search_with_highlight = function(query, success) {
        var host = 'http://localhost:9200';
        var index = 'test';
        var type = 'attachment';
        data = {
          "query": {
            "match": {
              "file.content": query
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