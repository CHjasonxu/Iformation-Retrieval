from elasticsearch import Elasticsearch
from Advance_function import Similarity_module, label, cal_rec_pre
import numpy as np

##WEIGHTED AND UNWEIGHTED FIELDS CREATED HERE AND LISTS TO FILL IN THE PRECISION AND RECALL
fields =["title^2","cast^1","country^1","description^3"]
index = ['tfidfnetflix','lmjnetflix', 'ibnetflix']


nfields =["title","cast","country","description"]
label_fields = ["title"]
label_id =[]
Similarity_score=[]
Similarity_id = []
Similarity_title = []
Similarity_name =[]
tmp_precision =0
tmp_recall =0
tmp_f_measure =0
tmp_precision_rank =0
tmp_recall_rank =0
tmp_f_measure_rank =0

Ag_precision = []
Ag_recall = []
Ag_f_measure = []
W_Ag_precision = []
W_Ag_recall = []
W_Ag_f_measure =[]


Ag_precision_rank = []
Ag_recall_rank = []
Ag_f_measure_rank = []
W_Ag_precision_rank = []
W_Ag_recall_rank = []
W_Ag_f_measure_rank =[]

##Use different models to search and match the query and return the score, id and name and also does score combination.

def Standard_similarity_moduletwo(query, index, wfields,nfields):
    score = []
    id = []
    name = []
    for i in range(len(index)):
        if i == 'tfidfnetflix':
            cfields = wfields
        else:
            cfields = nfields

        Similarity_score, Similarity_id, Similarity_name = Similarity_module(index[i], query, cfields)
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
    return list(map(str,list(id_unique[0:10])))


##Use different models to search and match the query and return the score, id and name and also does rank combination.
def rank_combinationtwo(query,index,wfields, nfields):
    score = []
    id = []
    name = []
    rank = []
    for i in range(len(index)):
        if i == 'tfidfnetflix':
            cfields = wfields
        else:
            cfields = nfields
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
    return list(map(str,list(id_unique[0:10])))



##CALLS THE FUNCTIONS AND CALCULATES THE SCORE AND RANK COMBINATION.
if __name__ == '__main__':
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
    
    weight_fields = ["title^2", "cast^1", "country^1", "description^3"]
    normal_fields = ["title", "cast", "country", "description"]

       

##FOR LOOP GOES THROUGH ALL THE QUERIES ABOVE AND ASSESSES THE MAP and MEAN AVERAGE RECALL
    for j in range(len(label_query)):
       
        label_id = label('bm25netflix', label_query[j], label_fields)

        score = []
        id = []
        name = []

        id_unique = Standard_similarity_moduletwo(query[j], index, weight_fields,normal_fields)
 
        id_unique_rank = rank_combinationtwo(query[j], index, weight_fields,normal_fields)


##PRECISION CALCULATED IN cal_rec_pre, WEIGHTED PRECISION CALCULATED IN cal_rec_pre
       
        
        precision, recall,f_measure = cal_rec_pre(label_id,id_unique)

        
        precision_rank, recall_rank,f_measure_rank =cal_rec_pre(label_id,id_unique_rank)

        tmp_precision = tmp_precision+precision
        tmp_recall = tmp_recall+recall
        tmp_f_measure = tmp_f_measure+f_measure

        tmp_precision_rank = tmp_precision_rank+precision_rank
        tmp_recall_rank = tmp_recall_rank+recall_rank
        tmp_f_measure_rank = tmp_f_measure_rank+f_measure_rank
    

##CALCULATES THE AVERAGE PRECISION AND RECALL 
    Ag_precision.append(tmp_precision/len(label_query))
    Ag_recall.append(tmp_recall/len(label_query))
    Ag_f_measure.append(tmp_f_measure/len(label_query))

    ag_precision = np.array(Ag_precision)
    ag_recall = np.array(Ag_recall)
    ag_f_measure = np.array(Ag_f_measure)
##SAVES SCORE DATA TO TEXT FILE
    np.savetxt("result/Score_Average_precision", ag_precision)
    np.savetxt("result/Score_Average_recall", ag_recall)
    np.savetxt("result/Score_Average_f_measure", ag_f_measure)


    Ag_precision_rank.append(tmp_precision/len(label_query))
    Ag_recall_rank.append(tmp_recall/len(label_query))
    Ag_f_measure_rank.append(tmp_f_measure/len(label_query))

    ag_precision_rank = np.array(Ag_precision_rank)
    ag_recall_rank = np.array(Ag_recall_rank)
    ag_f_measure_rank = np.array(Ag_f_measure_rank)
##SAVES RANK DATA TO TEXT FILE
    np.savetxt("result/Score_Average_precision", ag_precision_rank)
    np.savetxt("result/Score_Average_recall", ag_recall_rank)
    np.savetxt("result/Score_Average_f_measure", ag_f_measure_rank)

    tmp_precision=0
    tmp_recall=0
    tmp_f_measure =0


    print("This is Score Ag_precision:",Ag_precision)
    print("This is Score Ag_recall:",Ag_recall)
    print("This is Score Ag_f_measure:", Ag_f_measure)

    print("This is Rank Ag_precision:",Ag_precision_rank)
    print("This is Rank Ag_recall:",Ag_recall_rank)
    print("This is Rank Ag_f_measure:", Ag_f_measure_rank)
    #print("This is W_Ag_precision:", W_Ag_precision)
    #print("This is W_Ag_recall:", W_Ag_recall)
    #print("This is W_Ag_f_measure:", W_Ag_f_measure)

    #Avg_tau = []
    #max_p = 0
    #min_p = 10000
    #for i in range(7):
     #   for j in range(7):
      #      tmp = 0
       #     tau = 0
        #    for k in range(len(query)):
         #       if i < j:
          #          tau = Kendall_rank_correlation(index[i], index[j],query[k],fields)
           #         # print(tau)
            #    tmp = tmp + tau
            #p = tmp/len(query)
            #if max_p < p:
             #   max_p = p
              #  max_indexi = i
               # max_indexj = j
            #if p != 0:
             #   Avg_tau.append((index[i], index[j],p))

              #  if min_p > p:
               #     min_p = p
                #    min_indexi = i
                 #   min_indexj = j
            #tmp = 0
            #tau = 0
            # print(index[i],index[j],(tmp/len(query)))
   # print("This is AVG_tau:",Avg_tau)
    #print("What combination has the highest tau:",index[max_indexi], index[max_indexj],max_p)
    #print("What combination has the lowest tau:", index[min_indexi], index[min_indexj],min_p)










