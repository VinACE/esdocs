import os
from elasticsearch import Elasticsearch
from path import path



if __name__ == '__main__':

    ES_EXPORTER_ADDRESS = os.environ.get('ES_EXPORTER_ADDRESS') or 'http://localhost:9200'
    ES_EXPORTER_INDEX = os.environ.get('ES_EXPORTER_INDEX') or 'es_exporter'
    print(ES_EXPORTER_ADDRESS)

    es = Elasticsearch([ES_EXPORTER_ADDRESS])  
    filename = "C:\\Temp\\pdf-test.pdf"
    # content = path(filename).bytes()

    with open(filename,'rb') as f: content = f.read()
    print(content)


    doc = {
        "my_attachment" : {
            "_content_type" : "application/pdf",
            "_name" : "resource/name/of/my.pdf",
            "_language" : "en",
            "_content" : content
        }
    }
    
    res = es.index(index="test", doc_type='person', id=1, body=doc)
