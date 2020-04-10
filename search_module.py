from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Document, Text
from pip._vendor import requests

es = Elasticsearch(['localhost'],port=9200)
label_query = 'Krish Trish Baloy'
label_fields = ["title"]
query = 'which series of Krish Trish Baloy is about India'
fields = ["title","cast","country","description"]

label_bm25_id = []
label_dfi_id = []
label_ib_id = []
label_dfr_id = []
label_lmj_id = []
label_tfidf_id =[]
label_lmd_id =[]

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
##bm25label
# s = Search(using=es, index="bm25netflix")
# results = s.query("simple_query_string", query=label_query, fields=label_fields, auto_generate_synonyms_phrase_query=True).execute()
# for hit in results:
#     label_bm25_id.append(hit.meta.id)
# print('This is label_bm25_id:',label_bm25_id)
# ##bm25netflix
# s = Search(using=es, index="bm25netflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# for hit in results:
#     bm25_score.append(hit.meta.score)
#     bm25_id.append(hit.meta.id)
# print('This is bm25_score:',bm25_score)
# print('This is bm25_id:',bm25_id)

##dfinetflix
# s = Search(using=es, index="dfinetflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# # scan() removed
# for hit in results:
#     dfi_score.append(hit.meta.score)
#     dfi_id.append(hit.meta.id)
# print('This is dfi_score:',dfi_score)
# print('This is dfi_id:',dfi_id)
#
# ##ibnetflix
# s = Search(using=es, index="ibnetflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# # scan() removed
# for hit in results:
#     ib_score.append(hit.meta.score)
#     ib_id.append(hit.meta.id)
# print('This is ib_score:',ib_score)
# print('This is ib_id:',ib_id)
#
# ##dfrnetflix
# s = Search(using=es, index="dfrnetflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# # scan() removed
# for hit in results:
#     dfr_score.append(hit.meta.score)
#     dfr_id.append(hit.meta.id)
# print('This is dfr_score:',dfr_score)
# print('This is dfr_id:',dfr_id)
#
# ##lmjnetflix
# s = Search(using=es, index="lmjnetflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# # scan() removed
# for hit in results:
#     lmj_score.append(hit.meta.score)
#     lmj_id.append(hit.meta.id)
# print('This is lmj_score:',lmj_score)
# print('This is lmj_id:',lmj_id)
#
# ##tfidfnetflix
# s = Search(using=es, index="tfidfnetflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# # scan() removed
# for hit in results:
#     tfidf_score.append(hit.meta.score)
#     tfidf_id.append(hit.meta.id)
# print('This is tfidf_score:',tfidf_score)
# print('This is tfidf_id:',tfidf_id)
#
# ##lmdnetflix
# s = Search(using=es, index="lmdnetflix")
# results = s.query("simple_query_string", query=query, fields=fields, auto_generate_synonyms_phrase_query=True).execute()
# # scan() removed
# for hit in results:
#     lmd_score.append(hit.meta.score)
#     lmd_id.append(hit.meta.id)
# print('This is lmd_score:',lmd_score)
# print('This is lmd_id:',lmd_id)

label_index = "bm25netflix"
index = "bm25netflix"
def label(label_index):
    s = Search(using=es, index=label_index)
    results = s.query("simple_query_string", query=label_query, fields=label_fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        label_bm25_id.append(hit.meta.id)
    print('This is label_bm25_id:', label_bm25_id)
    return label_bm25_id
def Similarity_module(index):
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=query, fields=fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        bm25_score.append(hit.meta.score)
        bm25_id.append(hit.meta.id)
    print('This is bm25_score:', bm25_score)
    print('This is bm25_id:', bm25_id)
    return bm25_score,bm25_id

def cal_rec_pre(label_id,search_id):
    tmp = [val for val in label_id if val in search_id]
    precision = len(tmp) / len(bm25_id)
    recall = len(tmp) / len(label_bm25_id)
    print("This is Precision:",precision)
    print("This is Recall:",recall)
    return precision,recall

print("-----------BM25-----------")
label_id=label(label_index)
module_socre,module_id=Similarity_module(index)
cal_rec_pre(label_id,module_id)




