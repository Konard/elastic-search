import click
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['localhost:9200'])

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

@click.group()
def cli():
    pass

@click.command()
# @click.option('--str', 'input_str', prompt=True)
# def create(input_str):
def create():
    index = 'text_index'
    # settings = {}
    # mappings = {}
    body = {
        "settings": {},
        "mappings": { "properties": { "text_vector": { "type": "dense_vector", "dims": 384 } } }
    }
    es.indices.create(index=index, body=body)

    click.echo(f"Index {index} is created with settings {json.dumps(body, indent=4)}")

@click.command()
@click.option('--str', 'input_str', prompt=True)
def index(input_str):
    """Index a string in Elasticsearch."""
    text_embedding = model.encode([input_str])[0]

    body = {'text': input_str, 'text_vector': text_embedding}
    
    res = es.index(index='text_index', body=body)
    click.echo(f"Indexed {input_str} with id {res['_id']}")

@click.command()
@click.option('--search', 'search_string', prompt=True)
def search(search_string):
    """Find strings semantically similar to the search query in Elasticsearch."""
    search_vector = model.encode([search_string])[0]

    print(type(search_vector))
    print(type(search_vector[0]))
    print(f"{search_vector}")

    body = {
        'query': {
            'script_score': {
                'query': {'match_all': {}},
                'script': {
                    'source': "cosineSimilarity(params.query_vector, 'text_vector') + 1.0",
                    'params': {'query_vector': search_vector}
                }
            }
        }
    }

    # doc['text_vector'].size()

    # cosineSimilarity(params.query_vector, 'text_vector')
    # cosineSimilarity(params.query_vector, doc['text_vector'])

    # "source": "doc['my_vector'].size() == 0 ? 0 : cosineSimilarity(params.queryVector, 'my_vector')"

    # "script": {
    #     "source": "cosineSimilarity(params.query_vector, 'abs_emb') + 1.0",
    #     "params": {"query_vector": query_vector}
    # }


    try:
        res = es.search(index='text_index', body=body)
        click.echo("Search results:")
        for doc in res['hits']['hits']:
            click.echo(f"{doc['_id']} {doc['_score']}: {doc['_source']['text']}")
    except Exception as inst:
        print(type(inst))
        print(json.dumps(inst.args, indent=4))
        # print(json.dumps(inst, indent=4))


cli.add_command(create)
cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    cli()