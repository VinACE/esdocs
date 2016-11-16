import os
import sys
from elasticsearch import Elasticsearch

# constants, configure to match your environment
HOST = 'http://localhost:9200'
INDEX = 'test'
TYPE = 'attachment'
TMP_FILE_NAME = 'tmp.json'
# for supported formats, see apache tika - http://tika.apache.org/1.4/formats.html
INDEX_FILE_TYPES = ['html','pdf', 'doc', 'docx', 'xls', 'xlsx', 'xml']
es = Elasticsearch([HOST])


def log(txt):
    print(txt)


def main():
    current_dir = os.getcwd()
    log(current_dir)
    indexDir(current_dir+'\\talks')


def indexFile(fname):
    log('\nIndexing ' + fname)
    createEncodedTempFile(fname)
    postFileToTheIndex()
    os.remove(TMP_FILE_NAME)
    
def indexDir(dir):

    log('Indexing dir ' + dir)

    # es.indices.delete(index=INDEX)
    createIndexIfDoesntExist()

    for path, dirs, files in os.walk(dir):
        for file in files:
            fname = os.path.join(path,file)

            base,extension = file.rsplit('.',1)

            if extension.lower() in INDEX_FILE_TYPES:
                indexFile(fname)
            else:
                'Skipping {}, not approved file type: {}'.format(fname, extension)

def postFileToTheIndex():
    import json
    log(TMP_FILE_NAME)
    f = open(TMP_FILE_NAME, 'r')
    doc = json.load(f)      
    res = es.index(index=INDEX, doc_type=TYPE, body=doc)


def createEncodedTempFile(fname):
    import json
    file64 = open(fname, "rb").read().encode("base64")
    log('writing JSON with base64 encoded file to temp file {}'.format(TMP_FILE_NAME))

    f = open(TMP_FILE_NAME, 'w')
    data = { 'file': file64, 'title': fname }
    json.dump(data, f) # dump json to tmp file
    f.close()
    log('written')

def createIndexIfDoesntExist():
    if not es.indices.exists(INDEX):
        

        body = {
            "mappings" : {
                "attachment" : {
                    "properties" : {
                        "file" : {
                            "type" : "attachment",  
                            "fields": {
                                "content": {
                                    "type": "string",
                                    "term_vector":"with_positions_offsets",
                                    "store": True,
                                    "analyzer": "english"
                                }
                            }
                        }
                    }
                }
            }
        }

        es.indices.create(index=INDEX, body=body)
        log('index {} created'.format(INDEX))




# kick off the main function when script loads
main()
