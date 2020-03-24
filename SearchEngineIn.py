#!/usr/bin/env python
# coding: utf-8


from datetime import datetime
from elasticsearch import Elasticsearch
import csv, json
import pandas as pd
es = Elasticsearch(['localhost'],port=9200)


data = {}
idd = {}
line2 = {}
listline2 = []
listdata = []
director = {}

with open('/home/maz/Information Retrieval/Search Engine/NetflixData.csv') as csvfile:
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
        print(res['result'])



es.indices.refresh(index="netflixdata")

res = es.search(index="netflixdata", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(title)s: %(description)s" % hit["_source"])

