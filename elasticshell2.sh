git clone https://github.com/CHjasonxu/Iformation-Retrieval.git

curl -H "Content-Type: application/x-ndjson" -XPOST "localhost:9200/bank/_bulk?pretty&refresh" --data-binary "@NetflixDataJson.json"
curl "localhost:9200/_cat/indices?v"
