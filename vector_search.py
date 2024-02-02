import click
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import json
import re

es = Elasticsearch(['localhost:9200'])

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

space = ' '
dot = '.'
whitespace_regex = re.compile(r"\s+")
model_string_limit = 128

def split_string(string):
    string = whitespace_regex.sub(space, string).strip().lower()
    sentences = string.split(dot)

    for sentence in sentences:
        if len(sentence) >= model_string_limit:
            print(sentence)
            raise ValueError(f"Sentence is longer than {model_string_limit}.")

    return sentences

def index_strings(strings):
    text_embeddings = model.encode(strings)

    for text_embedding in text_embeddings:
        body = {'text': string, 'text_vector': text_embedding}
        res = es.index(index='text_index', body=body)
        print(f"Indexed {string} with id {res['_id']}.")

def index_string(string):
    text_embedding = model.encode([string.lower()])[0]

    body = {'text': string, 'text_vector': text_embedding}
    
    res = es.index(index='text_index', body=body)
    click.echo(f"Indexed {string} with id {res['_id']}")

def search_string(query):
    query_embedding = model.encode([query.lower()])[0]

    body = {
        'query': {
            'script_score': {
                'query': {'match_all': {}},
                'script': {
                    # "source": "doc['text_vector'].size() == 0 ? 0 : cosineSimilarity(params.query_embedding, 'text_vector') + 1.0"
                    'source': "cosineSimilarity(params.query_embedding, 'text_vector') + 1.0",
                    'params': {'query_embedding': query_embedding}
                }
            }
        }
    }

    try:
        res = es.search(index='text_index', body=body)
        click.echo("Search results:")
        for doc in res['hits']['hits']:
            click.echo(f"{doc['_id']} {doc['_score']}: {doc['_source']['text']}")
    except Exception as inst:
        print(type(inst))
        print(json.dumps(inst.args, indent=4))

@click.group()
def cli():
    pass

@click.command()
def create():
    index = 'text_index'
    body = {
        "settings": {},
        "mappings": { "properties": { "text_vector": { "type": "dense_vector", "dims": 384 } } }
    }
    es.indices.create(index=index, body=body)

    click.echo(f"Index {index} is created with settings {json.dumps(body, indent=4)}")

@click.command()
@click.option('--string', 'string', prompt=True)
def index(string):
    """Index a string in Elasticsearch."""
    index_string(string)

@click.command()
@click.option('--query', 'query', prompt=True)
def search(query):
    """Find strings semantically similar to the search query in Elasticsearch."""
    search_string(query)


cli.add_command(create)
cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    cli()