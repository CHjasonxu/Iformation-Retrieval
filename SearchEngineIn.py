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


##basicmodel be,d,g,if,in,ine   after_effect no,b,l          normalization = no,h1,h2,h3,z  
## normalization.h2/h1/h3/z/c (float values)
jsondfrtext = '{"settings":{"index":{"similarity":{"my_similarity":{"type": "DFR","basic_model": "g","after_effect": "l","normalization": "h3","normalization.h2.c": "3.0"}}}}}'
headers = {'Content-type': 'application/json',}
DFRtext = requests.put('http://localhost:9200/dfrnetflix?pretty' , headers=headers, data=jsondfrtext)


##bm25 
##bm25 ##CAN PUT BM25 ON SPECIFIC FIELDS IN THE MAPPING! and the rest use defaul similarity
## {  "settings": {    "similarity": {      "my_custom_similarity": {        "type": "BM25",        "b": 0,        "k1": 2         }    }  },  "mappings": {    "doc": {      "properties": {        "cast": {          "type":       "text"        },        "country": {          "type":       "text"        },{        "date_added": {          "type":       "text"        },        "description": {          "type":       "text",          "similarity": "my_custom_similarity"                },        {        "director": {          "type":       "text"        },        "duration": {          "type":       "text"        },{        "rating": {          "type":       "text"        },        "release_year": {          "type":       "text"        },        {        "timestamp": {          "type":       "text"        },        "title": {          "type":       "text"        },{        "rating": {          "type":       "text"        }   }    }  }}'

jsonbm25text = '{"settings":{"index":{"similarity":{"my_bm25__similarity":{"type":"BM25","b": "0","k1": "2"}}}}}'
headers = {'Content-type': 'application/json',}
bm25text = requests.put('http://localhost:9200/bm25netflix?pretty' , headers=headers, data=jsonbm25text)


### Scripted Similarity
jsontfidftext = '{"settings":{"index":{"similarity":{"scripted_tfidf":{"type": "scripted","script": {"source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"}}}}}'
headers = {'Content-type': 'application/json',}
tfidftext = requests.put('http://localhost:9200/tfidfnetflix?pretty' , headers=headers, data=jsontfidftext)


###DFI similarity
jsondfitext = '{"settings":{"index":{"similarity":{"dfi":{"type": "DFI","independence_measure":"standardized"}}}}}'
headers = {'Content-type': 'application/json',}
dfitext = requests.put('http://localhost:9200/dfinetflix?pretty' , headers=headers, data=jsondfitext)


##LM Dircichlet similarity
jsonlmdtext = '{"settings":{"index":{"similarity":{"esserverbook_lm_dircichlet_similarity":{"type": "LMDirichlet","mu":"2000"}}}}}'
headers = {'Content-type': 'application/json',}
lmdtext = requests.put('http://localhost:9200/lmdnetflix?pretty' , headers=headers, data=jsonlmdtext)


##LM Jelinek Mercer Similarity
jsonlmjtext = '{"settings":{"index":{"similarity":{"esserverbook_lm_jelinek_mercer_similarity":{"type": "LMJelinekMercer","lambda":"0.7"}}}}}'
headers = {'Content-type': 'application/json',}
lmjtext = requests.put('http://localhost:9200/lmjnetflix?pretty' , headers=headers, data=jsonlmjtext)


##IB Similarity
jsonibtext = '{"settings":{"index":{"similarity":{"esserverbook_ib_similarity":{"type": "IB","distribution":"ll","lambda":"df","normalization":"z","normalization.z.z":"0.25"}}}}}'
headers = {'Content-type': 'application/json',}
ibtext = requests.put('http://localhost:9200/ibnetflix?pretty' , headers=headers, data=jsonibtext)




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
        

        res_dfr = es.index(index="bm25netflix", id=i, body=doc)
        res_bm25 = es.index(index="dfrnetflix", id=i, body=doc)
        res_dfi = es.index(index="dfinetflix", id=i, body=doc)
        res_idf = es.index(index="tfidfnetflix", id=i, body=doc)
        res_lmd = es.index(index="lmdnetflix", id=i, body=doc)
        res_lmj = es.index(index="lmjnetflix", id=i, body=doc)
        res_ib = es.index(index="ibnetflix", id=i, body=doc)


        i+=1
     


es.indices.refresh(index="dfrnetflix")
es.indices.refresh(index="bm25netflix")
es.indices.refresh(index="tfidfnetflix")
es.indices.refresh(index="dfinetflix")
es.indices.refresh(index="lmdnetflix")
es.indices.refresh(index="lmjnetflix")
es.indices.refresh(index="ibnetflix")


res_dfr = es.search(index="dfrnetflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_dfr['hits']['total']['value'])

print(DFRtext.json())
DFRsettings = requests.get('http://localhost:9200/dfrnetflix/_settings?pretty' , headers=headers)
print(DFRsettings.json())



res_bm25 = es.search(index="bm25netflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_bm25['hits']['total']['value'])

print(bm25text.json())
bm25settings = requests.get('http://localhost:9200/bm25netflix/_settings?pretty' , headers=headers)
print(bm25settings.json())


res_tfidf = es.search(index="tfidfnetflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_tfidf['hits']['total']['value'])

print(tfidftext.json())
tfidfsettings = requests.get('http://localhost:9200/tfidfnetflix/_settings?pretty' , headers=headers)
print(tfidfsettings.json())


res_dfi = es.search(index="dfinetflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_dfi['hits']['total']['value'])

print(dfitext.json())
dfisettings = requests.get('http://localhost:9200/tfidfnetflix/_settings?pretty' , headers=headers)
print(dfisettings.json())



res_lmd = es.search(index="lmdnetflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_lmd['hits']['total']['value'])

print(lmdtext.json())
lmdsettings = requests.get('http://localhost:9200/lmdnetflix/_settings?pretty' , headers=headers)
print(lmdsettings.json())


res_lmj = es.search(index="lmjnetflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_lmj['hits']['total']['value'])


print(lmjtext.json())
lmjsettings = requests.get('http://localhost:9200/lmjnetflix/_settings?pretty' , headers=headers)
print(lmjsettings.json())


res_ib = es.search(index="ibnetflix", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_ib['hits']['total']['value'])

print(ibtext.json())
ibsettings = requests.get('http://localhost:9200/ibnetflix/_settings?pretty' , headers=headers)
print(ibsettings.json())



