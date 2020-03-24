##Linux

#curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.1-linux-x86_64.tar.gz
#tar -xvf elasticsearch-7.6.1-linux-x86_64.tar.gz

## macOS
#curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.1-darwin-x86_64.tar.gz
#tar -xvf elasticsearch-7.6.1-darwin-x86_64.tar.gz


cd elasticsearch-7.6.1/bin
./elasticsearch

./elasticsearch -Epath.data=data2 -Epath.logs=log2
./elasticsearch -Epath.data=data3 -Epath.logs=log3





