##Linux

curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.1-linux-x86_64.tar.gz
tar -xvf elasticsearch-7.6.1-linux-x86_64.tar.gz

cd elasticsearch-7.6.1/bin
./elasticsearch

./elasticsearch -Epath.data=data2 -Epath.logs=log2
./elasticsearch -Epath.data=data3 -Epath.logs=log3

git clone https://github.com/CHjasonxu/Iformation-Retrieval.git

curl -H "Content-Type: application/json" -XPOST "localhost:9200/bank/_bulk?pretty&refresh" --data-binary "@Netflix.json"
curl "localhost:9200/_cat/indices?v"





