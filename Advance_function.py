from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np

##Connect with elasticsearch client
es = Elasticsearch(['localhost'],port=9200)

##Some initial variables
label_fields = ["title"]
fields = ["title","cast","country","description"]
weight_fields =["title^2","cast^1","country^1","description^3"]
label_id =[]
Similarity_score=[]
Similarity_id = []
Similarity_title = []
Similarity_name =[]
tmp_precision =0
tmp_recall =0
tmp_f_measure =0
w_tmp_precision =0
w_tmp_recall =0
w_tmp_f_measure =0
Ag_precision = []
Ag_recall = []
Ag_f_measure = []
W_Ag_precision = []
W_Ag_recall = []
W_Ag_f_measure =[]

##Give label_query to return our label_id through this function
def label(index,label_query,label_fields):
    label_id=[]
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=label_query, fields=label_fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        label_id.append(hit.meta.id)
    # print('This is label_id:', label_id)
    return label_id

##Use different models to search and match the query and return the score, id and name
def Similarity_module(index,query,fields):
    Similarity_score=[]
    Similarity_id =[]
    Similarity_title = []
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=query, fields=fields,
                      auto_generate_synonyms_phrase_query=True).execute()

    for hit in results:
        Similarity_score.append(hit.meta.score)
        Similarity_id.append(hit.meta.id)
        Similarity_title.append(hit.title)
    # print('This is Similarity_score:', Similarity_score)
    # print('This is Similarity_id:', Similarity_id)
    Similarity_score = score_normalized(Similarity_score)
    return Similarity_score,Similarity_id,Similarity_title

##Use different models to search and match the query and return the score, id and name,
##Added each term in the field, giving different weights.
def Similarity_module_weight(index,query,weight_fields):
    Similarity_score=[]
    Similarity_id =[]
    Similarity_title = []
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=query, fields=weight_fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        Similarity_score.append(hit.meta.score)
        Similarity_id.append(hit.meta.id)
        Similarity_title.append(hit.title)
    # print('This is Similarity_score:', Similarity_score)
    # print('This is Similarity_id:', Similarity_id)
    Similarity_score=score_normalized(Similarity_score)
    return Similarity_score,Similarity_id,Similarity_title

##Calculate model accuracy, recall rate and Harmonic Mean
def cal_rec_pre(label_id,search_id):
    tmp = [val for val in label_id if val in search_id]
    precision = len(tmp) / len(label_id)
    recall = len(tmp) / len(search_id)
    f_measure = (2*precision*recall)/(precision+recall)
    return precision,recall,f_measure

##Normalize the returned document score (min-max)
def score_normalized(Similarity_score):
    normalize_score = []
    min_score = min(Similarity_score)
    max_score = max(Similarity_score)
    while True:
        try:
            for i in range(len(Similarity_score)):
                if len(Similarity_score) == 1:
                    normalize_score.append(Similarity_score[0] / Similarity_score[0])
                else:
                    normalize_score.append((Similarity_score[i] - min_score) / (max_score - min_score))
            return normalize_score
        except:
            break

## Calculation of diversity between models
def Kendall_rank_correlation(model1,model2,query,fields):
    model1_score,model1_id,_=Similarity_module(model1,query,fields)
    model2_score, model2_id,_ = Similarity_module(model2, query, fields)
    Same_results = [val for val in model1_id if val in model2_id]
    N = len(model1_id)
    C = len(Same_results)
    D = N - 2 * C
    tau = (C - D) / (N * (N+1) / 2)
    return tau

##Ranking combination, you can combine multiple models and return the new document score, id and name
def rank_combination(query,index,fields):
    score = []
    id = []
    name = []
    rank = []
    for i in range(len(index)):
        _, Similarity_id, Similarity_name = Similarity_module(index[i], query, fields)
        rank += [1,2,3,4,5,6,7,8,9,10]
        id += Similarity_id
        name += Similarity_name
    # print(id)
    id_unique = sorted(set(id), key=id.index)
    rank_unique = []
    name_unique = sorted(set(name), key=name.index)
    sum_rank = 0
    for j in range (len(id_unique)):
        location = [i for i, a in enumerate(id) if a == id_unique[j]]
        for k in range(len(location)):
            sum_rank = sum_rank + rank[location[k]]
        avg_rank = sum_rank/len(location)
        rank_unique.append(float(avg_rank))
        sum_rank = 0
    rank_unique = np.array(rank_unique, dtype=np.float32)
    id_unique = np.array(id_unique, dtype=np.int32)
    name_unique = np.array(name_unique)
    rank_unique = rank_unique[np.argsort(rank_unique)]
    id_unique = id_unique[np.argsort(rank_unique)]
    name_unique = name_unique[np.argsort(rank_unique)]
    rank_id_name = np.array([rank_unique,id_unique,name_unique])

    # print(rank_id_name[:, 0:10])
    return rank_id_name[:, 0:10]

##scoring combination, you can combine multiple models and return the new document score, id and name
def socre_combination(query, index, fields):
    score = []
    id = []
    name = []
    for i in range(len(index)):
        Similarity_score, Similarity_id, Similarity_name = Similarity_module(index[i], query, fields)
        score += Similarity_score
        id += Similarity_id
        name += Similarity_name
    id_unique = sorted(set(id), key=id.index)
    score_unique = []
    name_unique = sorted(set(name),key=name.index)
    sum_score = 0
    for j in range(len(id_unique)):
        location = [i for i, a in enumerate(id) if a == id_unique[j]]
        for k in range(len(location)):
            sum_score = sum_score + score[location[k]]
        avg_score = sum_score / len(location)
        score_unique.append(float(avg_score))

        sum_score = 0
    score_unique = np.array(score_unique, dtype=np.float32)
    id_unique = np.array(id_unique,dtype=np.int32)
    name_unique = np.array(name_unique)
    score_unique = score_unique[np.argsort(-score_unique)]
    id_unique=id_unique[np.argsort(-score_unique)]
    name_unique =name_unique[np.argsort(-score_unique)]
    score_id_name = np.array([score_unique, id_unique, name_unique])
    # print(score_id_name)
    return score_id_name[:, 0:10]











