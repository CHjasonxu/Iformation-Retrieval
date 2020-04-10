from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Document, Text
from pip._vendor import requests

es = Elasticsearch(['localhost'],port=9200)

bm25_score = []
dfi_score = []
ib_score = []
dfr_score = []
lmj_score = []
tfidf_score =[]
lmd_score =[]

##bm25netflix
s = Search(using=es, index="bm25netflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    bm25_score.append(hit.meta.score)
print('This is bm25_score:',bm25_score)

##dfinetflix
s = Search(using=es, index="dfinetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    dfi_score.append(hit.meta.score)
print('This is dfi_score:',dfi_score)

##ibnetflix
s = Search(using=es, index="ibnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    ib_score.append(hit.meta.score)
print('This is ib_score:',ib_score)

##dfrnetflix
s = Search(using=es, index="dfrnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    dfr_score.append(hit.meta.score)
print('This is dfr_score:',dfr_score)

##lmjnetflix
s = Search(using=es, index="lmjnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    lmj_score.append(hit.meta.score)
print('This is lmj_score:',lmj_score)

##tfidfnetflix
s = Search(using=es, index="tfidfnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    tfidf_score.append(hit.meta.score)
print('This is tfidf_score:',tfidf_score)

##lmdnetflix
s = Search(using=es, index="lmdnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    lmd_score.append(hit.meta.score)
print('This is lmd_score:',lmd_score)