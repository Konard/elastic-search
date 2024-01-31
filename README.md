[![Gitpod](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/konard/elastic-search)

# elastic-search

To create a script in Python that loads an array of strings to Elasticsearch Docker container and then allow user to search from CLI, follow these steps. But before starting make sure Docker and Elasticsearch are installed on your machine.  

1. First, start the Elasticsearch Docker container with the following command: 

```bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.1
```

2. Then, create a Python script. We'll use two external libraries: `elasticsearch`, for interacting with Elasticsearch, and `click`, for building command line interfaces. Install them using `pip`:

For GitPod (or if you have 3.12+ python installed):
```
pyenv install 3.11
pyenv global 3.11
```

```bash
pip install click 'elasticsearch<7.14.0' tensorflow tensorflow_text tensorflow_hub
```

5. Run

```bash
python vector_search.py create
```

```bash
python vector_search.py index --str "dog"
```

and follow the prompt to index a string. The script will store your string in an Elasticsearch index called `text_index`.

6. Search for the string by running

```bash
python vector_search.py search --search "dog"
```

Clear elastic search index

```bash
curl -X DELETE 'http://localhost:9200/_all'
```

and following the prompt to enter a search query. The script will retrieve and print any stored strings that match the query.

Note: This script is a simple example and might not cover more complicated use-cases. For larger and more complex data, you'll likely want to expand on this to include error-checking, handling of different data types, handling bulk data, etc. Also, keep in mind Elasticsearch indices should be created and configured as per your requirements. The example assumes Elasticsearch is empty and creates indices with the default settings.
