from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np
import sys
from search_module import Similarity_module


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


def Get_results(query,index,fields):

    Similarity_score, Similarity_id, Similarity_name = Similarity_module(index, query, fields)
    for i in range(len(Similarity_name)):
        print("Doc_%i:"%(i+1),Similarity_name[i])
    return Similarity_score, Similarity_id, Similarity_name


if __name__ == '__main__':
    print("----------------------")
    print('0-BM25', '1-DFI', '2-IB', '3-DFR', '4-LMJ', '5-TF-IDF', '6-LMJ')
    i = int(input("Please enter the number to select the model you want: "))
    print("----------------------")
    print("0-type", "1-title", "2-director", "3-cast", "4-country", "5-date_added", "6-release_year",
          "7-duration", "8-description")
    while True:
        try:

            fields_selected = int(input("Please select one field you want: "))
            field += [original_fields[fields_selected]]
        except:
            break
    print(field)
    print("----------------------")

    print("----------------------")
    query = input("Please input the query you want: ") # Example: Lord of the Rings about going to Mordor to destroy Rings

    Get_results(query, index[i], field)

