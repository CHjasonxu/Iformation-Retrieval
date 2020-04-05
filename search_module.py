from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text
from pip._vendor import requests

es = Elasticsearch(['localhost'],port=9200)

# es.indices.get_mapping(index='netflixdata', doc_type='cast')
#
# es.indices.put_mapping(
#     index="travel",
#     doc_type="cities",
#     body=
#         {
#
#                 "properties": {
#                     "city": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {
#                                 "type": "keyword",
#                                 "ignore_above": 256
#                             }
#                         }
#                     },
#                     "country": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {
#                                 "type": "keyword",
#                                 "ignore_above": 256
#                             }
#                         }
#                     },
#                     "datetime": {
#                         "type": "date",
#                         "format":"yyyy,MM,dd,hh,mm,ss"
#                     }
#                 }
#             }
# )

request_body = {

 "settings": {
    "index": {
      "similarity": {
        "my_similarity": {
          "type": "LMDirichlet",
          "mu": "2000",

        }
      }
    }
  }
}

print("creating 'example_index' index...")
es.indices.create(index = 'lmdirichlet', body = request_body)


# print("creating 'example_index' index...")
# es.indices.create(index = 'example_index', body = request_body)
# class MyDoc(Document):
#     text_field = Text(similarity='my_similarity')
#     class Index:
#         settings = {
#         "index" : {
#             "similarity" : {
#               "my_similarity" : {
#                 "type" : "DFR",
#                 "basic_model" : "g",
#                 "after_effect" : "l",
#                 "normalization" : "h2",
#                 "normalization.h2.c" : "3.0"
#               }
#             }
#         }
#     }
#
# res = es.search(index="netflixdata", body={"query": {"match": {"type": "Movie"}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(title)s: %(description)s" % hit["_source"])

# jsontext = '{"settings":{"index":{"similarity":{"my_similarity":{"type": "DFR","basic_model": "g","after_effect": "l","normalization": "h3","normalization.h2.c": "3.0"}}}}}'
#
# headers = {'Content-type': 'application/json',}
#
# DFRtext = requests.put('http://localhost:9200/index?pretty' , headers=headers, data=jsontext)
#
# print(DFRtext.json())

# res = es.search(index="netflixdata", body={"query": {"match": {"type": "Movie"}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(title)s: %(description)s" % hit["_source"])