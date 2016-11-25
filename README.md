# esdocs

## Prerequsities
* Python 3.X
* Elasticsearch 2.X with [mapper attachmentp plugin](https://github.com/elastic/elasticsearch-mapper-attachments) installed.
* Any browser

## Run
To run please do following
* Ensure your Elasticsearch listens and plugin works, check the [_nodes endpoint](http://localhost:9200/_nodes)
* Install prerequsities via pip `pip install -r requirements.txt`
* Run the scirpt

## Script usage
Running with python the main script will fallback to default options
```python
python esdocs.py
```
It will index files being in folder `\files_to_index` relative to script. You can use custom parameters as follows:
- `-h <host>` point a ES host
- `-t <type>` ES type name that document should be stored
- `-i <index_name>` ES index name that document should be stored


