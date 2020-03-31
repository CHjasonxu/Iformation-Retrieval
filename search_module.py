from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text


es = Elasticsearch(['localhost'],port=9200)

class MyDoc(Document):
    text_field = Text(similarity='my_similarity')
    class Index:
        settings = {
        "index" : {
            "similarity" : {
              "my_similarity" : {
                "type" : "DFR",
                "basic_model" : "g",
                "after_effect" : "l",
                "normalization" : "h2",
                "normalization.h2.c" : "3.0"
              }
            }
        }
    }

res = es.search(index="netflixdata", body={"query": {"match": {"type": "Movie"}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(title)s: %(description)s" % hit["_source"])