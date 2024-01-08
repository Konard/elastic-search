# elastic-search

To create a script in Python that loads an array of strings to Elasticsearch Docker container and then allow user to search from CLI, follow these steps. But before starting make sure Docker and Elasticsearch are installed on your machine.  

1. First, start the Elasticsearch Docker container with the following command: 

```bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.1
```

2. Then, create a Python script. We'll use two external libraries: `elasticsearch`, for interacting with Elasticsearch, and `click`, for building command line interfaces. Install them using `pip`:

```bash
pip install click
pip3 install 'elasticsearch<7.14.0'
pip install tensorflow tensorflow_text tensorflow_hub universal_sentence_encoder
```

3. Now let's build the script. Create a Python file named `search_script.py`, and use the following script:



4. Direct your command-line interface to the folder where you've saved the `search_script.py` file. 

5. Run

```bash
python search.py index
```

and follow the prompt to index a string. The script will store your string in an Elasticsearch index called `text_index`.

6. Search for the string by running

```bash
python search.py search
```

and following the prompt to enter a search query. The script will retrieve and print any stored strings that match the query.

Note: This script is a simple example and might not cover more complicated use-cases. For larger and more complex data, you'll likely want to expand on this to include error-checking, handling of different data types, handling bulk data, etc. Also, keep in mind Elasticsearch indices should be created and configured as per your requirements. The example assumes Elasticsearch is empty and creates indices with the default settings.