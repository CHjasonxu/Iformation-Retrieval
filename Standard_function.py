from elasticsearch import Elasticsearch
from search_module import Similarity_module
import numpy as np

fields =["title^2","cast^1","country^3","description^4"]
index = ['bm25netflix', 'dfinetflix', 'ibnetflix', 'dfrnetflix', 'lmjnetflix', 'tfidfnetflix', 'lmdnetflix']
indexs = []
Similarity_score=[]
Similarity_id = []
Similarity_name =[]

# def rank_combination(query,index,fields):
#     score = []
#     id = []
#     name = []
#     rank = []
#     for i in range(len(index)):
#         _, Similarity_id, Similarity_name = Similarity_module(index[i], query, fields)
#         rank += [1,2,3,4,5,6,7,8,9,10]
#         id += Similarity_id
#         name += Similarity_name
#     print(id)
#     #l2 = sorted(set(l1), key=l1.index)
#     id_unique = sorted(set(id), key=id.index)
#     rank_unique = []
#     name_unique = sorted(set(name), key=name.index)
#     location=[]
#     sum_rank = 0
#     for j in range (len(id_unique)):
#         location = [i for i, a in enumerate(id) if a == id[j]]
#         for k in range(len(location)):
#             sum_rank = sum_rank + rank[location[k]]
#         avg_rank = sum_rank/len(location)
#         rank_unique.append(avg_rank)
#         sum_rank = 0
#     rank_id_name = np.array([rank_unique,id_unique,name_unique])
#     rank_id_name.T[np.lexsort(rank_id_name[::-1, :])].T
#     print(rank_id_name[:, 0:10])

def Standard_similarity_module(query, index, fields):
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
    name_unique = sorted(set(name), key=name.index)
    sum_score = 0
    for j in range(len(id_unique)):
        location = [i for i, a in enumerate(id) if a == id_unique[j]]
        for k in range(len(location)):
            sum_score = sum_score + score[location[k]]
        avg_score = sum_score / len(location)
        score_unique.append(float(avg_score))

        sum_score = 0
    score_unique = np.array(score_unique, dtype=np.float32)
    id_unique = np.array(id_unique, dtype=np.int32)
    name_unique = np.array(name_unique)
    score_unique = score_unique[np.argsort(-score_unique)]
    id_unique = id_unique[np.argsort(-score_unique)]
    name_unique = name_unique[np.argsort(-score_unique)]
    score_id_name = np.array([score_unique, id_unique, name_unique])
    # print(score_id_name)
    return score_id_name[:, 0:10]


