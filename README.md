# Model Fusion Engine

## Functional description


This is a search engine for movies and TV series hosted by Netflix. 

Users enter the query they want to search through the interactive interface (which can be the name, actors, directors and related content of the description) in order to query the database. 

The system will use multiple models to search the database and the results are integrated to give the best results. It provides users with two main search methods. The first one is the relatively rapid introduction of search, while the second is more advanced and users can go to search based on user requirements.



## Development environment

```
Python: 3.7
Elasticsearch: 7.6
Kibana: 7.62


```
## Project structure


```
-----Root
  |
  |----- netflix_titles.csv
  |
  |----- Index.py
  |
  |----- user_search.py
  |  |
  |  |----- Standard_function.py
  |  |
  |  |----- Advanced_function.py
  |
  |----- Evaluation.py
  |
  |----- Standard_Evaluation.py
  
When you import the project successfully, you need to set the main file as the sources root file.
```

## Usage
```
1. Open and set up the connection of elasticsearch and kibana with your computer.
2. Run SearchingEngineIn.py and and just run it once. This converts the csv to json file with different indices and uploads them onto Elasticsearch.
3. Run user_search.py and user can choose two ways to search:
   * Standard searching:
     * Type the query.
     * The Engine will get the doc.
   * Advanced searching:
     * choose models the user want to use
     * Select fields 
     * Choose the weights of different fields
     * Type the query
     * Choose the way of combination
     * The Engine will get the doc.

Note: It is better to ensure queries are more than one word.
```

