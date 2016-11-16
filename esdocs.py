import os
import sys
from elasticsearch import Elasticsearch
import base64
import getopt


# constants, configure to match your environment
HOST = None
INDEX = None
TYPE = None
TMP_FILE_NAME = 'tmp.json'
# for supported formats, see apache tika - http://tika.apache.org/1.4/formats.html
INDEX_FILE_TYPES = ['html','pdf', 'doc', 'docx', 'xls', 'xlsx', 'xml']
es = None


def log(txt):
    print(txt)


def main(argv):
    host_arg = None
    index_arg = None
    type_arg = None
    try:
      opts, args = getopt.getopt(argv,"h:i:o:")
    except getopt.GetoptError:
      print('esdocs.py -h <ES host> -i <index name> -t <type>')
      sys.exit(2)
    for opt, arg in opts:
        print(opt)
        if opt == '-h':            
            host_arg = arg
        elif opt == '-i':
            index_arg = arg
        elif opt == '-t':
            type_arg = arg
    global INDEX,TYPE,HOST
    INDEX = index_arg or 'test'
    TYPE =  type_arg or 'attachment'
    HOST = host_arg or 'http://localhost:9200'
    print(INDEX,TYPE,HOST)
    global es
    es = Elasticsearch([HOST])
    current_dir = os.getcwd()
    indexDir(current_dir+'\\files_to_index')


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
    image_file = open(fname, "rb")
    content = image_file.read()
    file64bytes = base64.b64encode(content)
    ENCODING = 'utf-8'
    file64string = file64bytes.decode(ENCODING)

    log('writing JSON with base64 encoded file to temp file {}'.format(TMP_FILE_NAME))
    f = open(TMP_FILE_NAME, 'w')
    data = { 'file': file64string, 'title': fname }
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




if __name__ == "__main__":
   main(sys.argv[1:])
