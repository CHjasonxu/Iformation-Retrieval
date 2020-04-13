# Information-Retrieval
# Meta-Search Engine

## Functional description

```
This is a search engine for movies and TV series hosted by Netflix. 

Users enter the query they want to search through the interactive interface (which can be the name, actors, directors and related content of the description) in order to query the database. 

The system will use multiple models to search the database and the results are integrated to give the best results. It provides users with two main search methods. The first one is the relatively rapid introduction of search, while the second is more advanced and users can go to search based on user requirements.
```


## Development environment

```
Python: 3.7
Elasticsearch: 2.x
Kibana: 7.62

When you import the project successfully, you need to set the main file as the root file.

```
## Project structure


```
SearchingEngineIn:
Standard_function:
Search_module:
```

## Usage
```
1.Open and set up the connection of elasticsearch and kibana with your computer.
2.Run the SearchingEngineIn.py and and just run it once. The data has been uploaded
```

## Test DEMO

```
label_query = ['Krish Trish and Baltiboy', 
                'Rings Lord', 
                'transformers', 
                'The Matrix', 
                'Star Trek', 
                'Vampire',
                'spider man',   
                'Rocky', 
                'Avengers', 
                'Indiana Jones']

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

index = ['bm25netflix','dfinetflix','ibnetflix','dfrnetflix','lmjnetflix','tfidfnetflix','lmdnetflix']

```
