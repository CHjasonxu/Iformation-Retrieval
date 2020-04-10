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

bm25_id = []
dfi_id = []
ib_id = []
dfr_id = []
lmj_id = []
tfidf_id =[]
lmd_id =[]

##bm25netflix
s = Search(using=es, index="bm25netflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    bm25_score.append(hit.meta.score)
    bm25_id.append(hit.meta.id)
print('This is bm25_score:',bm25_score)
print('This is bm25_id:',bm25_id)

##dfinetflix
s = Search(using=es, index="dfinetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    dfi_score.append(hit.meta.score)
    dfi_id.append(hit.meta.id)
print('This is dfi_score:',dfi_score)
print('This is dfi_id:',dfi_id)

##ibnetflix
s = Search(using=es, index="ibnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    ib_score.append(hit.meta.score)
    ib_id.append(hit.meta.id)
print('This is ib_score:',ib_score)
print('This is ib_id:',ib_id)

##dfrnetflix
s = Search(using=es, index="dfrnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    dfr_score.append(hit.meta.score)
    dfr_id.append(hit.meta.id)
print('This is dfr_score:',dfr_score)
print('This is dfr_id:',dfr_id)

##lmjnetflix
s = Search(using=es, index="lmjnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    lmj_score.append(hit.meta.score)
    lmj_id.append(hit.meta.id)
print('This is lmj_score:',lmj_score)
print('This is lmj_id:',lmj_id)

##tfidfnetflix
s = Search(using=es, index="tfidfnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    tfidf_score.append(hit.meta.score)
    tfidf_id.append(hit.meta.id)
print('This is tfidf_score:',tfidf_score)
print('This is tfidf_id:',tfidf_id)

##lmdnetflix
s = Search(using=es, index="lmdnetflix")
query = 'The spider man collection of parallel universes'
fields = ["title","cast","country","description"]
results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# scan() removed
for hit in results:
    lmd_score.append(hit.meta.score)
    lmd_id.append(hit.meta.id)
print('This is lmd_score:',lmd_score)
print('This is lmd_id:',lmd_id)