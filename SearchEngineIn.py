#!/usr/bin/env python
# coding: utf-8


from datetime import datetime
from elasticsearch import Elasticsearch
import csv, json
import pandas as pd
import requests

es = Elasticsearch(['localhost'],port=9200,timeout=30)


data = {}
idd = {}
line2 = {}
listline2 = []
listdata = []
director = {}

with open('netflix_titles.csv', 'r', encoding='utf-8') as csvfile:
    csvReader = csv.DictReader(csvfile)
    i=1
    for rows in csvReader:
        idd["_id"] = rows['show_id']
        data["index"] = idd

        line2["type"] = rows['type']
        line2["title"] = rows['title']
        
        if not rows["director"]:
            line2["director"] = ['None']
        else:
            line2["director"] = rows['director'].split(',')
            
        if not rows['cast']:
            line2["cast"] = ['None']
        else:        
            line2["cast"] = rows['cast'].split(',')
            
            
        if not rows['country']:
            line2["country"] = ['None']
        else:
            line2["country"] = rows['country'].split(',')
        line2["date_added"] = rows['date_added']
        line2["release_year"] = rows['release_year']
        line2["rating"] = rows['rating']
        line2["duration"] = rows['duration']
        
        if not rows['listed_in']:
            line2["listed_in"] = ['None']
        else:
            line2["description"] = rows['description']
            
        line2["timestamp"] = datetime.now()
            
        doc = line2
        

        res = es.index(index="netflixdata", id=i, body=doc)
        i+=1
     



es.indices.refresh(index="netflixdata")

res = es.search(index="netflixdata", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(title)s: %(description)s" % hit["_source"])


##basicmodel be,d,g,if,in,ine   after_effect no,b,l          normalization = no,h1,h2,h3,z  
## normalization.h2/h1/h3/z/c (float values)

jsontext = '{"settings":{"index":{"similarity":{"my_similarity":{"type": "DFR","basic_model": "g","after_effect": "l","normalization": "h3","normalization.h2.c": "3.0"}}}}}'

headers = {'Content-type': 'application/json',}

DFRtext = requests.put('http://localhost:9200/index?pretty' , headers=headers, data=jsontext)

print(DFRtext.json())





