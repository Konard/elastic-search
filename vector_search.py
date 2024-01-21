import click
import tensorflow_hub as hub
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost:9200'])

# Load the Universal Sentence Encoder module from TensorFlow Hub.
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

@click.group()
def cli():
    pass

@click.command()
@click.option('--str', 'input_str', prompt=True)
def index(input_str):
    """Index a string in Elasticsearch."""
    # text_embedding = embed([input_str])[0].numpy().tolist()
    text_embedding = [4.2, 3.4, -0.2]

    body = {'text': input_str, 'text_vector': text_embedding}
    res = es.index(index='text_index', body=body)
    click.echo(f"Indexed {input_str} with id {res['_id']}")

@click.command()
@click.option('--search', 'search_string', prompt=True)
def search(search_string):
    """Find strings semantically similar to the search query in Elasticsearch."""
    # search_vector = embed([search_string])[0].numpy().tolist()
    search_vector = [4.2, 3.4, -0.2]

    print(type(search_vector))
    print(type(search_vector[0]))
    print(f"{search_vector}")

    body = {
        'query': {
            'script_score': {
                'query': {'match_all': {}},
                'script': {
                    'source': "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
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


    res = es.search(index='text_index', body=body)
    click.echo("Search results:")
    for doc in res['hits']['hits']:
        click.echo(f"{doc['_id']} {doc['_score']}: {doc['_source']['text']}")

cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    cli()