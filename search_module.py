from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np

es = Elasticsearch(['localhost'],port=9200)

label_fields = ["title"]
fields = ["title","cast","country","description"]
weight_fields =["title^2","cast^1","country^1","description^3"]
label_id =[]
Similarity_score=[]
Similarity_id = []
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
def label(index,label_query,label_fields):
    label_id=[]
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=label_query, fields=label_fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        label_id.append(hit.meta.id)
    # print('This is label_id:', label_id)
    return label_id
def Similarity_module(index,query,fields):
    Similarity_score=[]
    Similarity_id =[]
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=query, fields=fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        Similarity_score.append(hit.meta.score)
        Similarity_id.append(hit.meta.id)
    # print('This is Similarity_score:', Similarity_score)
    # print('This is Similarity_id:', Similarity_id)
    return Similarity_score,Similarity_id

def Similarity_module_weight(index,query,weight_fields):
    Similarity_score=[]
    Similarity_id =[]
    s = Search(using=es, index=index)
    results = s.query("simple_query_string", query=query, fields=weight_fields,
                      auto_generate_synonyms_phrase_query=True).execute()
    for hit in results:
        Similarity_score.append(hit.meta.score)
        Similarity_id.append(hit.meta.id)
    # print('This is Similarity_score:', Similarity_score)
    # print('This is Similarity_id:', Similarity_id)
    return Similarity_score,Similarity_id

def cal_rec_pre(label_id,search_id):
    tmp = [val for val in label_id if val in search_id]
    precision = len(tmp) / len(label_id)
    recall = len(tmp) / len(search_id)
    f_measure = (2*precision*recall)/(precision+recall)
    return precision,recall,f_measure

if __name__ == '__main__':
    print("----------------------")
    label_query = ['Krish Trish and Baltiboy', 'Rings Lord', 'transformers', 'The Matrix', 'Star Trek', 'Vampire', 'spider man', 'Rocky', 'Avengers', 'Indiana Jones']
    query = ['which series of Krish Trish Baloy is about India', 'Lord of the Rings about going to Mordor to destroy Rings', 'Transformers beat Megatron', 'The matrix is about protecting Zion','Star ship explore new space','Boy and his sister meet the vampire every night', 'The spider man collection of parallel universes','Rocky fights with former Soviet soldiers', 'Avengers against thanos who has infinite stones','Indiana Jones tries to find Ark of Covenant']
    index = ['bm25netflix', 'dfinetflix','ibnetflix','dfrnetflix','lmjnetflix','tfidfnetflix','lmdnetflix']
    for i in range(len(index)):
        for j in range(len(label_query)):
            label_id = label(index[i], label_query[j], label_fields)
            size = len(label_id)
            Similarity_score,Similarity_id=Similarity_module(index[i],query[j],fields)
            w_Similarity_score,w_Similarity_id=Similarity_module_weight(index[i],query[j],weight_fields)
            precision, recall,f_measure = cal_rec_pre(label_id,Similarity_id)
            w_precision, w_recall,w_f_measure =cal_rec_pre(label_id,w_Similarity_id)
            tmp_precision = tmp_precision+precision
            tmp_recall = tmp_recall+recall
            tmp_f_measure = tmp_f_measure+f_measure
            w_tmp_precision = w_tmp_precision + w_precision
            w_tmp_recall = w_tmp_recall + w_recall
            w_f_measure =w_f_measure+w_f_measure
            output_score = np.array(Similarity_score)
            output_id = np.array(Similarity_id)
            output_query = np.array(query[j])
            Output_result=np.array([output_query,output_id,output_score])
            np.savetxt("result/%s_query"%index[i]+"%i_result"%j,Output_result,fmt='%s')
            w_output_score = np.array(w_Similarity_score)
            w_output_id = np.array(w_Similarity_id)
            W_Output_result = np.array([output_query, w_output_id, w_output_score])
            np.savetxt("result/W_%s_query" % index[i] + "%i_result" % j, W_Output_result, fmt='%s')
        Ag_precision.append(tmp_precision/len(label_query))
        Ag_recall.append(tmp_recall/len(label_query))
        Ag_f_measure.append(tmp_f_measure/len(label_query))
        tmp_precision=0
        tmp_recall=0
        tmp_f_measure =0
        W_Ag_precision.append(w_tmp_precision / len(label_query))
        W_Ag_recall.append(w_tmp_recall / len(label_query))
        W_Ag_f_measure.append(w_f_measure/len(label_query))
        w_tmp_precision = 0
        w_tmp_recall = 0
        w_f_measure = 0
    ag_precision=np.array(Ag_precision)
    ag_recall=np.array(Ag_recall)
    ag_f_measure = np.array(Ag_f_measure)
    w_ag_precision = np.array(W_Ag_precision)
    w_ag_recall = np.array(W_Ag_recall)
    w_ag_f_measure = np.array(W_Ag_f_measure)
    np.savetxt("result/Average_precision",ag_precision)
    np.savetxt("result/Average_recall",ag_recall)
    np.savetxt("result/Average_f_measure", ag_f_measure)
    np.savetxt("result/W_Average_precision", w_ag_precision)
    np.savetxt("result/W_Average_recall", w_ag_recall)
    np.savetxt("result/W_Average_f_measure", w_ag_f_measure)
    print("This is Ag_precision:",Ag_precision)
    print("This is Ag_recall:",Ag_recall)
    print("This is Ag_f_measure:", Ag_f_measure)
    print("This is W_Ag_precision:", W_Ag_precision)
    print("This is W_Ag_recall:", W_Ag_recall)
    print("This is W_Ag_f_measure:", W_Ag_f_measure)








