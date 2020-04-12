#!/usr/bin/env python
# coding: utf-8

# In[443]:


import glob,os
import re
import json
from ast import literal_eval
import pandas as pd
import itertools


# In[444]:


GlobalDict = {}

def find_doc(query,path):
    result = []
    for file in os.listdir(path):
        if file.endswith(query):
            result.append(os.path.join(path,file)) 
    return result

def dictcreate(query,j):

    querylen = len(query)

    for i in query:
        
        start = i.find("result/") 
        end = i.find("_query")
        substring = i[start:end]

        start = substring.find("/")
        end = substring.find("netflix")
        substring = substring[start+1:end]
        substring = substring + '_Q' + str(j) 
        with open(i, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                elif i == 1:
                    news = substring + '_title'
                    line = line.replace(" ",",")
                    line = line.replace("\n","")
                    GlobalDict[news] = literal_eval(line)
                    news = []
                elif i == 2:
                    news2 = substring + '_score'
                    line = line.replace("[","")
                    line = line.replace("   "," ")
                    line = line.replace("  ", " ")
                    line = line.replace("\n","")
                    GlobalDict[news2] = line
                elif i == 3:
                    xx = GlobalDict[news2]
                    line = line.replace("]", "")
                    line = line.replace("   "," ")
                    line = line.replace("  ", " ")
                    line = xx + line
                    line = line.split()
                    line = [float(i) for i in line]
                    
                    GlobalDict[news2] = line
        
                    
    return


path = os.getcwd() + '/result'

dictcreate(find_doc("query0_result",path),1)
dictcreate(find_doc("query1_result",path),2)
dictcreate(find_doc("query2_result",path),3)
dictcreate(find_doc("query3_result",path),4)
dictcreate(find_doc("query4_result",path),5)
dictcreate(find_doc("query5_result",path),6)
dictcreate(find_doc("query6_result",path),7)
dictcreate(find_doc("query7_result",path),8)
dictcreate(find_doc("query8_result",path),9)
dictcreate(find_doc("query9_result",path),10)


# In[445]:


df = pd.DataFrame.from_dict(GlobalDict)   


# In[462]:


def getscore(qd,df,model,lmodel):
           
    Query= 'Q' + str(qd) + '_'

#     print(Query)
    Q_data_index = [col for col in df if Query in col]

    Q_data = df[Q_data_index]
    Q_data = Q_data.apply(pd.to_numeric)

    modelstr = model + '_' + Query

#     print(Q_data)
#     print(modelstr)

    model_Q_index = [col for col in Q_data if modelstr in col]
    model_Q_data = Q_data[model_Q_index]
    
#     print(model_Q_data)


    model_Q_data_copy = model_Q_data.sort_values([col for col in model_Q_data if '_title' in col]).copy()


    for i in lmodel:
        lmodelstr = i + '_' + Query

        lmodel_Q_index = [col for col in Q_data if lmodelstr in col]
        lmodel_Q_data = Q_data[lmodel_Q_index]
        lmodel_Q_data_copy = lmodel_Q_data.sort_values([col for col in lmodel_Q_data if '_title' in col]).copy()

        modeltitle = modelstr + 'title'
        lmodeltitle = lmodelstr + 'title'

        modelscore = modelstr + 'score'
        lmodelscore = lmodelstr + 'score'



        lmodel_fi = lmodel_Q_data_copy[lmodeltitle].tolist()
#         print(lmodel_fi)
        model_fi = model_Q_data_copy[modeltitle].tolist()
#         print(model_fi)

        model_rowtodelete= list(itertools.filterfalse(set(lmodel_fi).__contains__, model_fi))
        lmodel_rowtodelete = list(itertools.filterfalse(set(model_fi).__contains__, lmodel_fi))
#         print(model_rowtodelete)
#         print(lmodel_rowtodelete)



        scoremodelcomb = model + '_' + i + '_score_combination'
        rankmodelcomb = model + '_' + i + '_rank_combination'



        for i in lmodel_rowtodelete:
            lmodel_index_todelete = lmodel_Q_data_copy[lmodel_Q_data_copy[lmodeltitle] == i].index
            lmodel_Q_data_copy.update(lmodel_Q_data_copy.drop(lmodel_index_todelete, inplace=True))


        for i in model_rowtodelete:
            model_index_todelete = model_Q_data_copy[model_Q_data_copy[modeltitle] == i].index
            model_Q_data_copy.update(model_Q_data_copy.drop(model_index_todelete, inplace=True))



        xx = lmodel_Q_data.sort_values(lmodeltitle).copy()
        yy = model_Q_data.sort_values(modeltitle).copy()


        xx_sorted_score = xx[lmodelscore].tolist()
        yy_sorted_score = yy[modelscore].tolist()

        average = [(g+h)/2 for g, h in zip(xx_sorted_score, yy_sorted_score)]


        score_combination = xx.copy()
        scorecombsc = 'Score_Combination_Scores' + '_Q' + str(qd)
        rankcombsc = 'Rank_Combination_Scores' + '_Q' + str(qd)

        score_combination[scorecombsc] = average


        del score_combination[lmodelscore]



        score_combination.rename({lmodeltitle: scoremodelcomb},axis='columns',inplace =True)



        final_score_combination = score_combination.sort_values(scorecombsc, ascending=False).copy()
        final_score_combination

#         print(final_score_combination)


        l = len(xx_sorted_score)
        rankperc = [*range(l,0,-1)]
        normrankperc = [(float(i)-min(rankperc))/(max(rankperc)-min(rankperc)) for i in rankperc]

        rankbm25 = lmodel_Q_data.copy()
        rankdfi = model_Q_data.copy()

        rankbm25['RankScores'] = rankperc
        rankdfi['RankScores'] = rankperc

        rankbm25copy = rankbm25.sort_values(lmodeltitle).copy()
        rankdficopy = rankdfi.sort_values(modeltitle).copy()

        xx_rank_score = rankbm25copy['RankScores'].tolist()
        yy_rank_score = rankdficopy['RankScores'].tolist()


        rank_average = [(g+h)/2 for g, h in zip(xx_rank_score, yy_rank_score)]


        rank_combination = rankbm25copy.sort_values(lmodeltitle).copy()
        rank_combination[rankcombsc] = rank_average

        del rank_combination[lmodelscore]
        del rank_combination['RankScores']

        rank_combination.rename({lmodeltitle: rankmodelcomb},axis='columns',inplace =True)
        final_rank_combination = rank_combination.sort_values(rankcombsc, ascending=False).copy()
        
        
        return final_score_combination[scorecombsc].mean(), final_rank_combination[rankcombsc].mean()


# In[ ]:


def Average(lst): 
    return sum(lst) / len(lst) 


scoredict = {}
rankdict = {}
def scorecombination(df,model,lmodel):
    
    highestscorecombination = []
    highestrankcombination = []
    
    Q = [1,2,3,4,5,6,7,8,9,10]
      
        
    for qd in Q:
        sc, rc = getscore(qd,df,model,lmodel)
        highestscorecombination.append(sc)
        highestrankcombination.append(rc)
        
    return Average(highestscorecombination), Average(highestrankcombination)
        
        

lmodels = ['bm25','ib', 'dfi', 'dfr', 'tfidf', 'lmd', 'lmj']


for i in lmodels:
    print(lmodels)
    for j in lmodels:
        if i == j:
            continue
        else:
            sc, rc = scorecombination(df,j,[i])  
            kk = j + '_' + i
            scoredict[kk] = sc
#             lmodels.remove[lmodels[0]]

            
#             rankdict[kk] = rc
    


# In[475]:


import csv
print(scoredict)


minval = min(scoredict.values())
maxval = max(scoredict.values())

for k in scoredict:
    scoredict[k] = (scoredict[k] - minval)/(maxval - minval)

    
print(scoredict)

