from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np
import sys
from search_module import Similarity_module,socre_combination,rank_combination
from Standard_function import Standard_similarity_module

es = Elasticsearch(['localhost'],port=9200)

label_fields = ["title"]
original_fields = ["type","title","director","cast","country","date_added","release_year","duration","description"]
fields = ["title","cast","country","description"]
weight_fields =["title^2","cast^1","country^3","description^4"]
index = ['bm25netflix', 'dfinetflix', 'ibnetflix', 'dfrnetflix', 'lmjnetflix', 'tfidfnetflix', 'lmdnetflix']

label_id =[]
Similarity_score=[]
Similarity_id = []
Similarity_name = []
field = []


def Get_results_score(query,index,fields):
    score_id_name = socre_combination(query, index, fields)
    print(score_id_name)
    for i in range(len(score_id_name)):
        print("Doc_%i:"%(i+1),score_id_name[:, i])
    return score_id_name

def Get_results_rank(query,index,fields):
    rank_id_name = rank_combination(query, index, fields)
    print(rank_id_name)
    for i in range(len(rank_id_name)):
        print("Doc_%i:"%(i+1),rank_id_name[:, i])
    return rank_id_name

def Get_standard_results(query,index,fields):
    Standard_score_id_name = Standard_similarity_module(query, index, fields)
    for i in range(len(Standard_score_id_name)):
        print("Doc_%i:"%(i+1),Standard_score_id_name[:, i])
    return Standard_score_id_name


def Standard_pattern():
    print("----------------------")
    query = input(
        "Please input the query you want: ")  # Example: Indiana Jones tries to find Ark of Covenant
    indexs = ['lmjnetflix','tfidfnetflix', 'lmdnetflix']
    weight_fields = ["title^2", "cast^1", "country^1", "description^4"]
    Get_standard_results(query, indexs, weight_fields)


def Advanced_pattern():
    field = []
    indexs = []
    print("----------------------")
    print('0-BM25', '1-DFI', '2-IB', '3-DFR', '4-LMJ', '5-TF-IDF', '6-LMJ')
    while True:
        try:
            indexs_selected = int(input("Please enter the number to select the model, otherwise press Enter: "))
            indexs += [index[indexs_selected]]
        except:
            break
    # i = int(input("Please enter the number to select the model you want: "))
    print("----------------------")
    print("0-type", "1-title", "2-director", "3-cast", "4-country", "5-date_added", "6-release_year",
          "7-duration", "8-description")
    while True:
        try:
            fields_selected = int(input("Please select one field you want if finished press Enter: "))
            field += [original_fields[fields_selected]]
        except:
            break
    print(field)
    print("----------------------")
    print("Select the weight of each field, default is 1")
    for j in range(len(field)):
        weight_select = input("The value of weight: ")
        field[j] += '^' + weight_select
    print(field)
    print("----------------------")
    query = input(
        "Please input the query you want: ")  # Example: Indiana Jones tries to find Ark of Covenant
    print("----------------------")
    rank_or_score = int(input(
        "Please select the rank combination or score combination(0 or 1): "))
    if rank_or_score ==0:
        Get_results_rank(query,indexs,field)
    else:
        Get_results_score(query, indexs, field)


if __name__ == '__main__':
    print("----------------------")
    print("There are two patterns: 1-Standard or 2-Advanced")
    pattern_select = int(input("Please input the number to select the pattern: "))
    if pattern_select == 1:
        Standard_pattern()
    else:
        Advanced_pattern()
