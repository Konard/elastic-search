import click
import json
from elasticsearch import Elasticsearch

@click.group()
def cli():
    pass

@click.command()
@click.option('--str', 'input_str', prompt=True)
def index(input_str):
    """Index a string in Elasticsearch."""
    es = Elasticsearch(['http://localhost:9200'])
    body = {'text': input_str}
    res = es.index(index='text_index', body=body)
    click.echo(f"Indexed {input_str} with id {res['_id']}")

@click.command()
@click.option('--search', 'search_string', prompt=True)
def search(search_string):
    """Search for a string in Elasticsearch."""
    es = Elasticsearch(['localhost:9200'])
    body = {
        'query': {
            'match': {
                'text': search_string
            }
        } 
    }
    res = es.search(index='text_index', body=body)
    click.echo("Search results:")
    click.echo(json.dumps(res, indent=2))
    for doc in res['hits']['hits']:
        click.echo(f"{doc['_source']['text']}")

cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    cli()