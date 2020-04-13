from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np
from Advance_function import*

es = Elasticsearch(['localhost'],port=9200)

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

print("----------------------")
label_query = ['Krish Trish and Baltiboy', 'Rings Lord', 'transformers', 'The Matrix', 'Star Trek', 'Vampire',
               'spider man', 'Rocky', 'Avengers', 'Indiana Jones']
query = ['which series of Krish Trish Baloy is about India',
         'Lord of the Rings about going to Mordor to destroy Rings',
         'Transformers beat Megatron',
         'The matrix is about protecting Zion',
         'Star ship explore new space',
         'Boy and his sister meet the vampire every night',
         'The spider man collection of parallel universes',
         'Rocky fights with former Soviet soldiers',
         'Avengers against thanos who has infinite stones',
         'Indiana Jones tries to find Ark of Covenant']
index = ['bm25netflix', 'dfinetflix', 'ibnetflix', 'dfrnetflix', 'lmjnetflix', 'tfidfnetflix', 'lmdnetflix']
for i in range(len(index)):
    for j in range(len(label_query)):
        label_id = label(index[i], label_query[j], label_fields)
        size = len(label_id)
        Similarity_score, Similarity_id, Similarity_title = Similarity_module(index[i], query[j], fields)
        w_Similarity_score, w_Similarity_id, w_Similarity_title = Similarity_module_weight(index[i], query[j],
                                                                                           weight_fields)
        precision, recall, f_measure = cal_rec_pre(label_id, Similarity_id)
        w_precision, w_recall, w_f_measure = cal_rec_pre(label_id, w_Similarity_id)
        tmp_precision = tmp_precision + precision
        tmp_recall = tmp_recall + recall
        tmp_f_measure = tmp_f_measure + f_measure
        w_tmp_precision = w_tmp_precision + w_precision
        w_tmp_recall = w_tmp_recall + w_recall
        w_f_measure = w_f_measure + w_f_measure
        output_score = np.array(Similarity_score)
        output_id = np.array(Similarity_id)
        output_query = np.array(query[j])
        Output_result = np.array([output_query, output_id, output_score])
        np.savetxt("result/%s_query" % index[i] + "%i_result" % j, Output_result, fmt='%s')
        w_output_score = np.array(w_Similarity_score)
        w_output_id = np.array(w_Similarity_id)
        W_Output_result = np.array([output_query, w_output_id, w_output_score])
        np.savetxt("result/W_%s_query" % index[i] + "%i_result" % j, W_Output_result, fmt='%s')
    Ag_precision.append(tmp_precision / len(label_query))
    Ag_recall.append(tmp_recall / len(label_query))
    Ag_f_measure.append(tmp_f_measure / len(label_query))
    tmp_precision = 0
    tmp_recall = 0
    tmp_f_measure = 0
    W_Ag_precision.append(w_tmp_precision / len(label_query))
    W_Ag_recall.append(w_tmp_recall / len(label_query))
    W_Ag_f_measure.append(w_f_measure / len(label_query))
    w_tmp_precision = 0
    w_tmp_recall = 0
    w_f_measure = 0
ag_precision = np.array(Ag_precision)
ag_recall = np.array(Ag_recall)
ag_f_measure = np.array(Ag_f_measure)
w_ag_precision = np.array(W_Ag_precision)
w_ag_recall = np.array(W_Ag_recall)
w_ag_f_measure = np.array(W_Ag_f_measure)
np.savetxt("result/Average_precision", ag_precision)
np.savetxt("result/Average_recall", ag_recall)
np.savetxt("result/Average_f_measure", ag_f_measure)
np.savetxt("result/W_Average_precision", w_ag_precision)
np.savetxt("result/W_Average_recall", w_ag_recall)
np.savetxt("result/W_Average_f_measure", w_ag_f_measure)
print("This is Ag_precision:", Ag_precision)
print("This is Ag_recall:", Ag_recall)
print("This is Ag_f_measure:", Ag_f_measure)
print("This is W_Ag_precision:", W_Ag_precision)
print("This is W_Ag_recall:", W_Ag_recall)
print("This is W_Ag_f_measure:", W_Ag_f_measure)

Avg_tau = []
max_p = 0
min_p = 10000
for i in range(7):
    for j in range(7):
        tmp = 0
        tau = 0
        for k in range(len(query)):
            if i < j:
                tau = Kendall_rank_correlation(index[i], index[j], query[k], fields)
                # print(tau)
            tmp = tmp + tau
        p = tmp / len(query)
        if max_p < p:
            max_p = p
            max_indexi = i
            max_indexj = j
        if p != 0:
            Avg_tau.append((index[i], index[j], p))

            if min_p > p:
                min_p = p
                min_indexi = i
                min_indexj = j
        tmp = 0
        tau = 0
        # print(index[i],index[j],(tmp/len(query)))
print("This is AVG_tau:", Avg_tau)
print("What combination has the highest tau:", index[max_indexi], index[max_indexj], max_p)
print("What combination has the lowest tau:", index[min_indexi], index[min_indexj], min_p)